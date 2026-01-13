# 🚀 Auto Retention Agents  

## Multi-Agent Churn Response System (FastAPI + Real Integrations)

A **Python-based multi-agent system** that simulates and executes **automated customer retention actions** based on churn risk, integrating **real-world services** (Google APIs, Telegram, Email) and exposing the orchestration via **FastAPI** through batch endpoints.

This project is designed as a **realistic workplace simulation**, focusing on **decision automation, agent orchestration, and production-oriented architecture**.

---

## 🧠 What does this system do?

Given a customer and a **churn score** (simulated or real), the system:

1. Evaluates churn risk  
2. Decides the best retention action  
3. Executes **real integrations**  
4. Logs and audits the action  
5. Exposes everything via API and batch execution  

---

## 🏗️ Architecture Overview

```bash

┌───────────────┐
│ FastAPI API   │
└───────┬───────┘
        │
        ▼
┌───────────────────┐
│ Decision Agent    │ ← rules 
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│ Action Agent      │ ← single execution point
└───────┬───────────┘
        │
        ▼
┌──────────────────────────────────────────┐
│ Real Integrations (feature-flagged)      │
│ • Gmail                                  │
│ • Google Calendar + Meet                 │
│ • Google Sheets (audit log)              │
│ • Telegram Bot                           │
└──────────────────────────────────────────┘
```

---

## 📊 Dataset

- Real supermarket customer dataset  
- Demographic + transactional variables  
- The dataset **does not include churn probability**
- A **churn score simulation** is used for realistic testing  

---

## 🔮 Churn Score Simulation

When churn probability is not available:

bash```python
churn_score = round(random.random(), 2) ```

This allows:

* End-to-end pipeline testing
* Realistic decision automation
* Batch and scheduler simulations

In production, this will be replaced by a trained ML model; (models/churn_model.pkl) 

---

## 🤖 Agents

### Decision Agent

Determines which action to execute based on:

* churn_score

* execution mode:

   * deterministic
   * probabilistic (randomized decisions)

### Possible actions:

* schedule_meeting_with_meet
* send_email
* send_telegram
* no_action

---

## ⚙️ Action Agent (Core Orchestrator)

### 👉 All actions are triggered from a single method:

bash```python
execute_action()```

Responsibilities:

* Orchestrates all downstream agents
* Applies feature flags
* Handles failures and fallbacks
* Executes real-world integrations

### 📅 High Churn Flow (≥ 0.85)

For high churn customers, the system automatically executes:

📅 Google Calendar event

🎥 Google Meet generation

✉️ Automatic email with meeting link

📊 Action audit logged in Google Sheets

| Service         | Status |
| --------------- | ------ |
| Gmail           | ✅ Real |
| Google Calendar | ✅ Real |
| Google Meet     | ✅ Real |
| Google Sheets   | ✅ Real |
| Telegram Bot    | ✅ Real |

Features:

* OAuth 2.0 authentication
* Token refresh handling
* Controlled failures
* Feature-flag enable/disable

---

## 🧪 Testing Strategy

✅ Action-Based Tests

* Email only
* Email + Meet + Calendar
* Telegram message
* No action

✅ API Tests

* GET /
* GET /customers/sample
* POST /run-batch

✅ Batch Execution

* Multiple customers
* Random churn simulation
* Real integrations enabled

✅ Scheduler Simulation

* Daily execution simulation
* Prepared for Airflow or cron-based orchestration

✅ Controlled Error Tests

* Expired OAuth token
* Missing Google Sheet
* Telegram API failure
* Disabled services via feature flags

---

## 🌐 FastAPI Endpoints

* Healthcheck
```
GET /
```
* Sample customer
```
GET /customers/sample
```
* Run single customer
```
POST /run-customer/{customer_id}
```
* Run batch
```
POST /run-batch?limit=10
```
### 🔐 Feature Flags
```
USE_REAL_SERVICES = True
```

Allows:

* Mock vs real execution
* Cost-free local testing
* Safe failure simulation

---

## 🧱 Tech Stack

* Python 3.12
* FastAPI
* Pandas
* Google APIs (Gmail, Calendar, Sheets, Meet)
* Telegram Bot API
* OAuth 2.0
* Requests
* python-dotenv

---

## 🚧 Planned / Next Steps

### 🎥 Microfodt functions 

Microsoft Graph real

### 🛠️ Apache Airflow

* DAG-based daily orchestration
* Visual pipeline monitoring
* Production-style scheduling

### 🧠 Machine Learning Integration

* Replace churn simulation with churn_model.pkl
* Real-time inference

### ☁️ Cloud Deployment

* GCP, Azure or AWS
* Secret managers
* Production scheduler

---

## 🎯 Why this project?

This project demonstrates:

✅ Multi-agent architecture

✅ Decision automation

✅ Real-world API integrations

✅ Production-oriented design

✅ Failure handling and fallbacks

✅ API + batch execution patterns

It simulates a real customer retention system, not an academic exercise.

---

## ▶️ How to Use

### 1. Clone the repository

```bash
git clone https://github.com/BarbaraAngelesOrtiz/auto-retention-agents.git
cd auto-retention-agents 
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements.txt
```

### 4. Environment variables

Create a .env file (never commit it):

```bash
# Google APIs
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REFRESH_TOKEN=your_refresh_token
# Gmail
SENDER_EMAIL=your_email@gmail.com
# Google Sheets
GOOGLE_SHEET_ID=your_sheet_id
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
# Feature flags
USE_REAL_SERVICES=true
```

You can disable real integrations by setting USE_REAL_SERVICES=false.

### 5. Run the FastAPI server

```bash
uvicorn main:app --reload
```
Open Swagger UI:
```bash
http://127.0.0.1:8000/docs
```

### 6. Run a batch simulation (local)

Runs a batch of customers with simulated churn scores and real actions:
```bash
python test_batch_random.py
```

### 7. Test API batch execution
```bash
POST /run-batch?limit=5


Example response:
```bash
{
  "processed": 5,
  "results": [
    {
      "customer_id": "C1000",
      "churn_score": 0.87,
      "action": "schedule_meeting_with_meet",
      "status": "success"
    }
  ]
}
```

### 8. Test individual actions

You can test specific flows:

* Email only
* Email + Calendar + Meet
* Telegram message
* No action

By adjusting:

* churn score
* decision mode (deterministic / random)
* feature flags

### 9. Simulate daily execution

Use the batch script to simulate a daily run:

```bash
python test_batch_random.py
```

This mimics a scheduler-triggered execution (cron / Airflow).

### 🔒 Notes

* .env must never be committed
* Google OAuth tokens may expire (handled by refresh logic)
* Failures are logged and do not crash the pipeline
* All actions are executed through a single execute_action() entry point

---

## Authors

**Bárbara Ángeles Ortiz**

<img src="https://github.com/user-attachments/assets/30ea0d40-a7a9-4b19-a835-c474b5cc50fb" width="115">

[LinkedIn](https://www.linkedin.com/in/barbaraangelesortiz/) | 

![Status](https://img.shields.io/badge/status-in%20progress-yellow) 📅 January 2026

![Python](https://img.shields.io/badge/python-3.10-blue)
![Pandas](https://img.shields.io/badge/pandas-2.1.0-blue)

![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

![GoogleAPI](https://img.shields.io/badge/Google_API-integrated-yellow)
![Telegram](https://img.shields.io/badge/Alerts-Telegram-blueviolet)
![GitHubActions](https://img.shields.io/badge/CI-GitHub_Actions-black)
