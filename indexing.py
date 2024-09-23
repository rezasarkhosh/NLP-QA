from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import pipeline


model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(texts):
    return model.encode(texts, convert_to_tensor=False)

btc_texts = open('data/BTC_normalized.txt').read().split("\n\n")
eth_texts = open('data/ETH_normalized.txt').read().split("\n\n")

btc_embeddings = get_embeddings(btc_texts)
eth_embeddings = get_embeddings(eth_texts)

btc_embeddings = np.array(btc_embeddings)
eth_embeddings = np.array(eth_embeddings)

all_embeddings = np.vstack((btc_embeddings, eth_embeddings))

dimension = all_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(all_embeddings)

print(f"Indexed {index.ntotal} documents!")


def retrieve_relevant_docs(question, top_k=5):
    # Generate embedding for the question
    question_embedding = model.encode([question], convert_to_tensor=False)
    
    # Search the index for the top_k most similar documents
    distances, indices = index.search(np.array(question_embedding), top_k)
    
    # Retrieve the matching documents
    relevant_docs = [btc_texts[i] if i < len(btc_texts) else eth_texts[i - len(btc_texts)] for i in indices[0]]
    
    # Filter the documents based on Ethereum and elections keywords
    keywords = ["Ethereum", "ETH", "election", "politics", "market outlook", "crypto"]
    filtered_docs = [doc for doc in relevant_docs if any(keyword.lower() in doc.lower() for keyword in keywords)]
    
    return filtered_docs

def generate_answer(question, relevant_docs):
    # Combine relevant documents into a context string
    context = " ".join(relevant_docs)
    
    # Ensure the input contains both question and context
    input_text = f"question: What is the market outlook for Ethereum after the elections? Explain why Ethereum's price might change, considering political and market conditions. Provide short-term and long-term expectations. context: {context}"
    
    # Generate multiple answers with beam search for better results
    answer = generator(input_text, max_length=500, num_return_sequences=3, num_beams=5, early_stopping=True)
    
    return answer


generator = pipeline("text2text-generation", model="t5-large")


question = "What is the market outlook for Ethereum after the upcoming elections?"


relevant_docs = retrieve_relevant_docs(question, top_k=5)


print("Relevant Documents:", relevant_docs)


answer = generate_answer(question, relevant_docs)
print(f"Q: {question}\nA: {answer}")
