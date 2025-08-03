#!/usr/bin/env python3
"""
Quick test script for InputHandler
"""

import os
import openai
from dotenv import load_dotenv
from agents.input_handler import InputHandler

# Load environment variables from .env file
load_dotenv()

def call_model(prompt: str, max_tokens=3000, temperature=0.1) -> str:
    """Mock LLM call for testing - replace with real OpenAI when ready"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai.api_key:
        # Mock response for testing without API key
        print("🔧 Using mock LLM (no API key found)")
        if "sdfdfgg" in prompt:
            return '{"valid": false, "story_elements": "", "suggestion": "I didn\'t catch that! Try: \'A story about a friendly robot\'"}'
        elif any(word in prompt.lower() for word in ["dragon", "cat", "mouse", "adventure"]):
            story_element = "a magical adventure"
            for word in ["dragon", "cat", "mouse", "robot", "princess"]:
                if word in prompt.lower():
                    story_element = f"a {word}"
                    break
            return f'{{"valid": true, "story_elements": "A story about {story_element}", "suggestion": ""}}'
        else:
            return '{"valid": true, "story_elements": "A story about friendship and adventure", "suggestion": ""}'
    
    # Real OpenAI call
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]

def test_input_handler():
    """Test the InputHandler with various inputs"""
    
    print("🌱 Testing Beanstalk AI InputHandler")
    print("=" * 50)
    
    handler = InputHandler(call_model)
    
    test_cases = [
        "A story about a girl named Alice and her cat Bob",
        "dragon",
        "sdfdfgg",
        "",
        "something magical",
        "Spider-Man saves the day",
        "my pet died",
        "asdf123",
        "time bomb",
        "brdkfvnfjv"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{test_input}'")
        print("-" * 30)
        
        try:
            result = handler.process_input(test_input)
            
            if result["valid"]:
                print(f"✅ VALID")
                print(f"📝 Enhanced: {result['story_elements']}")
            else:
                print(f"❌ INVALID")
                print(f"💡 Suggestion: {result['suggestion']}")
                
        except Exception as e:
            print(f"💥 ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("✨ InputHandler test complete!")

if __name__ == "__main__":
    test_input_handler()