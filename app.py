import streamlit as st
import os
import tempfile
import shutil
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="DocMind — RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0f0f13;
    color: #e2e2e8;
}
.stApp { background: #0f0f13; }

[data-testid="stSidebar"] {
    background: #16161d !important;
    border-right: 1px solid #2a2a35;
}

.hero {
    padding: 2.5rem 0 1.5rem 0;
    border-bottom: 1px solid #2a2a35;
    margin-bottom: 2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 0.9rem;
    color: #6b6b7e;
    margin-top: 0.4rem;
    letter-spacing: 0.02em;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1e1e2a;
    border: 1px solid #2a2a38;
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.78rem;
    color: #9ca3af;
    margin-bottom: 1.5rem;
}
.dot-green  { width:8px; height:8px; border-radius:50%; background:#34d399; display:inline-block; }
.dot-yellow { width:8px; height:8px; border-radius:50%; background:#fbbf24; display:inline-block; }

.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    max-height: 55vh;
    overflow-y: auto;
    padding: 1rem 0.5rem;
    margin-bottom: 1.5rem;
}
.bubble-user {
    align-self: flex-end;
    background: linear-gradient(135deg, #6d28d9, #4f46e5);
    color: #fff;
    padding: 0.75rem 1.1rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 70%;
    font-size: 0.92rem;
    line-height: 1.55;
}
.bubble-ai {
    align-self: flex-start;
    background: #1e1e2a;
    border: 1px solid #2a2a38;
    color: #d1d5db;
    padding: 0.85rem 1.2rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 75%;
    font-size: 0.92rem;
    line-height: 1.65;
}
.bubble-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
    color: #7c7c8e;
}
.bubble-ai   .bubble-label { color: #a78bfa; }
.bubble-user .bubble-label { color: #c4b5fd; }

.source-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.6rem;
}
.source-chip {
    background: #252530;
    border: 1px solid #33334a;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.72rem;
    color: #9ca3af;
}

.stTextInput > div > div > input {
    background: #1a1a24 !important;
    border: 1px solid #2e2e42 !important;
    border-radius: 10px !important;
    color: #e2e2e8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 0.65rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px #7c3aed22 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.danger-btn > button {
    background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
}

[data-testid="stFileUploader"] {
    background: #16161d;
    border: 1.5px dashed #2e2e42;
    border-radius: 12px;
    padding: 1rem;
}

.sidebar-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #5a5a6e;
    margin-bottom: 0.5rem;
    margin-top: 1.2rem;
}

.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #3d3d52;
}
.empty-icon { font-size: 2.8rem; margin-bottom: 0.8rem; }
.empty-text { font-size: 0.9rem; line-height: 1.6; }

.warn-box {
    background: #2a1f10;
    border: 1px solid #78350f;
    border-radius: 8px;
    padding: 0.7rem 0.9rem;
    font-size: 0.8rem;
    color: #fbbf24;
    margin-top: 0.5rem;
    line-height: 1.5;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
for key, default in {
    "messages": [],
    "vectorstore": None,
    "doc_name": None,
    "show_cleared_msg": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.2rem 0 0.5rem 0;">
        <div style="font-family:'Syne',sans-serif; font-size:1.25rem; font-weight:800;
                    background:linear-gradient(90deg,#a78bfa,#60a5fa);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">🧠 DocMind</div>
        <div style="font-size:0.72rem; color:#4a4a5e; margin-top:2px; letter-spacing:0.05em;">
            RAG-powered document assistant
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Upload ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">Upload Document</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        label="Upload PDF",
        type=["pdf"],
        label_visibility="collapsed",
        help="Upload any PDF book or document to start asking questions"
    )

    # Warn if a DB already exists and a NEW file is chosen
    db_exists = os.path.exists("chroma_db")
    if uploaded_file and db_exists:
        existing_name = st.session_state.doc_name or "another document"
        if uploaded_file.name != existing_name:
            st.markdown(f"""
            <div class="warn-box">
                ⚠️ A database for <b>{existing_name}</b> already exists.<br>
                Click <b>Clear Database</b> below before processing a new book,
                otherwise both books' data will be mixed together.
            </div>
            """, unsafe_allow_html=True)

    if uploaded_file:
        if st.button("📥  Process Document", use_container_width=True):
            with st.spinner("Reading & indexing document…"):
                try:
                    from langchain_community.document_loaders import PyPDFLoader
                    from langchain_text_splitters import RecursiveCharacterTextSplitter
                    from langchain_mistralai import MistralAIEmbeddings
                    from langchain_community.vectorstores import Chroma

                    # Save upload to a temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = tmp.name

                    # ── create_database.py logic ──────────────────────────────
                    loader = PyPDFLoader(tmp_path)
                    docs   = loader.load()

                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )
                    chunks = splitter.split_documents(docs)

                    embedding_model = MistralAIEmbeddings()

                    vectorstore = Chroma.from_documents(
                        documents=chunks,
                        embedding=embedding_model,
                        persist_directory="chroma_db"
                    )
                    # ─────────────────────────────────────────────────────────

                    st.session_state.vectorstore = vectorstore
                    st.session_state.doc_name    = uploaded_file.name
                    st.session_state.messages    = []
                    os.unlink(tmp_path)
                    st.success(f"✓ Indexed {len(chunks)} chunks from '{uploaded_file.name}'")

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # ── Active document ────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">Active Document</div>', unsafe_allow_html=True)
    if st.session_state.doc_name:
        st.markdown(f"""
        <div style="background:#1a1a24; border:1px solid #2e2e42; border-radius:8px;
                    padding:0.7rem 0.9rem; font-size:0.82rem; color:#a78bfa;">
            📄 {st.session_state.doc_name}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#16161d; border:1px dashed #2a2a35; border-radius:8px;
                    padding:0.7rem 0.9rem; font-size:0.8rem; color:#3d3d52; text-align:center;">
            No document loaded
        </div>
        """, unsafe_allow_html=True)

    # ── Retrieval settings ─────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">Retrieval Settings</div>', unsafe_allow_html=True)
    k_docs    = st.slider("Chunks to retrieve (k)", 2, 8, 4)
    diversity = st.slider("Diversity (MMR λ)", 0.0, 1.0, 0.5, 0.1,
                          help="0 = more diverse results · 1 = more relevant results")

    # ── Session controls ───────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">Session</div>', unsafe_allow_html=True)
    if st.session_state.messages:
        if st.button("🗑  Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # ── Database controls ──────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">Database</div>', unsafe_allow_html=True)

    db_exists = os.path.exists("chroma_db")
    st.markdown(f"""
    <div style="background:#16161d; border:1px solid #2a2a35; border-radius:8px;
                padding:0.6rem 0.9rem; font-size:0.78rem; color:#5a5a6e; margin-bottom:0.6rem;">
        Status: <span style="color:{'#34d399' if db_exists else '#ef4444'};">
        {'● Exists on disk' if db_exists else '● Not found'}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
    if st.button("🗑  Clear Database", use_container_width=True):
        if os.path.exists("chroma_db"):
            shutil.rmtree("chroma_db")
        st.session_state.vectorstore = None
        st.session_state.doc_name    = None
        st.session_state.messages    = []
        st.session_state.show_cleared_msg = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.show_cleared_msg:
        st.success("✓ Database cleared! Upload a new document.")
        st.session_state.show_cleared_msg = False


# ── Main ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">Ask your document</div>
    <div class="hero-sub">Upload a PDF, then ask anything — answers come only from the document.</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.vectorstore:
    st.markdown(f"""
    <div class="status-pill">
        <span class="dot-green"></span>
        Ready · {st.session_state.doc_name}
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="status-pill">
        <span class="dot-yellow"></span>
        No document loaded — upload a PDF in the sidebar
    </div>
    """, unsafe_allow_html=True)


# ── Chat history ───────────────────────────────────────────────────────────────
chat_html = '<div class="chat-container">'

if not st.session_state.messages:
    chat_html += """
    <div class="empty-state">
        <div class="empty-icon">💬</div>
        <div class="empty-text">No conversation yet.<br>Upload a PDF and ask your first question.</div>
    </div>
    """
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f"""
            <div style="display:flex; justify-content:flex-end;">
                <div class="bubble-user">
                    <div class="bubble-label">You</div>
                    {msg["content"]}
                </div>
            </div>
            """
        else:
            sources_html = ""
            if msg.get("sources"):
                chips = "".join(
                    f'<span class="source-chip">p.{s}</span>'
                    for s in msg["sources"]
                )
                sources_html = f'<div class="source-strip">{chips}</div>'
            chat_html += f"""
            <div style="display:flex; justify-content:flex-start;">
                <div class="bubble-ai">
                    <div class="bubble-label">DocMind</div>
                    {msg["content"]}
                    {sources_html}
                </div>
            </div>
            """

chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)


# ── Input ──────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([6, 1])
with col1:
    query = st.text_input(
        "question",
        placeholder="Ask a question about your document…",
        label_visibility="collapsed",
        key="query_input"
    )
with col2:
    send = st.button("Send →", use_container_width=True)


# ── Inference (main.py logic) ──────────────────────────────────────────────────
if send and query.strip():
    if not st.session_state.vectorstore:
        st.warning("Please upload and process a PDF first.")
    else:
        st.session_state.messages.append({"role": "user", "content": query})

        with st.spinner("Thinking…"):
            try:
                from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
                from langchain_community.vectorstores import Chroma
                from langchain_core.prompts import ChatPromptTemplate

                # ── main.py logic ─────────────────────────────────────────────
                retriever = st.session_state.vectorstore.as_retriever(
                    search_type="mmr",
                    search_kwargs={
                        "k": k_docs,
                        "fetch_k": k_docs * 3,
                        "lambda_mult": diversity
                    }
                )

                retrieved_docs = retriever.invoke(query)

                context = "\n\n".join([doc.page_content for doc in retrieved_docs])
                pages   = sorted(set(
                    doc.metadata.get("page", "?") + 1
                    for doc in retrieved_docs
                    if isinstance(doc.metadata.get("page"), int)
                ))

                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a helpful AI assistant.
Use ONLY the provided context to answer the question.
If the answer is not present in the context,
say: "I could not find the answer in the document." """),
                    ("human", "Context:\n{context}\n\nQuestion:\n{question}")
                ])

                llm = ChatMistralAI(model="mistral-small-2506")

                final_prompt = prompt.invoke({"context": context, "question": query})
                response     = llm.invoke(final_prompt)
                # ─────────────────────────────────────────────────────────────

                st.session_state.messages.append({
                    "role":    "assistant",
                    "content": response.content,
                    "sources": pages
                })

            except Exception as e:
                st.session_state.messages.append({
                    "role":    "assistant",
                    "content": f"⚠ Error: {str(e)}",
                    "sources": []
                })

        st.rerun()