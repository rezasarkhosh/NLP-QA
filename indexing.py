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
    
    return relevant_docs


def generate_answer(question, relevant_docs):
    # Combine relevant documents into a context string
    context = " ".join(relevant_docs)
    
    # Ensure the input contains both question and context
    input_text = f"question: {question} context: {context}"
    
    # Generate an answer with beam search for better results
    answer = generator(input_text, max_length=500, num_return_sequences=1, num_beams=5, early_stopping=True)
    
    return answer[0]['generated_text']


# Switching to a larger model or using beam search
generator = pipeline("text2text-generation", model="t5-large")

# Example question
question = "What is the market outlook for Ethereum after the upcoming elections?"

# Retrieve relevant documents from the FAISS index
relevant_docs = retrieve_relevant_docs(question, top_k=5)

# Display the retrieved relevant documents
print("Relevant Documents:", relevant_docs)

# Generate an answer based on the retrieved documents with beam search
answer = generate_answer(question, relevant_docs)
print(f"Q: {question}\nA: {answer}")
