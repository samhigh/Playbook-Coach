Overview
A context-aware behavioral nudge engine that transforms a static "Performance Playbook" into proactive SMS interactions. This project demonstrates how to leverage Retrieval-Augmented Generation (RAG) to provide highly personalized, domain-specific coaching.

Key Features
Managed RAG Pipeline: Ingests unstructured data (PDF/TXT) into a Google Gemini File Search Store for real-time retrieval.

Contextual Nudging: Uses Gemini 2.5 Flash to synthesize daily tasks with personal investment philosophies and sports psychology.

Zero-UI Interaction: Delivers high-intent triggers directly to the user via the Twilio SMS API.

Automated Scheduling: Features a background task scheduler to trigger interventions at specific focus blocks.

Tech Stack
AI/LLM: Google Gemini API (File Search / Managed RAG)

Communication: Twilio SMS API

Language/Environment: Python 3.13, Virtualenv, Dotenv

Automation: APScheduler

Getting Started
Clone the repository.

Create a .env file with your GEMINI_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and phone numbers.

Install dependencies: pip install -r requirements.txt.

Add your personal goals to playbook.txt.

Run the coach: python main.py.