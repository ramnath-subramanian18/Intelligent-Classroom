import nltk
import pymysql

nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import gensim
import numpy as np
from nltk.tokenize import word_tokenize
import os



from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')
'''
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    global processed_text
    processed_text=text
    print(processed_text)
    #detect_text_from_image()

    #hard(processed_text)

    return render_template("my-form.html")


'''

processed_text=5
path1="C:/Users/ramna/PycharmProjects/face/capstone/test"
def func(path):

    file_docs = []

    with open ('C:/Users/ramna/PycharmProjects/face/capstone/imp.txt') as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file_docs.append(line)

    gen_docs = [[w.lower() for w in word_tokenize(text)]
                for text in file_docs]

    #print(gen_docs)

    dictionary = gensim.corpora.Dictionary(gen_docs)
    #print(dictionary.token2id)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]

    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('C:/Users/ramna/PycharmProjects/face/',tf_idf[corpus],
                                           num_features=len(dictionary))

    file2_docs = []

    with open (path) as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file2_docs.append(line)

    #print("Number of documents:",len(file2_docs))
    for line in file2_docs:
        query_doc = [w.lower() for w in word_tokenize(line)]
        query_doc_bow = dictionary.doc2bow(query_doc) #update an existing dictionary andcreate bag of words
# perform a similarity query against the corpus
    query_doc_tf_idf = tf_idf[query_doc_bow]

    sum_of_sims =(np.sum(sims[query_doc_tf_idf], dtype=np.float32))
    #print(sum_of_sims)

    percentage_of_similarity = round(float((sum_of_sims / len(file_docs)) * 100))

    avg_sims = [] # array of averages
    global t_avg
    t_avg=0
    # for line in query documents
    for line in file2_docs:
        # tokenize words
        query_doc = [w.lower() for w in word_tokenize(line)]
        # create bag of words
        query_doc_bow = dictionary.doc2bow(query_doc)
        # find similarity for each document
        query_doc_tf_idf = tf_idf[query_doc_bow]
        # print (document_number, document_similarity)
        #print('Comparing Result:', sims[query_doc_tf_idf])
        # calculate sum of similarities for each query doc
        sum_of_sims =(np.sum(sims[query_doc_tf_idf], dtype=np.float32))
        # calculate average of similarity for each query doc
        avg = sum_of_sims / len(file_docs)

        t_avg+=avg
        # print average of similarity for each query doc
        #print(f'avg: {sum_of_sims / len(file_docs)}')
        # add average values into array
        avg_sims.append(avg)
    print(t_avg)



    # calculate total average
    total_avg = np.sum(avg_sims, dtype=np.float)
    # round the value and multiply by 100 to format it as percentage
    percentage_of_similarity = round(float(total_avg) * 100)
    # if percentage is greater than 100
    # that means documents are almost same
    if percentage_of_similarity >= 100:
        percentage_of_similarity = 100
    return t_avg
dirListing = os.listdir(path1)
editFiles = []

marks = []
textfile=[]
textfile_without_comma=[]
textfile=[]
def func1():
    #print("hello")
    dirListing = os.listdir(path1)
    for item in dirListing:
        if ".txt" in item:
            textfile.append(item)
            #print(textfile)
            marks.append(func(item))
    print(marks)

    for i in textfile:
        split=i.split(".")
        substring = split[0]
        textfile_without_comma.append(substring)
    print("hi")
    print(textfile_without_comma)




p=[]
final_marks=[]
def hard(processed_text1):
    print(processed_text1)
    k = 5
    p = [i * 100 for i in marks]
    print(p)
    for i in range(4):
        if (p[i] > 75):
            final_marks.append(k)


        elif (p[i] > 50 and p[i] < 75):
            final_marks.append(k * 0.75)
        elif (p[i] < 50 and p[i] > 30):
            final_marks.append(k * 0.5)
        else:
            final_marks.append(0)
    print(final_marks)
    copied(path1)
    copied_final_marks()
def medium(processed_text1):
    print(processed_text1)
    k = 5
    p = [i * 100 for i in marks]
    print(p)
    for i in range(4):
        if (p[i] > 70):
            final_marks.append(k)


        elif (p[i] > 45 and p[i] < 70):
            final_marks.append(k * 0.75)
        elif (p[i] < 45 and p[i] > 25):
            final_marks.append(k * 0.5)
        else:
            final_marks.append(0)
    print(final_marks)
    copied(path1)
    copied_final_marks()
def easy(processed_text1):
    print(processed_text1)
    k = 5
    p = [i * 100 for i in marks]
    print(p)
    for i in range(4):
        if (p[i] > 65):
            final_marks.append(k)


        elif (p[i] > 40 and p[i] <= 65):
            final_marks.append(k * 0.75)
        elif (p[i] < 40 and p[i] > 20):
            final_marks.append(k * 0.5)
        else:
            final_marks.append(0)
    print(final_marks)
    copied(path1)
    #copied_final_marks()



@app.route('/hard1')
def hard1():
    hard(processed_text)
    return render_template("my-form.html")


@app.route('/medium1')
def medium1():
    medium(processed_text)
    return render_template("my-form.html")


@app.route('/easy1')
def easy1():
    easy(processed_text)
    return render_template("my-form.html")

copy = []
def copied(path1):
    os.chdir(path1)
    s = []
    copied_student1 = []
    copied_student = []
    copied_student2 = []

    def read_text_file(file_path1):
        with open(file_path1, 'r') as f:
            s.append(f.read())

    # iterate through all file
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path1 = f"{path1}\{file}"

            # call read text file function
            read_text_file(file_path1)



    dirListing = os.listdir(path1)
    editFiles = []
    for item in dirListing:
        if ".txt" in item:
            editFiles.append(item)
    print(editFiles)
    n = 0
    j=1
    while (n < 4):

        while (j < 4):
            #print(j)
            #print(n)
            from fuzzywuzzy import fuzz
            match_perc = fuzz.ratio(s[n].lower(), s[j].lower())
            #print(match_perc)
            if (match_perc > 95):
                copied_student1.append(editFiles[n])
                #print(editFiles[n])
                copied_student2.append(editFiles[j])
                #print(editFiles[j])
            j += 1

        n += 1
        j=n+1


    i=0
    copied_student = copied_student1 + copied_student2
    for i in copied_student:
        split = i.split(".")
        substring = split[0]
        copy.append(substring)

    print("copied students"+str(copy))


def update_marks(regno,marks):
	"""UPDATE table_name
	SET column1 = value1, column2 = value2, ...
	WHERE condition;"""
	connection = pymysql.connect(host="localhost", user="root", passwd="", database="mysqldata")
	cursor = connection.cursor()
	marks_query="""UPDATE main_db1   
	  SET MARKS=MARK1
	  WHERE REGNO='regno1';
	  """.replace("MARK1", marks).replace("regno1", regno)
	cursor.execute(marks_query)
	connection.commit()
	connection.close()


def copied_final_marks():
    i=0
    while (i < 4):
        j = 0
        while (j < len(copy)):
            if (textfile_without_comma[i] == copy[j]):
                # print(i)
                final_marks[i] = final_marks[i] / 2
            j += 1
        #print(final_marks[i])
        #print(textfile_without_comma[i])
        update_marks(textfile_without_comma[i], str(final_marks[i]))


        i += 1
    print("marks of students"+str(final_marks))
    print("students name" +str(textfile_without_comma))



processed_text=''
@app.route('/input', methods=["GET", "POST"])
def new1():
    if request.method == "POST":


        text = request.form['text']
        processed_text = text.upper()
        f = open("C:/Users/ramna/PycharmProjects/face/capstone/imp.txt", "w")
        f.write(processed_text)
        f.close()
        #detect_document('C:/Users/ramna/PycharmProjects/face/capstone/test/')
        detect_text_from_image()
        func1()

    return render_template("my-form.html", message="upload")






os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ramna/Downloads/json/Capstone1-082408e27af0.json"






def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    text = ''
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    text += word_text + ' '
    return (text)


def detect_text_from_image():
    path1 = "C:/Users/ramna/PycharmProjects/face/capstone/test/"
    dirListing = os.listdir(path1)
    editFiles = []
    i = 0
    while (i < 4):
        for item in dirListing:

            if ".jpeg" in item:
                split = item.split(".")
                substring = split[0]
                editFiles.append(substring+'.txt')
                f = open(editFiles[i], "w")
                f.write(detect_document(item))
                f.close()
                i = i + 1


if __name__ == '__main__':
    app.run(debug = True)
