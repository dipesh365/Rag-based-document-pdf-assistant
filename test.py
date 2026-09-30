from langchain_community.document_loaders import TextLoader

data=TextLoader("document loaders/notes.txt")

docs=data.load()

print(len(docs))



















































#document=the nodes whichi have created and we just have to load the node
#when we load something the text is converted into pdf