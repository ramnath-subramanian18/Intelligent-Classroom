import face_recognition as fr
import datetime
from datetime import datetime
from flask import *
import os
import cv2
import face_recognition
import numpy as np
import pandas as pd
from flask import Flask, render_template
from flask_wtf import Form
from flaskext import mysql
from wtforms.fields.html5 import DateField
import pymysql

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

#from yourapp import create_app
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
date_from_form=""
path = 'faces'
images = []
classNames = []
myList = os.listdir(path)
    #removing .jpg in each file
#print(myList)


from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

# If modifying these scopes, delete the file token.json.
credentials=None
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE='C:/Users/ramna/Downloads/json/sheet-312206-c827ee848f90.json'
credentials=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)


SAMPLE_SPREADSHEET_ID = '1WgJcdnZoHEWkSEh5G5kZHx2R3GRrRDaY8fwtzVA84pY'


service = build('sheets', 'v4', credentials=credentials)


sheet = service.spreadsheets()

result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Sheet4!A1").execute()
#print(result)
values = result.get('values', [])
print(values)


for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
#print(classNames)

#Initialize the Flask app
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)




app.config['SECRET_KEY'] = 'secret'
app.secret_key = 'SHH!'
camera = cv2.VideoCapture(0)
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnown = findEncodings(images)

def send_mail_to_student(mail_id,name):
   fromaddr = "notification.attendance.alert@gmail.com"
   toaddr = mail_id
   msg = MIMEMultipart()
   msg['From'] = fromaddr
   msg['To'] = toaddr
   msg['Subject'] = "Low Attendance Alert"
   #Change body
   body = "Greetings,\n\nThis email is to inform you that your  attendance has fallen short of the minimum university requirements. If the attendance percentage falls below 75% before exams, he/she will not be allowed to write exams"
   msg.attach(MIMEText(body, 'plain'))
   s = smtplib.SMTP('smtp.gmail.com', 587)
   s.starttls()
   s.login(fromaddr, "Capstone123!!")
   text = msg.as_string()
   s.sendmail(fromaddr, toaddr, text)
   s.quit()

def send_mail_to_parent(mail_id,name):
   fromaddr = "notification.attendance.alert@gmail.com"
   toaddr = mail_id
   msg = MIMEMultipart()
   msg['From'] = fromaddr
   msg['To'] = toaddr
   msg['Subject'] = "Low Attendance Alert"
   body = "Greetings,\n\nThis email is to inform you that your ward's attendance has fallen short of the minimum university requirements. If the attendance percentage falls below 75% before exams, he/she will not be allowed to write exams"
   msg.attach(MIMEText(body, 'plain'))
   s = smtplib.SMTP('smtp.gmail.com', 587)
   s.starttls()
   s.login(fromaddr, "Capstone123!!")
   text = msg.as_string()
   s.sendmail(fromaddr, toaddr, text)
   s.quit()



def markAttendance(name):
    with open('attend1.csv', 'r+') as f:
        myDatalist = f.readlines()
        nameList = []
        #print(myDatalist)
        for line in myDatalist:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtstring}')
# live attendance
def gen_frames1():  # generate frame by frame from camera

    while True:
        # Capture frame-by-frame
        success, img = camera.read()  # read the camera frame
        if not success:
            break
        else:
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
            print(facesCurFrame)
            print(encodesCurFrame)
            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                name = ""
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex]
                    #print(name)
                    y1, x2, y2, x1 = faceLoc
                    # y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                    #markAttendance(name)
                    time_now= datetime.now().strftime('%H:%M:%S')
                    attendance_update(name, time_now, date_from_form)


            ret, jpeg = cv2.imencode('.jpg', img)
            data = []
            data.append(jpeg.tobytes())
            data.append(name)
            frame = data[0]

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
def attendance_update(regno,time,date1):
   connection = pymysql.connect(host="localhost", user="root", passwd="", database=id)
   cursor = connection.cursor()
   query='''INSERT INTO NAME VALUES(REG,'TIME');'''.replace("REG",regno).replace("TIME",time).replace("NAME",date1)
   #Ensure Error handling for duplication
   cursor.execute(query)
   connection.commit()
   connection.close()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return render_template("home.html")



@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        #print(str(curl))
        global faculty_id
        faculty_id = "FACULTY_" + str(user["id"])

        #print("FACULTY_ID = "+str(user["id"]))
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("main.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")
#global faculty_id
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']

        connection = pymysql.connect(host="localhost", user="root", passwd="", database="flaskdb")
        cursor = connection.cursor()
        id_query = '''SELECT ID FROM users WHERE name="abc"'''.replace("abc",name);

        cursor.execute(id_query)
        #global faculty_id
        global faculty_id
        myresult = cursor.fetchall()
        for x in myresult:
            #print(x)

            faculty_id = "FACULTY_" + str(x[0])
        print(faculty_id)

        create_db_query="CREATE DATABASE db;".replace("db",faculty_id);
        cursor.execute(create_db_query)
        connection = pymysql.connect(host="localhost", user="root", passwd="", database=faculty_id)
        create_table_faculty_query = """CREATE TABLE NAME1(REGNO VARCHAR(9) PRIMARY KEY,NAME VARCHAR(30), PRESENT_DAYS INT, TOTAL_DAYS INT,
                       ATTEND_PERCENT FLOAT, MARKS FLOAT);""".replace("NAME1", faculty_id)
        cursor.execute(create_table_faculty_query)

        connection = pymysql.connect(host="localhost", user="root", passwd="", database=faculty_id)
        cursor = connection.cursor()
        create_main_db="""CREATE TABLE NAME1(NAME varchar(30) ,REGNO VARCHAR(9) PRIMARY KEY,PHONE bigint(10),PARENT_PHONE bigint(10),
        EMAIL varchar(100),PARENT_EMAIL varchar(100),PRESENT_DAYS int(11),TOTAL_DAYS int(11),ATTEND_PERCENT float, MARKS float);""".replace("NAME1",'maindb');
        cursor.execute(create_main_db)
        cursor.close()
        connection.close()
        return redirect(url_for('login'))






'''@app.route('/')
def upload():
    return render_template("main.html")'''
def get_encoded_faces():
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded
#upload face detection
def classify_face(img):
    face_names = []
    namestr = ""

    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    #img = cv2.imread(im, 1)
    # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    # img = img[:,:,::-1]

    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
        markAttendance(name)
        #print(date_from_form)
        time_now = datetime.now().strftime('%H:%M:%S')
        attendance_update(name, time_now, date_from_form)
        namestr += name + ','

    return namestr.strip(',')

class ExampleForm(Form):
    dt = DateField('DatePicker', format='%Y-%m-%d')
    #print(dt)
#create  a new table or particular date
def create_table(date1):
    print(faculty_id)
    connection = pymysql.connect(host="localhost", user="root", passwd="", database=faculty_id)
    cursor = connection.cursor()
    NEWTABLE = 'CREATE TABLE NAME(REGNO VARCHAR(9) PRIMARY KEY,TIME TIME);'.replace("NAME",date1)
    cursor.execute(NEWTABLE)
    connection.close()

def attendance_update(regno,time,date1):
   connection = pymysql.connect(host="localhost", user="root", passwd="", database=faculty_id)
   cursor = connection.cursor()
   query='''INSERT INTO NAME VALUES('REG','TIME');'''.replace("REG",regno).replace("TIME",time).replace("NAME",date1)
   #Ensure Error handling for duplication
   cursor.execute(query)
   connection.commit()
   connection.close()

#displaying the image of the upload image
@app.route('/success', methods = ['POST','GET'])
def success():

    #target = os.path.join(APP_ROOT, 'faces/')
    if request.method == 'POST':
        f = request.files['file']
        img = cv2.imread(f.filename, 1)
        target = os.path.join(APP_ROOT, 'test/')

        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename
            destination = "/".join([target, filename])
            print("Accept incoming file:", filename)
            print("Save it to:", destination)
            upload.save(destination)
        return render_template("index10.html",image_name=filename, message ='Face: '+classify_face(img))


@app.route('/data',methods=['GET','POST'])
def data():

    file='attend1.csv'
    data=pd.read_csv(file)
    return render_template('data.html',data=data.to_html())
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

def unknown_image_encoded(img):

    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding

@app.route('/clear')
def clear():
   """UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;"""
   connection = pymysql.connect(host="localhost", user="root", passwd="", database=faculty_id)
   cursor = connection.cursor()
   present_days_query = """UPDATE maindb   
      SET PRESENT_DAYS=PRESENT_DAYS+1
      WHERE REGNO IN (SELECT REGNO FROM table_name);
      """.replace("table_name", date_from_form)
   attend_perecent_query="""UPDATE maindb   
   SET TOTAL_DAYS=TOTAL_DAYS+1, ATTEND_PERCENT=(PRESENT_DAYS/TOTAL_DAYS)*100;
   """.replace("table_name",date_from_form)
   cursor.execute(present_days_query)
   cursor.execute(attend_perecent_query)
   get_emails = """SELECT NAME,EMAIL,PARENT_EMAIL FROM maindb WHERE ATTEND_PERCENT<75"""
   cursor.execute(get_emails)
   myresult = cursor.fetchall()
   # print(myresult)
   for x in myresult:
       print(x[0])
       send_mail_to_student(x[1], x[0])
       send_mail_to_parent(x[2], x[0])
   connection.commit()
   connection.close()
   return render_template('clear.html')

def show_attendance(date5):
    global myresult
    connection = pymysql.connect(host="localhost", user="root", passwd="", database=faculty_id)
    cursor = connection.cursor()
    view_attendance_query = """SELECT NAME,REGNO AS REGISTER_NUMBER
           FROM maindb  where REGNO IN (SELECT REGNO FROM dat);""".replace("dat", date5)
    cursor.execute(view_attendance_query)
    myresult = cursor.fetchall()
    #return render_template('index.html', data=myresult)
    for x in myresult:
        print(x)
    connection.close()

def show_attendance1(date5):
    global myresult1
    connection = pymysql.connect(host="localhost", user="root", passwd="", database=faculty_id)
    cursor = connection.cursor()
    view_attendance_query = """SELECT NAME,REGNO AS REGISTER_NUMBER
           FROM maindb where REGNO NOT IN (SELECT REGNO FROM dat);""".replace("dat", date5)
    cursor.execute(view_attendance_query)
    myresult1 = cursor.fetchall()
    #return render_template('index.html', data=myresult1)
    for x in myresult1:
        print(x)
    connection.close()

@app.route('/success1')
def success1():

    return render_template('index10.html')
@app.route('/attendance_System')
def attendance_System():

    return render_template('view_start_attendance.html')

@app.route('/main_attendance_page')
def main_attendance_page():

    return render_template('index.html')

@app.route('/video_feed')
def video_feed():

    #gen_frames()
    #Video streaming route. Put this in the src attribute of an img tag
    #return Response(gen_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame',)
    aoa = [['1']]
    global values

    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet4!a1",
                                    valueInputOption="USER_ENTERED", body={"values": aoa}).execute()
    return render_template('re_directed_ri_pi.html')


@app.route('/start_attendance', methods=['POST','GET'])
def start_attendance():
    global date_from_form
    form = ExampleForm()
    if form.validate_on_submit():
        date_from_form=form.dt.data.strftime('%d_%m_%Y')
        create_table(date_from_form)

    return render_template('choose_date_attendance1.html', form=form)

@app.route('/choose_date_display_attendance', methods=['POST','GET'])
def choose_date_display_attendance():
    global date_from_form1
    form = ExampleForm()
    if form.validate_on_submit():
        date_from_form1=form.dt.data.strftime('%d_%m_%Y')
        #create_table(date_from_form)
        print(date_from_form1)

    return render_template('choose_date_view.html', form=form)


@app.route('/display_attendance_date_wise', methods=['POST','GET'])
def display_attendance_date_wise():
    show_attendance(date_from_form1)
    show_attendance1(date_from_form1)
    return render_template('show_attendance.html', data=myresult, data1=myresult1)



@app.route('/Upload_new_face',methods=["GET","POST"])
def hello():
    if request.method=="POST":

        first_name = request.form['fname']
        regno = request.form['regno']

        phone = request.form['phone']
        pphone = request.form['pphone']
        email_id = request.form['emailid']
        pemailid = request.form['pemailid']
        connection = pymysql.connect(host="localhost", user="root", passwd="", database=faculty_id)
        cursor = connection.cursor()
        query = "INSERT INTO maindb(NAME,REGNO,PHONE,PARENT_PHONE,EMAIL,PARENT_EMAIL) VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (first_name, regno, phone, pphone, email_id, pemailid))
        connection.commit()
        file=request.files["file"]
        file.save(os.path.join("faces",file.filename))
    return render_template("upload.html",message="upload")


@app.route('/back')
def back():
    return render_template("view_start_attendance.html")
@app.route('/back1')
def back1():
    return render_template("main.html")
@app.route('/back3')
def back3():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug = True)