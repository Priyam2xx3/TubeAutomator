import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
else:
    genai.configure(api_key=api_key)

    output_file = "available_models.txt"

    print(f"Checking available models and saving to {output_file}...")

    try:
        with open(output_file, "w") as f:
            f.write("=== Google Gemini Models Available to Your API Key ===\n\n")
            
            model_count = 0
            # List all models
            for m in genai.list_models():
                # We only care about models that can generate content (text/chat)
                if 'generateContent' in m.supported_generation_methods:
                    # Write details to file
                    f.write(f"Model Name: {m.name}\n")
                    f.write(f"Description: {m.description}\n")
                    f.write(f"Input Token Limit: {m.input_token_limit}\n")
                    f.write(f"Output Token Limit: {m.output_token_limit}\n")
                    f.write("-" * 40 + "\n")
                    
                    # Print a short confirmation to the terminal
                    print(f"✅ Found: {m.name}")
                    model_count += 1
            
            if model_count == 0:
                f.write("No models found that support content generation.\n")
                print("⚠️ No suitable models found.")
            else:
                f.write(f"\nTotal Models Found: {model_count}")
                print(f"\n🎉 Success! Saved {model_count} models to '{output_file}'")

    except Exception as e:
        error_msg = f"❌ Error retrieving models: {str(e)}"
        print(error_msg)
        # Write the error to the file too, so you can debug later
        with open(output_file, "w") as f:
            f.write(error_msg)