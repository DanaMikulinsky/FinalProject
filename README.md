# Moodibot - a RAG-Based Chatbot

### Authors: Dana Mikulinsky, Nitzan Manor, Saar David

---

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) chatbot designed to assist users with information related to their rights within the "Maccabi Health Services" organization. The chatbot integrates retrieval and generative capabilities to provide contextually accurate, relevant, and personalized responses. It leverages semantic chunking, Gemini embeddings, and MongoDB to manage data efficiently and track conversation history. The chatbot can adjust its interaction style to cater to diverse audiences and adapt to different conversational tones.
**Please Note** that this is an installation guide for a local machine. You can also accsess partial chatbot abilities by using the "chat_no_ui" Jupyter Notebbok.

## Prerequisites

Ensure you have the following versions installed:

- **Python**: Version 3.10 or higher
- **Node.js**: Version 21.7.1 or higher

### Check for Python and Node.js

To confirm that Python and Node.js are installed and meet the version requirements, run the following commands in your terminal:

```bash
python3 --version  # or python --version
node --version
```

If you do not have these installed or your versions are lower than required, download and install the latest versions from the official sites:

- [Download Python](https://www.python.org/downloads/)
- [Download Node.js](https://nodejs.org/)

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

1. **Open a new terminal window**:  
   Keep the backend running in its terminal and open a separate terminal window for the frontend.

2. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

3. **Install the required npm packages**:
   ```bash
   npm install
   ```

4. **Start the frontend application**:
   ```bash
   npm start
   ```

---

Your backend should now be running on its own terminal, with the frontend running in a separate terminal window. You are ready to start using Moodibot!
