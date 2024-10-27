# Moodibot - a RAG-Based Chatbot

### Authors: Dana Mikulinsky, Nitzan Manor, Saar David

---

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) chatbot specifically designed to assist users with information related to their rights within the "Maccabi Health Services" organization. The chatbot integrates retrieval and generative capabilities to provide contextually accurate, relevant, and personalized responses. It leverages semantic chunking, Gemini embeddings, and MongoDB to manage data efficiently and track conversation history. The chatbot can adjust its interaction style, allowing it to cater to diverse audiences and adapt to different conversational tones.

## Prerequisites

Ensure you have the following versions installed:

- **Python**: Version 3.10 or higher
- **Node.js**: Version 21.7.1 or higher

## Setup Instructions

To get started with the project, follow these instructions to set up both the backend and frontend components.

### 1. Clone the Repository
```bash
git clone https://github.com/DanaMikulinsky/FinalProject.git
cd FinalProject
```

### 2. Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a Python virtual environment**:
   ```bash
   python3.10 -m venv moodibot_venv
   source moodibot_venv/bin/activate  # On Windows, use `moodibot_venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend application**:
   ```bash
   python app.py
   ```

### 3. Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd ../frontend
   ```

2. **Install the required npm packages**:
   ```bash
   npm install
   ```

3. **Start the frontend application**:
   ```bash
   npm start
   ```
