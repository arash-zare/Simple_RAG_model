# Arash Zare AI Assistant (RAG System)

A Retrieval-Augmented Generation (RAG) system designed to provide accurate, context-aware answers about Arash Zare's professional background, skills, and projects using his resume and portfolio data.

## Features
- **Semantic Search:** Uses Vector Embeddings (ChromaDB) to understand the *meaning* behind questions, not just keywords.
- **Context-Aware:** Limits AI hallucinations by forcing the model to answer based only on provided professional data.
- **Modular Data Loading:** Easily switch between hardcoded documents, web scraping, or file-based ingestion.
- **Tech Stack:** Python, OpenAI API (GPT-4o), ChromaDB.

## Prerequisites
- Python 3.9+
- OpenAI API Key
- `pip` installed

## Installation

1. **Clone the repository** (or create a project folder):
```bash
   mkdir arash-ai-assistant
   cd arash-ai-assistant
   
