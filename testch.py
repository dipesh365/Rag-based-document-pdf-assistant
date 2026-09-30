from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="",#core 
    chunk_size=10,
    chunk_overlap=1
)

data=TextLoader("document loaders/notesch.txt")

docs=data.load()
chunks=splitter.split_documents(docs)

for i in chunks:
    print(i.page_content)
    print()
    print()
    print()


















































#document=the nodes whichi have created and we just have to load the node
#when we load something the text is converted into pdf