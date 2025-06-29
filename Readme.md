# FinSage: AI-Driven Loan Management and Financial Advisory System

**FinSage** - An AI powered web application is designed to assist users with loan consultations, application guidance, legal term explanations, and financial goal planning. <br>

## Features
- **Loan Consultation**: Provides personalized loan recommendations based on user's income, credit score, loan type,and desired amount using LLaMA-3 model
- **Loan Application Assistant**: Parse financial summaries and receive actionable guidance for loan applications. 

   > From the user input (free text) structured data extracted using regex and LLM. ChromaDB retrieves relevant loan info (RAG), and LLaMA-3-8B generates guidance along highlighting missing details of the user required for loan application.

- **Financial Goals Tracker**: Generate savings plans based on income, expenses, savings, and user-defined financial goals.
   > LangChain processes the input with a prompt template, and LLaMA-3-8B generates a markdown-formatted savings plan.

- **Legal Term Explanation**: Understand complex loan clauses entered by user in simple, beginner-friendly language. LLaMA generates a clear explanation and implications in markdown



## Tech Stack
- **Frontend**: Streamlit
- **Backend**: LangChain, Together API (LLaMA-3-8B), ChromaDB, Sentence Transformers
- **Programming Language**: Python 3.8+
- **External Services**: Together API for LLM, ChromaDB for vector storage

## Installation & Configuration
- Set up virtual environment (optional)
- Install the reqired dependencies 
- Obtain a Together API key for accessing the LLaMA-3-8B model. Store it in .env file
- Prepare Loan Data: Ensure a loan_data.json file exists in the project root with loan-related data

## Dependencies
Uses langchain_community for interacting with the LLaMA-3-8B model via Together API.<br>
chromadb: Vector storage for RAG<br>
sentence-transformers: Text embeddings
<br>
Loads environment variables (e.g., TOGETHER_API_KEY) using dotenv.<br>
python-dotenv: Environment variable management









