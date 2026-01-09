# 👁️ Project Drishti  
### AI-Powered Situational Awareness Platform for Large Public Event Safety

---

## 📖 Overview
Large-scale public events such as music festivals, rallies, and sports gatherings involve highly dynamic crowd movement and significant safety risks. Traditional monitoring systems are largely reactive, making it difficult to anticipate incidents like bottlenecks, crowd surges, or medical emergencies.

**Project Drishti** is an AI-powered situational awareness platform that acts as a **central nervous system for event safety**. It leverages Google AI technologies to provide **real-time insights, predictive intelligence, and automated response coordination**, enabling authorities to move from reactive monitoring to proactive intervention.

---

## 🎯 Objectives
- Predict crowd bottlenecks before they become dangerous
- Provide real-time, AI-generated situational summaries for commanders
- Enable intelligent and automated emergency resource dispatch
- Detect visual and behavioral anomalies in large crowds
- Improve overall safety and response efficiency at public events

---

## 🚨 Key Challenges Addressed
- Crowd congestion and crushing risks  
- Delayed response to medical emergencies  
- Lack of unified situational awareness  
- Manual and inefficient resource coordination  

---

## 🧠 Core Features

### 🔮 Predictive Bottleneck Analysis
- Ingests real-time video feeds from drones and fixed cameras
- Uses **Vertex AI Vision** to analyze crowd density, velocity, and flow
- Applies **Vertex AI Forecasting** to predict bottlenecks **15–20 minutes in advance**
- Enables proactive crowd diversion and management

---

### 📝 AI-Powered Situational Summaries
- Commanders can query the system using natural language  
  _Example:_  
  > “Summarize security concerns in the West Zone”
- Powered by **Gemini models**
- Fuses insights from:
  - Video analytics
  - Security reports
  - Social media signals
- Produces concise, actionable briefings

---

### 🚑 Intelligent Resource Dispatch
- Automatically triggered during incidents (e.g., medical emergencies)
- Built using **Vertex AI Agent Builder**
- Identifies:
  - Exact incident location
  - Nearest available response unit using GPS
- Calculates fastest, least congested route via **Google Maps APIs**
- Instantly dispatches responders

---

### 🚨 Multimodal Anomaly Detection
- Continuously scans live video feeds using **multimodal Gemini models**
- Detects anomalies such as:
  - Smoke or fire
  - Sudden crowd surges
  - Panic-like crowd behavior
- Triggers immediate, high-priority alerts

---

## 🚀 Advanced & Innovative Capabilities (Go Beyond)
- 🔍 **AI-powered Lost & Found** using photo matching across live feeds
- 😨 **Crowd sentiment analysis** to detect rising panic levels
- 🚁 **Autonomous drone dispatch** for closer inspection of high-risk zones
- 📡 Real-time incident escalation and visualization dashboard

---

## 🛠️ Tech Stack (Google AI – Mandatory)

### 🔹 AI & ML
- Vertex AI Vision
- Vertex AI Forecasting
- Gemini (Multimodal & NLP)
- Vertex AI Agent Builder

### 🔹 Cloud & Backend
- Google Cloud Platform (GCP)
- Firebase Studio (for deployment & backend services)

### 🔹 Maps & Location
- Google Maps API
- GPS-based unit tracking

### 🔹 Data Sources
- Live video feeds (drones & fixed cameras)
- Security reports
- Social media streams

---

## 📂 Project Architecture (High-Level)
Project-Drishti/
│
├── video-ingestion/ # Live video feed processing
├── ai-models/ # Vertex AI Vision & Forecasting
├── agent-services/ # AI Agent for dispatch & automation
├── dashboard/ # Command center interface
├── firebase/ # Firebase Studio deployment
├── maps-routing/ # Google Maps integration
├── README.md # Project documentation
└── requirements.txt # Dependencies
