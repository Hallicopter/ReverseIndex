import uuid
import pprint

class elasticSearch:

    def __init__(self):
        self.doc_data = {}
        self.wordList = []
        self.invertedIndex = {}
        self.raw_text = ''


    # Takes the raw string text input, breaks
    # it down to documents with unique ids.
    # Returns docs dict of document and IDs
    def convertToDocs(self):
        raw_text = self.raw_text.lower()
        d1 = raw_text.split('\r\n\r')
        d2 = raw_text.split('\n\n')
        if len(d1)>len(d2):
            documents = d1
        else:
            documents = d2
        
        for doc in documents:
            uid = uuid.uuid4()
            self.doc_data[uid] = doc
            


    def indexDoc(self, docId):
        tokenized_doc = self.doc_data[docId].split()
        
        for word in tokenized_doc:
            if word in self.invertedIndex:
                if docId in self.invertedIndex[word]:
                    self.invertedIndex[word][docId]+=1
                else:
                    self.invertedIndex[word][docId]=1
            else:
                self.invertedIndex[word] = {docId: 1}
    
    def search(self, word):
        if word in self.invertedIndex:
            docIds = self.invertedIndex[word]
            TopTenSortedDocIds = sorted(docIds.items(), key=lambda kv: kv[1])[:10]
            paras = []
            for docId in TopTenSortedDocIds:
                print(self.doc_data[docId[0]])
                paras.append(self.doc_data[docId[0]])
            return paras
        else:
            return None