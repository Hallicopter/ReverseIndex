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
        self.raw_text = self.raw_text.lower()
        documents = self.raw_text.split('\n\n')
        
        for doc in documents:
            uid = uuid.uuid4()
            self.doc_data[uid] = doc
            # self.docIdList.append(uid)


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
        docIds = self.invertedIndex[word]
        TopTenSortedDocIds = sorted(docIds.items(), key=lambda kv: kv[1]) 
        paras = []
        for docId in TopTenSortedDocIds:
            print(self.doc_data[docId[0]])
            paras.append(self.doc_data[docId[0]])
        return paras