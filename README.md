# AI Conversational Chatbot – Tech Stack Overview

This repository documents the architecture, technology stack, and request flow for an AI-powered conversational chatbot application. The system is designed to be modular, scalable, and production-ready, following a clean MVC-inspired architecture.

---

## System Overview

The chatbot enables real-time conversational interactions between users and a Large Language Model (LLM). It supports contextual memory, asynchronous communication, and future extensibility such as Retrieval Augmented Generation (RAG).

At a high level:

* The **frontend** provides a real-time chat interface.
* The **backend** orchestrates requests, manages conversation state, and communicates with the LLM.
* The **database** persists chat history, user data, and embeddings.

---

## Tech Stack

### Backend

#### FastAPI

**Purpose:** Core backend framework

**Responsibilities:**

* Expose REST and WebSocket APIs
* Orchestrate the chatbot request pipeline
* Connect the frontend with the LLM and database
* Handle asynchronous and concurrent requests

> *Think of FastAPI as the Spring Boot equivalent for Python.*

---

#### LangChain

**Purpose:** LLM orchestration framework

**Responsibilities:**

* Prompt management
* Conversation memory handling
* Chaining multiple LLM calls
* Tool and function calling
* Retrieval Augmented Generation (RAG)

> *Acts as the glue layer between business logic and the LLM.*

---

#### Gemini API (Google LLM)

**Purpose:** Large Language Model

**Responsibilities:**

* Understand user intent
* Extract entities
* Generate conversational responses
* Answer user queries

> *This is the “brain” of the chatbot.*

---

### Database

#### Neon Postgres (Serverless)

**Purpose:** Persistent storage

**Responsibilities:**

* Store chat history
* Manage users and conversation state
* Store embeddings for vector search
* Support analytics and reporting

> *A scalable, serverless PostgreSQL solution.*

---

### Frontend

#### React (Vite)

**Purpose:** User Interface

**Responsibilities:**

* Render the chat UI
* Handle real-time updates
* Manage client-side state

---

#### TanStack Query

**Purpose:** Server-state management

**Responsibilities:**

* Perform API calls
* Cache responses
* Handle retries and error states
* Synchronize server and client state

> *Think of this as Axios plus a powerful caching layer.*

---

#### Chat UI Kit

**Purpose:** UI acceleration

**Responsibilities:**

* Provide prebuilt chat components
* Speed up chat UI development
* Ensure consistent UX patterns

---

## Architecture (MVC Pattern)

The application loosely follows the **Model–View–Controller (MVC)** pattern for clarity and separation of concerns.

### Model

**Includes:**

* Intent and entity schemas
* Conversation state
* SQLAlchemy models
* Database tables

**Responsible for:**

* Data persistence
* Conversation memory
* Embeddings and historical context

---

### View

**Includes:**

* React chat interface
* Message bubbles
* Typing indicators
* Streaming responses

**Responsible for:**

* User interface
* User experience

---

### Controller

**Includes:**

* FastAPI routes
* LangChain pipelines
* Gemini API calls
* Database interactions

**Responsible for:**

* Business logic
* Request orchestration
* Response handling

---

## Request Flow (High Level)

```text
User Message
   ↓
React UI
   ↓
FastAPI Controller
   ↓
LangChain Pipeline
   ↓
Gemini API
   ↓
Postgres (store history / state)
   ↓
Response → React UI
```

---

## Key Design Principles

* Asynchronous and scalable backend
* Clean separation of concerns
* LLM-agnostic orchestration layer
* Real-time user experience
* Extensible for RAG, tools, and analytics

---
