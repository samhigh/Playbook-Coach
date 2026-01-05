import os
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from twilio.rest import Client as TwilioClient
from apscheduler.schedulers.background import BackgroundScheduler

# 1. SETUP & CONFIGURATION
load_dotenv()

# Gemini Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
# Replace this with your actual store ID from your successful run
STORE_ID = "fileSearchStores/performanceplaybook2026-4fjtkh1kpv79"
MODEL_ID = "gemini-2.5-flash"

# Twilio Config
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")
MY_PHONE = os.getenv("MY_PERSONAL_PHONE")
twilio_client = TwilioClient(TWILIO_SID, TWILIO_TOKEN)

# 2. CORE LOGIC FUNCTIONS

def generate_coaching_nudge(task_name):
    """Retrieves context from your Playbook and generates a personalized SMS."""
    print(f"🧠 Gemini is consulting the Playbook for: {task_name}...")
    
    prompt = f"I am about to start my '{task_name}'. Give me a quick, high-performance nudge based on my playbook."
    
    try:
        response = gemini_client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[STORE_ID]
                        )
                    )
                ]
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return f"Time to start {task_name}! Stay focused."

def send_sms(text):
    """Sends the generated text via Twilio."""
    try:
        message = twilio_client.messages.create(
            body=text,
            from_=TWILIO_PHONE,
            to=MY_PHONE
        )
        print(f"✅ SMS Sent! (SID: {message.sid})")
    except Exception as e:
        print(f"❌ Twilio Error: {e}")

def run_nudge_cycle(task_name):
    """The workflow that combines AI generation and SMS delivery."""
    print(f"\n🔔 Triggering nudge cycle at {datetime.now().strftime('%H:%M:%S')}")
    nudge = generate_coaching_nudge(task_name)
    send_sms(nudge)

# 3. SCHEDULER SETUP
def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Example: Schedule your 2026 Focus Blocks
    # Adjust these times to match your actual daily goals
    scheduler.add_job(run_nudge_cycle, 'cron', hour=9, minute=0, args=["90-minute Deep Work Block #1"])
    scheduler.add_job(run_nudge_cycle, 'cron', hour=13, minute=0, args=["90-minute Deep Work Block #2"])
    scheduler.add_job(run_nudge_cycle, 'cron', hour=17, minute=0, args=["30-minute Strength Training"])
    
    scheduler.start()
    print("📅 Scheduler started. Waiting for your focus blocks...")

# 4. MAIN EXECUTION
if __name__ == "__main__":
    print("--- 🚀 THE PLAYBOOK COACH IS ONLINE ---")
    
    # Run a test nudge immediately to verify everything is working
    run_nudge_cycle("Project Setup Test")
    
    # Start the daily automation
    start_scheduler()
    
    # Keep the main thread alive so the background scheduler can run
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\n👋 Coach going offline. See you tomorrow.")