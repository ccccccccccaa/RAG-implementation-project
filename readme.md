# RMIT Policy Assistant Chatbot

## 1. Overview

Welcome to the **RMIT Policy Assistant**! This chatbot helps you find, understand, and comprehend official RMIT policies using a **local Retrieval Augmented Generation (RAG)** approach.

### Key Components

- **Knowledge Base:**  
  Built from RMIT policy documents in Markdown (`.md`) format located in the `<rmit_markdown_content>` folder.

- **Local Embeddings & Search:**  
  Uses [sentence-transformers](https://www.sbert.net/) to create text embeddings locally and FAISS for efficient similarity search to find relevant policy sections.

- **LLM Generation:**  
  Utilizes **AWS Bedrock** with the Anthropic Claude 3 Haiku model (`anthropic.claude-3-haiku-20240307-v1:0`) to generate answers based on user questions and the retrieved policy context.

### Project Files

- `build_index.py`:  
  Offline script to process Markdown files and build the local knowledge base index.  
  **Note:** Latest Markdown files are already processed and stored as:  
  `rmit_policies_local.faiss_index` and `rmit_policy_chunks_local.json`

- `app.py`:  
  Main Streamlit web app providing the interactive chat interface.

---

## 2. Prerequisites

- **Python:** Version 3.11 or above  
- **PIP:** Python package installer  
- **AWS Account & Credentials:** For `app.py` to call AWS Bedrock  
- **AWS Bedrock Access:** For Anthropic Claude 3 model  
- **Cognito User Pool Credentials:**  
  We have already provided in the code
- **RMIT Policy Markdown Documents:**  
  Collection of crawled RMIT policies as `.md` files in `<rmit_markdown_content>`  
- **Internet Connection:**  
  - For the first run of `build_index.py` (to download sentence-transformers model)  
  - For `app.py` to communicate with AWS Bedrock  

---

## 3. Setup Instructions

### Step 3.1: Get Project Files

Ensure you have `app.py` and `build_index.py` scripts.

---

### Step 3.2: Install Python Libraries

Run the following command in your terminal:

```bash
pip install streamlit boto3 faiss-cpu sentence-transformers numpy PyPDF2 pandas
```

### Step 3.3: Configure AWS Credentials (for app.py)
Update the AWS Cognito and Bedrock configuration in app.py with your credentials:

REGION = "us-east-1"
LLM_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

IDENTITY_POOL_ID = "YOUR_IDENTITY_POOL_ID"
USER_POOL_ID = "YOUR_USER_POOL_ID"
APP_CLIENT_ID = "YOUR_APP_CLIENT_ID"
USERNAME = "YOUR_COGNITO_USERNAME"
PASSWORD = "YOUR_COGNITO_PASSWORD"

Note:
Credentials may already be preset; change if necessary.
build_index.py does not require these AWS credentials.

### Step 3.4: Prepare RMIT Policy Markdown Files
Only required if you have updated or new Markdown files.
Otherwise, skip this step and proceed to Step 4.

Create a folder (e.g., policy_markdowns) in your project directory.

Place all .md policy documents into this folder.

### Step 3.5: Build Local Knowledge Base (Offline Indexing)
Open build_index.py.

Set markdown_dir variable to your Markdown folder path, e.g.:

``` bash
if __name__ == "__main__":
    markdown_dir = "policy_markdowns"
Run the script in your terminal:
```
```bash
python build_index.py
``` 

This will download the embedding model (first run only) and generate:

rmit_policies_local.faiss_index

rmit_policy_chunks_local.json

### Step 3.6: Verify Knowledge Base Files
Make sure rmit_policies_local.faiss_index and rmit_policy_chunks_local.json are in the same directory as app.py.

## 4. Running the RMIT Policy Assistant Chatbot
Open your terminal and navigate to the project directory.

cd path/to/Assignment3_Chatbot_Python
(Recommended) Create and activate a Python virtual environment:

### Windows:

``` bash
python -m venv .venv
.\.venv\Scripts\activate
```
### macOS/Linux:

``` bash
python3 -m venv .venv
source .venv/bin/activate
``` 

Launch the Streamlit app:
``` bash
streamlit run app.py
``` 

Your default web browser should open at http://localhost:8501 with the chatbot UI.

## 5. Features Overview
### Session Management:
Create and select chat sessions; each session’s conversation history is saved in a local SQLite database for persistence.

### Local RAG Pipeline:
User queries are embedded locally, relevant policy chunks retrieved via FAISS, then passed with conversation context to AWS Bedrock LLM for answer generation.

### Responsible AI Rules:
The system strictly answers based on retrieved policy content only, refuses out-of-scope questions, filters inappropriate content, and provides disclaimers transparently.

### Chat Interface:
Streamlit chat UI with continuous conversation display and controls to clear history and start new sessions.

### Sidebar Status Panel:
Shows loading status for embedding model and knowledge base, current session ID, and session controls.

## 6. How to Update the Knowledge Base
If you need to update your knowledge base with newer policy documents:
1. Crawl or download updated Markdown .md files into your local folder.
2. Run build_index.py again to re-generate the FAISS index and chunk files.
3. Replace the old .faiss_index and .json files with the new ones in your project directory.
4. Restart the chatbot app to load the new knowledge base.

## 7. Using the Chatbot

Ask Questions:
Enter your queries in the chat input box about RMIT policies.

Contextual Responses:
The assistant uses local policy documents and your chat history to generate accurate, context-aware answers.

Session Control:
Manage chat sessions and conversation history in the sidebar.

Clear History:
Use the sidebar button to clear current session history and start fresh.

## 8. Troubleshooting
StreamlitSetPageConfigMustBeFirstCommandError:
Ensure st.set_page_config() is the very first Streamlit command in app.py.

Knowledge Base Files Missing:
Run build_index.py successfully and confirm output files are in the same directory as app.py.

Markdown Files Not Found in build_index.py:
Verify the path set in markdown_dir and ensure Markdown files exist there.

AWS Authentication Errors:
Check your Cognito credentials and ensure the assigned IAM role has the correct Bedrock invoke permissions.

Embedding Model Loading Errors:
Ensure internet connection during first run and verify the LOCAL_EMBEDDING_MODEL_NAME is correct.

## 9. Key Project Files
app.py: Streamlit chatbot application

build_index.py: Offline script to build local FAISS knowledge base

rmit_markdown_content/: Folder containing .md policy files (input)

rmit_policies_local.faiss_index: FAISS index file (generated)

rmit_policy_chunks_local.json: Policy chunk metadata file (generated)

## 10. Credits & Notes
Uses sentence-transformers and FAISS for efficient local semantic search.

Powered by AWS Bedrock and Anthropic Claude 3 Haiku for LLM generation.

Includes responsible AI safeguards with filtering, disclaimers, and session persistence.

Designed and developed as part of the RMIT University course assignment project (Assignment 3).

Good luck with your RMIT Policy Assistant!
If you need further assistance, contact us at s3825008@student.rmit.edu.au 