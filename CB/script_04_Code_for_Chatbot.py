import os 
import re
import faiss
import pickle
import base64
import numpy as np 
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt 
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
##########################################################
########################################################## 
Data = pd.read_excel("Translated_Data_all.xlsx") 

## Creating Iput document 
documents = []
for _, row in Data.iterrows():
    doc = f"""
    Assembly: {row['assembly']}
    Component: {row['component']}
    Action: {row['action']}
    Description: {row['Translated Text']}
    """
    documents.append(doc.strip()) 
########################################################## 
########################################################## 
## Indexing the documents 
## Load embedding model
embedder = SentenceTransformer("Text_MiniLM_L6_v2") 
## Embed the documents
document_embeddings = embedder.encode(documents)
#### Create FAISS index
dimension = document_embeddings.shape[1]
index     = faiss.IndexFlatL2(dimension)
index.add(document_embeddings) 

with open("docs.pkl", "wb") as f:
    pickle.dump(documents, f)
faiss.write_index(index, "faiss_index.index") 
########################################################## 
##########################################################
## Loading the transformer : llama-3.2-1B

model_path = "Llama_3p2_1B"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model     = AutoModelForCausalLM.from_pretrained(model_path) 
########################################################## 
########################################################## 
## RAG Loop Building 
def ask_rag(query):
    # Embed query
    query_embedding = embedder.encode([query])
    
    # Retrieve top-k docs
    D, I = index.search(np.array(query_embedding), k=5)
    retrieved_docs = [documents[i] for i in I[0]]
    
    # Combine retrieved context with user question
    context = "\n\n".join(retrieved_docs)
    prompt = f"""ZF-Maintenance Chatbot. Based on the following context, answer the query.
    
    Context:
    {context}
    
    Query: {query}
    Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=300)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
########################################################## 
##########################################################
def Output_Formattor(R):
    print("##############################")
    components1  = re.findall(r"Component:\s*(.*)", R) 
    Assembly1    = re.findall(r"Assembly:\s*(.*)", R) 
    action1      = re.findall(r"Action:\s*(.*)", R)
    Description1 = re.findall(r"Description:\s*(.*)", R) 

    
    unique_components = sorted(set(components1))
    unique_Assembly = sorted(set(Assembly1)) 
    unique_action = sorted(set(action1))  
    unique_Description = sorted(set(Description1))
    print("The Possible Components")
    print(unique_components) 
    print("The possible Assembly lines :") 
    print(unique_Assembly) 
    print("The Suggested Action :") 
    print(unique_action)
    print("##############################")


########################################################## 
##########################################################
#### ChatBot
Flag = True 

while Flag:
    msg = input("Type something (or 'quit' to stop): ")
    response = ask_rag(str(msg))
    Output_Formattor(response) 
    if msg == "quit":
        Flag = False

########################################################## 
########################################################## 