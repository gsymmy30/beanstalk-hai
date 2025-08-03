import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def call_model(prompt: str, max_tokens=3000, temperature=0.1) -> str:
    """Centralized OpenAI API call function"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai.api_key:
        print("❌ No OpenAI API key found. Please add OPENAI_API_KEY to your .env file")
        return '{"title": "Mock Story", "story": "This is a test story.", "moral": "Always test your code!"}'
    
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]

def simple_input_validation(user_input: str) -> dict:
    """Simple input validation without importing agents"""
    if not user_input or len(user_input.strip()) < 2:
        return {
            "valid": False,
            "story_elements": "",
            "suggestion": "I need a bit more to work with! Try something like: 'A story about a brave mouse who lives in a library'"
        }
    
    # For now, just enhance single words
    cleaned = user_input.strip()
    if len(cleaned.split()) == 1:
        story_elements = f"A story about a {cleaned.lower()}"
    else:
        story_elements = user_input
    
    return {
        "valid": True,
        "story_elements": story_elements,
        "suggestion": ""
    }

def generate_bedtime_story(story_request: str) -> dict:
    """Generate bedtime story using direct LLM call"""
    prompt = f"""
Create a bedtime story for children aged 5-10 based on: "{story_request}"

REQUIREMENTS:
- Length: 900-1000 words (perfect for 10-15 minutes reading)
- Child protagonist (age 5-10) who solves problems independently
- Gentle, positive themes (friendship, kindness, exploration, overcoming small fears)
- Simple plot: clear beginning, middle, peaceful resolution
- Magical/imaginative elements balanced with familiar settings
- Soothing language that gradually winds down toward the end
- Light humor and playfulness without overstimulation
- Happy, reassuring ending that makes child feel safe and sleepy

Respond ONLY with valid JSON:
{{
    "title": "Compelling story title",
    "story": "Complete 900-1000 word narrative",
    "moral": "Simple life lesson naturally embedded in the story"
}}
"""
    
    try:
        response = call_model(prompt, max_tokens=1200, temperature=0.7)
        import json
        return json.loads(response)
    except:
        return {
            "title": "A Magical Adventure",
            "story": "Once upon a time, there was a kind and curious child who discovered something wonderful that led to an amazing journey filled with friendship and joy. After their adventure, they returned home feeling happy and safe, ready for sweet dreams.",
            "moral": "Every day holds the possibility of magic and wonder."
        }

def generate_qa_questions(story: dict) -> list:
    """Generate Q&A questions for the story"""
    prompt = f"""
Generate 3 engaging questions that curious 5-10 year old children might ask about this story:

Story: {story['title']} - {story['story'][:500]}...

Make them specific to this story and age-appropriate.

Respond ONLY with valid JSON:
{{"questions": ["Question 1", "Question 2", "Question 3"]}}
"""
    
    try:
        response = call_model(prompt, max_tokens=300, temperature=0.3)
        import json
        result = json.loads(response)
        return result.get("questions", [])
    except:
        return [
            "What was your favorite part of the story?",
            "What do you think happened next?",
            "If you could be in the story, what would you do?"
        ]

def answer_question(question: str, story: dict) -> str:
    """Answer a child's question about the story"""
    prompt = f"""
Answer this child's question about the bedtime story in a warm, age-appropriate way (2-4 sentences):

Story Context: {story['title']} - {story['story'][:300]}...
Child's Question: "{question}"

Keep the magic alive and be encouraging. Respond with just the answer (no JSON).
"""
    
    try:
        return call_model(prompt, max_tokens=200, temperature=0.4).strip()
    except:
        return "That's such a wonderful question! What do you think the answer might be?"

def main():
    """Main Beanstalk AI story generation loop"""
    print("🌱 Welcome to Beanstalk AI - Magical Bedtime Stories!")
    print("=" * 50)
    
    while True:
        print("\n📖 Let's create a magical bedtime story!")
        user_input = input("What kind of story would you like? (or 'quit' to exit): ")
        
        if user_input.lower() == 'quit':
            print("✨ Sweet dreams! Thanks for using Beanstalk AI!")
            break
        
        try:
            # Step 1: Validate input
            processed_input = simple_input_validation(user_input)
            if not processed_input["valid"]:
                print(f"🤔 {processed_input['suggestion']}")
                continue
            
            # Step 2: Generate story
            print("✨ Creating your magical bedtime story...")
            story = generate_bedtime_story(processed_input["story_elements"])
            
            # Step 3: Present the story
            print("\n" + "=" * 60)
            print(f"📚 {story['title']}")
            print("=" * 60)
            print(story['story'])
            print(f"\n💭 Moral: {story['moral']}")
            print("=" * 60)
            
            # Step 4: Q&A opportunity
            questions = generate_qa_questions(story)
            print(f"\n🤔 Curious about the story? You can ask up to 3 questions!")
            print("Example questions:")
            for i, q in enumerate(questions, 1):
                print(f"  {i}. {q}")
            
            questions_asked = 0
            while questions_asked < 3:
                question = input(f"\n❓ Your question ({3-questions_asked} left, or 'done'): ")
                if question.lower() == 'done':
                    break
                
                answer = answer_question(question, story)
                print(f"💡 {answer}")
                questions_asked += 1
            
            print("\n🌙 Sweet dreams!")
                
        except Exception as e:
            print(f"❌ Oops! Something went wrong: {e}")
            print("Let's try again with a different story idea!")

if __name__ == "__main__":
    main()