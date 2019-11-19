from elasticSearch import elasticSearch
import pprint
import pdf2txt
import pdfkit

from flask import Flask, render_template, flash, request, send_file
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
        
        output = ''
        pretty = '<ol>'
        for para in paras:
            output += ' ' + para[:] + '\n \n'
            pretty+='<li>' + para + "</li>"
        pretty+='</ol>'
        pretty+='<a href="/pdf">Search again!</a>'
        pretty+='<br><a href="/out">Download output.</a>'
        pdfkit.from_string(output, "/tmp/out.pdf")
        return pretty

    elif request.form['singlebutton'] == 'clear':
        es.invertedIndex = {}
        return render_template('formPDF.html') + \
            '<script>alert("Cleared Index!");</script>'

    return render_template('formPDF.html')

@app.route('/out')
def return_files_tut():
	try:
		return send_file('/tmp/out.pdf', attachment_filename='out.pdf')
	except Exception as e:
		return str(e)
    

if __name__ == '__main__':
   app.run(debug = True)





