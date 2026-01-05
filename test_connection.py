from google import genai
import google.genai as genai_module

client = genai.Client(api_key="YOUR_API_KEY")

print(f"📦 SDK Version: {genai_module.__version__}")

if hasattr(client, 'file_search_stores'):
    print("✅ Success! file_search_stores is available.")
else:
    print("❌ Error: Still can't find file_search_stores.")
    print("Try: pip3 show google-genai (check the version number)")