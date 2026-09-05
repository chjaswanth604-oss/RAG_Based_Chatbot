# RAG-Based College Information Chatbot

## Project Specification

## 1. Project Overview

Build a full-stack web application called:

**AI-Powered College Information Assistant using RAG**

The application will allow college students to ask questions about their college.

The chatbot must answer questions using information stored in uploaded college documents such as:

* Academic regulations
* Admission information
* Course details
* Fee structure
* Examination information
* Academic calendar
* Hostel rules
* Library information
* Placement information
* Scholarship information
* College policies
* Clubs and events
* Department information

The project MUST use a real **Retrieval-Augmented Generation (RAG)** pipeline.

A simple chatbot connected directly to an LLM is NOT acceptable.

---

# 2. Main Objective

The system should work like this:

Student Question

↓

Convert question into embedding

↓

Search college documents in vector database

↓

Retrieve relevant document chunks

↓

Send retrieved information to LLM

↓

Generate answer based on retrieved information

↓

Display answer

↓

Display source document and page number

---

# 3. Technology Stack

Use the following technologies.

### Frontend

* React.js
* Vite
* Tailwind CSS

### Backend

* Python
* FastAPI

### AI

* Groq API for LLM
* Sentence Transformers for embeddings

The code should make the LLM provider configurable using environment variables.

### Vector Database

Use:

* ChromaDB

### Database

Use:

* MongoDB

MongoDB should store:

* Users
* Chat history
* Document metadata
* Feedback

### PDF Processing

Use:

* PyMuPDF

---

# 4. User Roles

There must be two roles.

## Student

Students can:

* Register
* Login
* Ask questions
* View answers
* View source documents
* View chat history
* Delete their chat history
* Give thumbs-up/thumbs-down feedback

Students MUST NOT be able to upload or delete documents.

## Admin

Admins can:

* Login
* View dashboard
* Upload documents
* View documents
* Delete documents
* Replace/update documents
* View document processing status
* View basic chatbot usage statistics

---

# 5. Authentication

Implement secure authentication.

Required:

* Register
* Login
* Logout
* JWT authentication
* Password hashing
* Role-based authorization

User database fields:

```text
_id
name
email
password_hash
role
created_at
```

Roles:

```text
student
admin
```

Do not store plain-text passwords.

---

# 6. Student Chat Interface

Create a modern chatbot interface.

The interface should contain:

### Left sidebar

* New Chat
* Chat History
* User profile
* Logout

### Main area

Display:

* Welcome message
* Chat messages
* Input box
* Send button
* Loading indicator

Example:

```text
------------------------------------------------
| Chat History | College AI Assistant          |
|              |                               |
| New Chat     | AI: Hello! How can I help?   |
|              |                               |
| Previous     | You: What is the attendance   |
| chats        | requirement?                  |
|              |                               |
|              | AI: The minimum attendance   |
|              | requirement is 75%.          |
|              |                               |
|              | Source: Academic Rules.pdf  |
|              | Page 23                       |
|              |                               |
|              | [ Ask your question... ]      |
------------------------------------------------
```

---

# 7. RAG DOCUMENT PROCESSING

This is the MOST IMPORTANT part of the project.

When an admin uploads a PDF:

```text
PDF Upload
    ↓
Extract Text
    ↓
Clean Text
    ↓
Split Text into Chunks
    ↓
Generate Embeddings
    ↓
Store Embeddings in ChromaDB
    ↓
Store Document Metadata in MongoDB
```

Do NOT skip any step.

---

# 8. PDF Text Extraction

Use PyMuPDF.

For every page:

* Extract text
* Keep page number
* Clean unnecessary whitespace
* Ignore empty pages

Store metadata for every chunk.

Example:

```json
{
  "document_name": "Academic_Regulations.pdf",
  "page_number": 23,
  "department": "General",
  "chunk_id": "abc123"
}
```

---

# 9. Text Chunking

Split documents into smaller chunks.

Recommended:

* Chunk size: approximately 500–800 words
* Overlap: approximately 100 words

Make chunk size configurable.

Each chunk must retain:

* Document name
* Page number
* Department
* Document ID

---

# 10. Embedding Generation

Use Sentence Transformers.

Recommended model:

```text
all-MiniLM-L6-v2
```

Generate an embedding for every document chunk.

Example:

```text
Document chunk
      ↓
Sentence Transformer
      ↓
Embedding vector
      ↓
ChromaDB
```

---

# 11. ChromaDB

Use ChromaDB as the vector database.

Store:

```text
embedding
document chunk
document ID
document name
page number
department
```

Create a collection for the college knowledge base.

The system must perform semantic similarity search.

---

# 12. Question Processing

When the student asks:

> What is the minimum attendance required?

Process the question:

```text
Question
 ↓
Embedding
 ↓
ChromaDB similarity search
 ↓
Retrieve top relevant chunks
```

Retrieve approximately the top 3–5 relevant chunks.

The number should be configurable.

---

# 13. RAG Prompt

Send the retrieved information to the LLM.

Use a prompt similar to:

```text
You are an AI College Information Assistant.

Answer the student's question using ONLY the
provided college knowledge base.

Do not invent information.

If the answer cannot be found in the provided
context, clearly tell the student that the
information is not available in the college
knowledge base.

Always provide a concise and useful answer.

Retrieved Context:
{context}

Student Question:
{question}
```

The LLM must NOT be allowed to freely answer college-related questions without retrieved context.

---

# 14. Unknown Question Handling

This is mandatory.

If the required information is not found in the knowledge base, respond with something like:

> "I couldn't find this information in the college knowledge base. Please contact the concerned college department for accurate information."

Do NOT hallucinate an answer.

Example:

Student:

> What is the current stock price of Apple?

The chatbot should not try to answer because this is outside the college knowledge base.

---

# 15. Source References

Every RAG answer should show the sources used.

Example:

```text
Answer:

Students must maintain at least 75% attendance
to be eligible for the semester examination.

Sources:

📄 Academic Regulations.pdf
Page 23
```

If multiple sources are used:

```text
Sources:

📄 Academic Regulations.pdf - Page 23
📄 Examination Guidelines.pdf - Page 7
```

Source information must come from the retrieved chunks.

---

# 16. Relevance Score

Show a simple relevance/confidence indicator.

Example:

```text
Source Relevance: 92%
```

Do not claim that this is mathematically equivalent to LLM confidence.

It should represent the retrieval similarity score.

If the similarity is too low, treat the question as unanswered.

Make the threshold configurable.

Example:

```text
SIMILARITY_THRESHOLD=0.35
```

---

# 17. Chat History

Store conversations in MongoDB.

Each chat message should contain:

```text
_id
user_id
question
answer
sources
created_at
```

Students should be able to:

* View previous conversations
* Open previous conversation
* Start a new conversation
* Delete conversation

---

# 18. Admin Dashboard

Create an admin dashboard.

Display:

```text
-------------------------------------
Admin Dashboard
-------------------------------------

Total Documents: 25

Total Students: 450

Total Questions: 1240

Documents Processed: 23

Processing Failed: 2
-------------------------------------
```

Also provide:

```text
Upload Document
View Documents
Delete Document
Update Document
```

---

# 19. Document Management

Admin document page should display:

```text
Document Name
Department
Upload Date
Number of Pages
Processing Status
Actions
```

Example:

```text
Academic_Regulations.pdf
General
29 Pages
Processed
[Delete] [Replace]
```

Processing status:

```text
Processing
Processed
Failed
```

---

# 20. Department-wise Knowledge Base

Add support for departments.

Example departments:

```text
Computer Science
Electrical Engineering
Mechanical Engineering
Civil Engineering
Electronics
General
```

During document upload, admin selects the department.

Example:

```text
Upload Document

File: [ Academic_Rules.pdf ]

Department:
[ Electrical Engineering ▼ ]

[ Upload ]
```

Students can ask:

> What are the electrical engineering lab requirements?

The system should retrieve relevant documents.

---

# 21. Suggested Questions

On the chatbot home screen, show suggested questions.

Example:

```text
Suggested Questions

• What is the minimum attendance requirement?
• When are the semester examinations?
• What are the hostel timings?
• What scholarships are available?
• How can I apply for placements?
• What are the library timings?
```

Clicking a suggested question should automatically place it into the chat.

---

# 22. Feedback

After every answer display:

```text
Was this answer helpful?

👍   👎
```

Store feedback in MongoDB.

Fields:

```text
user_id
question
answer
feedback
created_at
```

---

# 23. API Structure

Create FastAPI endpoints.

### Authentication

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Chat

```text
POST /api/chat
GET  /api/chat/history
GET  /api/chat/{chat_id}
DELETE /api/chat/{chat_id}
```

### Documents

```text
POST /api/documents/upload
GET  /api/documents
DELETE /api/documents/{id}
PUT /api/documents/{id}
```

Only admins can access document management endpoints.

### Feedback

```text
POST /api/feedback
```

### Admin

```text
GET /api/admin/stats
```

---

# 24. Backend Architecture

Use a clean structure.

```text
backend/
│
├── main.py
│
├── routes/
│   ├── auth.py
│   ├── chat.py
│   ├── documents.py
│   ├── feedback.py
│   └── admin.py
│
├── services/
│   ├── rag_service.py
│   ├── embedding_service.py
│   ├── document_service.py
│   ├── vector_service.py
│   └── llm_service.py
│
├── database/
│   ├── mongodb.py
│   └── chromadb.py
│
├── models/
│   ├── user.py
│   ├── chat.py
│   └── document.py
│
├── middleware/
│   └── auth.py
│
├── utils/
│   └── security.py
│
├── uploads/
│
├── requirements.txt
└── .env.example
```

---

# 25. Frontend Architecture

Use:

```text
frontend/
│
├── src/
│
├── components/
│   ├── ChatWindow.jsx
│   ├── ChatMessage.jsx
│   ├── Sidebar.jsx
│   ├── SourceCard.jsx
│   └── Loading.jsx
│
├── pages/
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Chat.jsx
│   ├── AdminDashboard.jsx
│   └── Documents.jsx
│
├── services/
│   └── api.js
│
├── context/
│   └── AuthContext.jsx
│
├── App.jsx
└── main.jsx
```

---

# 26. UI Design

Make the interface modern and professional.

Requirements:

* Responsive design
* Clean dashboard
* Modern chatbot interface
* Mobile-friendly
* Loading animations
* Error messages
* Empty states
* Toast notifications
* Dark/light mode if practical

Do NOT make the interface overly complicated.

The chatbot should be the main focus.

---

# 27. Security

Implement:

* Password hashing
* JWT authentication
* Protected API routes
* Role-based access
* File type validation
* File size validation
* Environment variables for API keys
* Never expose API keys in frontend
* Validate uploaded documents

Allowed document types:

```text
PDF
DOCX
TXT
```

PDF should be implemented first.

---

# 28. Environment Variables

Create:

```text
.env.example
```

with:

```text
MONGO_URI=
JWT_SECRET=
GROQ_API_KEY=
CHROMA_DB_PATH=
EMBEDDING_MODEL=
SIMILARITY_THRESHOLD=
TOP_K=
```

Never commit actual API keys to GitHub.

---

# 29. Error Handling

The application should handle:

* Invalid login
* Duplicate registration
* Invalid document
* Empty PDF
* Failed PDF processing
* LLM API failure
* MongoDB connection failure
* ChromaDB failure
* No relevant documents found
* Network errors

Show user-friendly messages.

Do not expose stack traces to normal users.

---

# 30. Loading States

While processing a document:

```text
Uploading document...
Extracting text...
Creating chunks...
Generating embeddings...
Adding to knowledge base...
Completed!
```

While answering:

```text
Searching college knowledge base...
Generating answer...
```

---

# 31. Important RAG Requirement

The system MUST demonstrate that it is actually using RAG.

Provide a backend response containing:

```json
{
  "answer": "...",
  "sources": [
    {
      "document": "Academic Regulations.pdf",
      "page": 23,
      "score": 0.91
    }
  ]
}
```

The frontend should display the sources.

---

# 32. Sample Documents

Create a small sample knowledge base for testing.

Include sample documents containing:

```text
Academic Regulations
Fee Structure
Hostel Rules
Examination Rules
Library Rules
Placement Information
Scholarship Information
```

These can be simple sample PDFs/documents if official college documents are unavailable.

Clearly label them as demo/sample documents.

---

# 33. Testing

Test the following.

### Test 1

Question:

```text
What is the minimum attendance requirement?
```

Expected:

Relevant answer + source document.

### Test 2

Question:

```text
What are the hostel timings?
```

Expected:

Relevant hostel information + source.

### Test 3

Question:

```text
What is the fee for the course?
```

Expected:

Relevant fee document + source.

### Test 4

Question:

```text
What is the capital of France?
```

Expected:

```text
Information not available in the college knowledge base.
```

### Test 5

Upload a document and ask a question whose answer exists only in that document.

The chatbot MUST retrieve that document.

---

# 34. Deployment

The final application must be deployable.

Frontend:

```text
Vercel
```

Backend:

```text
Render
```

Database:

```text
MongoDB Atlas
```

The vector database should be configured so that it persists correctly in the deployed environment.

Do not assume local ChromaDB storage will automatically persist on a temporary deployment filesystem. Configure persistent storage or a suitable hosted vector database if necessary.

---

# 35. README

Create a detailed README.md containing:

```text
Project Overview
Features
Architecture
Technology Stack
RAG Pipeline
Installation
Environment Variables
How to Run Frontend
How to Run Backend
How to Upload Documents
How RAG Works
API Documentation
Testing
Deployment
Screenshots
Future Improvements
```

Also include a simple architecture diagram using Mermaid if useful.

---

# 36. Final RAG Flow

The final implementation MUST follow:

```text
                COLLEGE DOCUMENTS
                       |
                       ↓
                TEXT EXTRACTION
                       |
                       ↓
                    CHUNKING
                       |
                       ↓
                  EMBEDDINGS
                       |
                       ↓
                   CHROMADB
                       |
                       |
Student Question → EMBEDDING
                       |
                       ↓
               SIMILARITY SEARCH
                       |
                       ↓
              TOP RELEVANT CHUNKS
                       |
                       ↓
              CONTEXT + QUESTION
                       |
                       ↓
                     LLM
                       |
                       ↓
                  FINAL ANSWER
                       |
              ┌────────┴────────┐
              ↓                 ↓
          ANSWER             SOURCES
```

---

# 37. Development Instructions

Build the project incrementally.

Do NOT create fake functionality.

Do NOT use mock chatbot responses in the final application.

Do NOT connect the chatbot directly to the LLM without retrieval.

Do NOT skip the vector database.

Do NOT hardcode answers.

The chatbot must retrieve information from the uploaded documents.

First make the backend RAG pipeline work.

Then integrate authentication.

Then build the frontend.

Then integrate frontend and backend.

Then add admin features.

Finally test and deploy.

---

# 38. Definition of Done

The project is considered complete only when:

* [ ] Student registration works
* [ ] Student login works
* [ ] Admin login works
* [ ] Admin can upload PDF
* [ ] PDF text extraction works
* [ ] Text chunking works
* [ ] Embeddings are generated
* [ ] Embeddings are stored in ChromaDB
* [ ] Questions are converted to embeddings
* [ ] Similarity search works
* [ ] Relevant chunks are retrieved
* [ ] Retrieved chunks are sent to LLM
* [ ] LLM generates answer using retrieved context
* [ ] Sources are displayed
* [ ] Unknown questions are handled
* [ ] Chat history works
* [ ] Admin can delete documents
* [ ] Admin can replace documents
* [ ] Department-wise documents work
* [ ] Feedback works
* [ ] Admin dashboard works
* [ ] Frontend and backend are integrated
* [ ] Application is responsive
* [ ] Application can be deployed
* [ ] README is complete

---

# 39. Final Instruction to Antigravity

Build this project as a complete working application.

Before writing large amounts of code:

1. Create the project structure.
2. Implement the backend.
3. Test the RAG pipeline independently.
4. Implement authentication.
5. Implement document management.
6. Implement the frontend.
7. Connect frontend and backend.
8. Test all major features.
9. Fix errors.
10. Prepare the application for deployment.

At every stage, prefer **working, testable functionality** over placeholder code.

The most important requirement is:

**This MUST be a genuine RAG application using document retrieval + embeddings + vector database + LLM.**

Do not replace the RAG pipeline with a normal LLM chatbot.
