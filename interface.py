import streamlit as st
import google.generativeai as genai
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# --- Setup ---
PINECONE_KEY = "pcsk_5ctgLG_BS2s3B5TUmrExjq6MsbiQkUokQek3U7huDCj5iwFVyqsVBgKPr3Sd47Rut1Wg1P"
GEMINI_KEY = "AIzaSyDiPVi7_OMLuHD-Csg7YcsH9Zd_GSHTyeA"

pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index("news-index")
genai.configure(api_key=GEMINI_KEY)
llm = genai.GenerativeModel('gemini-2.5-flash')
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# --- UI Layout ---
st.set_page_config(page_title="Tech News AI", page_icon="🤖")
st.title("🤖 Tech Layoff Smart Analyzer")
st.markdown("Ask me anything about the latest tech news from our database.")

query = st.text_input("Enter your question:", placeholder="e.g. Is there any news about Google?")

if st.button("Ask AI"):
    if query:
        with st.spinner("Searching database..."):
            # RAG Logic
            query_vector = embed_model.encode(query).tolist()
            results = index.query(vector=query_vector, top_k=2, include_metadata=True)
            
            context = ""
            for match in results['matches']:
                context += f"\nTitle: {match['metadata']['title']}\nLink: {match['metadata']['url']}\n"
            
            prompt = f"Context: {context}\n\nUser Question: {query}\n\nAnswer clearly:"
            response = llm.generate_content(prompt)
            
            st.subheader("AI Answer:")
            st.write(response.text)
            
            with st.expander("See Sources (From Pinecone)"):
                st.write(context)
    else:
        st.warning("Please enter a question first!")