from elasticSearch import elasticSearch
import pprint
# import pdf2txt
import pdfkit

from flask import Flask, render_template, flash, request, send_file
# from flask import Flask


def merge_dict(d1, d2):
    
    for el in d2:
        if el in d1:
            d1[el].update(d2[el])
        else:
            d1[el] = d2[el]
    print(d1)
    return d1

app = Flask(__name__)
global es
@app.route('/')
def index():
   return render_template('form.html')

@app.route('/', methods=['POST'])
def createElasticSearchObj():
    global es
    # if request.form['singlebutton'] == 'getInput':
        
    if request.form['singlebutton'] == 'indexDoc':
        text = request.form['textarea']
        
       
        try:
            if es!=None:
                es_tmp = elasticSearch()
                es_tmp.raw_text = text
                es_tmp.convertToDocs()
                for d in es_tmp.doc_data:
                    es_tmp.indexDoc(d)
                # es.invertedIndex.update(es_tmp.invertedIndex)
                es.invertedIndex = merge_dict(es.invertedIndex, es_tmp.invertedIndex)
                # inv_es = {v: k for k, v in my_map.items()}
                es.doc_data.update(es_tmp.doc_data)
                print(es.invertedIndex)

        except:
            es = elasticSearch()
            es.raw_text = text
            # return render_template('form.html') + \
            # '<script>alert("Please enter text first!");</script>'
            es.convertToDocs()
            for d in es.doc_data:
                es.indexDoc(d)
        
        
       
    elif request.form['singlebutton'] == 'search':
        
        try:
            print('wooot', es.invertedIndex)
        except:
            return render_template('form.html') + \
            '<script>alert("Please enter text first!");</script>'

       
            
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
        es = None
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
        text = convert_pdf_to_txt(pdfFileObj.filename)
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
        pdfkit.from_string(output, "out.pdf")
        return pretty

    elif request.form['singlebutton'] == 'clear':
        es = elasticSearch()
        return render_template('formPDF.html') + \
            '<script>alert("Cleared Index!");</script>'

    return render_template('formPDF.html')

@app.route('/out')
def return_files_tut():
	try:
		return send_file('out.pdf', attachment_filename='out.pdf')
	except Exception as e:
		return str(e)
    

if __name__ == '__main__':
   app.run(debug = True)





from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO



def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text