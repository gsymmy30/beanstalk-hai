#!/usr/bin/env python3
"""
Test script for StoryGenerator
"""

import os
import openai
from dotenv import load_dotenv
from agents.story_generator import StoryGenerator

# Load environment variables
load_dotenv()

def call_model(prompt: str, max_tokens=3000, temperature=0.1) -> str:
    """LLM call function"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai.api_key:
        print("❌ No OpenAI API key found. Please add OPENAI_API_KEY to your .env file")
        return '{"title": "Mock Story", "story": "This is a mock story for testing without API key.", "moral": "Always test your code!"}'
    
    # Real OpenAI call
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]

def test_story_generator():
    """Test the StoryGenerator with different story requests"""
    
    print("🌱 Testing Beanstalk AI StoryGenerator")
    print("=" * 60)
    
    generator = StoryGenerator(call_model)
    
    test_requests = [
        "A story about a dragon who is afraid of the dark",
        "A story about a little girl who finds a magic paintbrush",
        "A story about a mouse who lives in a library"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n{i}. Generating story for: '{request}'")
        print("-" * 50)
        
        try:
            story = generator.generate_story(request)
            
            print(f"📚 TITLE: {story['title']}")
            print(f"\n📖 STORY:")
            print(story['story'])
            print(f"\n💭 MORAL: {story['moral']}")
            print(f"\n📊 STATS:")
            print(f"   Word count: {len(story['story'].split())} words")
            print(f"   Character count: {len(story['story'])} characters")
            
            # Ask if user wants to see the next one
            if i < len(test_requests):
                input(f"\n✨ Press Enter to generate the next story...")
                
        except Exception as e:
            print(f"💥 ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("✨ StoryGenerator test complete!")

if __name__ == "__main__":
    test_story_generator()