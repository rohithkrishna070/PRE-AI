# ⚡ PRE-AI: Prompt Refinement & Evaluation AI Platform

> **GitHub for AI Prompts + Token Compression Engine + Multi-LLM Benchmark Runner**

PRE-AI is a full-stack platform built for prompt version control, automated token optimization, model-specific prompt tuning, side-by-side LLM benchmarking, and production deployment management.

---

## 📚 Learning Concepts & Codebase Structure

Every file in this project contains **extensive educational comments** explaining line-by-line what each function, class, and block does!

```
R:\PRE-AI\
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  --> FastAPI REST Controllers (auth, projects, prompts, refine, experiments, deployments, audit)
│   │   ├── core/              --> Config & JWT/Bcrypt security
│   │   ├── db/                --> SQLAlchemy Session, Base, and Automatic PostgreSQL/SQLite Fallback Engine
│   │   ├── models/            --> Database ORM entities (User, Project, Prompt, PromptVersion, Evaluation, Experiment, Deployment)
│   │   ├── schemas/           --> Pydantic v2 Request/Response validation schemas
│   │   ├── providers/         --> AI Provider Factory (Google Gemini + Local Ollama + Mock)
│   │   ├── services/          --> Business logic (Token Refinement Engine, Prompt Versioning, Evaluation Engine, Stats)
│   │   └── main.py            --> FastAPI main application entry point
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/        --> React components (Navbar, Dashboard, PromptRefiner, VersionHistory)
    │   ├── services/api.js    --> Axios HTTP Client
    │   └── main.jsx           --> React mounting point
    ├── index.html
    └── package.json
```

---

## 🛢️ PostgreSQL Database Setup Guide

You have **two options** for running the database:

### Option A: Use Automatic Zero-Config Engine (Default)
By default, the backend checks for a live PostgreSQL connection. If PostgreSQL is not created yet, it **automatically falls back to a local SQLite database (`preai_dev.db`)**, so you can develop and test immediately without configuring anything!

---

### Option B: Create PostgreSQL Database (Step-by-Step)

To connect the platform to your local PostgreSQL server:

1. **Open pgAdmin 4** (or open your terminal and run `psql -U postgres`).
2. Run the SQL command to create the database:
   ```sql
   CREATE DATABASE preai_db;
   ```
3. Update your `backend/app/core/config.py` (or `.env` file) with your PostgreSQL password:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_SERVER=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=preai_db
   ```
4. Run the database table initialization script:
   ```powershell
   cd R:\PRE-AI\backend
   python -m app.db.init_db
   ```

---

## 🚀 How to Run the Platform

### 1. Launch Backend (FastAPI Server)
```powershell
cd R:\PRE-AI\backend
python -m uvicorn app.main:app --reload --port 8000
```
- Interactive API Documentation (Swagger UI): `http://localhost:8000/docs`

### 2. Launch Frontend (React App)
```powershell
cd R:\PRE-AI\frontend
npm install
npm run dev
```
- Open browser at: `http://localhost:3000`

---

## 🤖 Free AI Providers Setup

* **Google Gemini (Free Cloud AI)**: Set `GEMINI_API_KEY=your_key` in `.env`.
* **Ollama (Free Local AI)**: Download and run Ollama from [ollama.com](https://ollama.com). Run `ollama pull llama3`.
