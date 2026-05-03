# 🤖 Smart AI Meeting Assistant

A professional Flask-based web application that converts meeting transcripts into actionable insights. It uses a hybrid approach of **Deep Learning (Transformers)** and **Rule-based NLP** to provide high-accuracy reports.

## ✨ Key Features
*   **AI Summarization:** Utilizes the `BART-large-CNN` model for abstractive summarization[cite: 3].
*   **Entity Recognition:** Automatically detects meeting participants using `BERT` NER[cite: 3].
*   **Structured Insights:** Extracts Action Items, Decisions, and Questions using a custom NLP Pipeline.
*   **Sentiment Analysis:** Analyzes the overall tone of the meeting (Positive/Negative/Neutral)[cite: 2].
*   **Session History:** Keeps track of previous reports during the active session.

## 🛠️ Technology Stack
*   **Backend:** Flask (Python)[cite: 1]
*   **AI Models:** Hugging Face Transformers (BART & BERT)[cite: 3]
*   **Processing:** PyTorch, Regex, Dataclasses[cite: 2]
*   **Frontend:** HTML5, CSS (Responsive Report Design)

## 🚀 Quick Start
1. Install dependencies:
   ```bash
   pip install flask transformers torch sentencepiece