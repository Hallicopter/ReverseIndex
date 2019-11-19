from elasticSearch import elasticSearch
import pprint
import pdf2txt


from flask import Flask, render_template, flash, request
# from flask import Flask
app = Flask(__name__)
global es
@app.route('/')
def index():
   return render_template('form.html')

@app.route('/', methods=['POST'])
def createElasticSearchObj():
    global es
    if request.form['singlebutton'] == 'getInput':
        text = request.form['textarea']
        es = elasticSearch()
        es.raw_text = text
    elif request.form['singlebutton'] == 'indexDoc':
        try:
            es==None
        except:
            return render_template('form.html') + \
            '<script>alert("Please enter text first!");</script>'

        es.convertToDocs()
        for d in es.doc_data:
            es.indexDoc(d)
       
    elif request.form['singlebutton'] == 'search':
        try:
            es==None
        except:
            return render_template('form.html') + \
            '<script>alert("Please enter text first!");</script>'

        if es.invertedIndex  == {}:
            return render_template('form.html') + \
            '<script>alert("Please index first!");</script>'
            
        paras = es.search(request.form['searchterm'])

        if paras == None:
            return render_template('form.html') + \
            '<script>alert("Word not found!");</script>'

        pretty = '<ol>'
        for para in paras:
            pretty+='<li>' + para + "</li>"
        pretty+='</ol>'
        pretty+='<a href="/">Search again!</a>'

        return pretty

    elif request.form['singlebutton'] == 'clear':
        es.invertedIndex = {}
        return render_template('form.html') + \
            '<script>alert("Cleared Index!");</script>'

    return render_template('form.html')

@app.route('/pdf')
def pdfPage():
    return render_template('formPDF.html')

@app.route('/pdf', methods=['POST'])
def pdfElasticSearch():
    global es
    if 'singlebutton' not in request.form:
        pdfFileObj = request.files['file']
        pdfFileObj.save(pdfFileObj.filename)
        text = pdf2txt.convert_pdf_to_txt(pdfFileObj.filename)
        print(text)
        es = elasticSearch()
        es.raw_text = text
    elif request.form['singlebutton'] == 'indexDoc':
        try:
            es==None
        except:
            return render_template('formPDF.html') + \
            '<script>alert("Please enter text first!");</script>'

        es.convertToDocs()
        for d in es.doc_data:
            es.indexDoc(d)
       
    elif request.form['singlebutton'] == 'search':
        try:
            es==None
        except:
            return render_template('formPDF.html') + \
            '<script>alert("Please enter text first!");</script>'

        if es.invertedIndex  == {}:
            return render_template('formPDF.html') + \
            '<script>alert("Please index first!");</script>'
            
        paras = es.search(request.form['searchterm'])

        if paras == None:
            return render_template('formPDF.html') + \
            '<script>alert("Word not found!");</script>'

        pretty = '<ol>'
        for para in paras:
            pretty+='<li>' + para + "</li>"
        pretty+='</ol>'
        pretty+='<a href="/pdf">Search again!</a>'

        return pretty

    elif request.form['singlebutton'] == 'clear':
        es.invertedIndex = {}
        return render_template('formPDF.html') + \
            '<script>alert("Cleared Index!");</script>'

    return render_template('formPDF.html')
    

if __name__ == '__main__':
   app.run(debug = True)





