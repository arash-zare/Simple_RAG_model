import os
from pypdf import PdfReader
import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

client = OpenAI(base_url=base_url, api_key=api_key)

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="pdf_knowledge_base")

PDF_PATH = 'Arash_Zare_resume3.pdf'

def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    reader = PdfReader(pdf_path)
    pages_data = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            pages_data.append({"page": page_num, "text": text})
    return pages_data


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
    return chunks



if __name__ == "__main__":
    
    if os.path.exists(PDF_PATH):
        print(f"Reading {PDF_PATH}...")
        pdf_pages = extract_text_from_pdf(PDF_PATH)

        documents = []
        metadatas = []
        ids = []

        doc_counter = 0
        for page in pdf_pages:
            # تکه‌تکه کردن متن صفحه
            chunks = chunk_text(page["text"], chunk_size=80, overlap=15)
            for chunk in chunks:
                documents.append(chunk)
                metadatas.append({"page": page["page"]})
                ids.append(f"doc_{doc_counter}")
                doc_counter += 1
        # ذخیره یک‌جای تمام چانک‌ها در ChromaDB
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(documents)
        print(f"Successfully ingested {len(documents)} chunks from PDF into ChromaDB!\n")
    else:
        print(f"Error: {PDF_PATH} not found in the current directory.")
        exit(1)


        
print(f"Successfully ingested {len(documents)} chunks from PDF.")
print("=" * 50)
print("Arash Zare AI Assistant is Ready!")
print("Type 'exit' to quit.")
print("=" * 50)

while True:
    user_query = input("\nAsk a question: ").strip()

    if user_query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    if not user_query:
        continue

    # جستجو در ChromaDB
    results = collection.query(
        query_texts=[user_query],
        n_results=min(3, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    retrieved_docs = results.get("documents", [[]])[0]
    retrieved_meta = results.get("metadatas", [[]])[0]

    if not retrieved_docs:
        print("No relevant information found.")
        continue

    # ساخت Context
    context_parts = []

    for doc, metadata in zip(retrieved_docs, retrieved_meta):
        page_number = metadata.get("page", "Unknown")
        context_parts.append(
            f"[Page {page_number}]\n{doc}"
        )

    context = "\n\n---\n\n".join(context_parts)

    print("\nRetrieved Context:")
    print(context)
    print("-" * 50)



    system_prompt = f"""
You are an assistant answering questions about Arash Zare.

Use only the information inside the context below.
If the answer is not available in the context, say:
"I don't have enough information in the document."

Answer clearly and concisely.

Context:
{context}
"""
    # اتصال به OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": user_query
            }
        ],
        temperature=0.2
    )

    print("\nAI Response:")
    print(response.choices[0].message.content)
    print("=" * 50)
