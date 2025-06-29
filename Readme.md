# FinSage: AI-Driven Loan Management and Financial Advisory System

**FinSage** - An AI powered is a web application designed to assist users with loan consultations, application guidance, legal term explanations, and financial goal planning. It  is a digital financial advisor designed to make complex financial decisions easier, faster for individuals to achieve their goals.FinSage helps users understand their desired loan options by analyzing their details and offering personalized loan recommendations that best match their needs and eligibility.<br>

## Features
- **Loan Consultation**: Provides personalized loan recommendations based on user's income, credit score, loan type,and desired amount using LLaMA-3 model
- **Loan Application Assistant**: Parse financial summaries and receive actionable guidance for loan applications. 

   > From the user input (free text), the structured data is extracted using regex and LLM. ChromaDB retrieves relevant loan info (RAG), and LLaMA-3-8B generates guidance and highlights user's missing details for the loan application.

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
- Uses langchain_community for interacting with the LLaMA-3-8B model via Together API.
- Chromadb: Vector storage for RAG
- sentence-transformers: Text embeddings
- Python-dotenv: Environment variable management









