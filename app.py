from elasticSearch import elasticSearch
import pprint

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
        if es.doc_data == {}:
            return render_template('form.html') + \
            '<script>alert("Please index first!");</script>'
        paras = es.search(request.form['searchterm'])
        if paras == None:
            return render_template('form.html') + \
            '<script>alert("Word not found!");</script>'
        pretty = '<ol>'
        print(paras)
        for para in paras:
            pretty+='<li>' + para + "</li>"
        pretty+='</ol>'

        pretty+='<a href="/">Search again!</a>'
        return pretty

    # template = open('templates/form.html', 'a+')
    # template.write(str(es.search('lorem')))
    # template.close()
    return render_template('form.html')

if __name__ == '__main__':
   app.run(debug = True)





