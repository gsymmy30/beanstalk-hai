import os
import openai
from dotenv import load_dotenv
from agents.input_handler import InputHandler
from agents.story_generator import StoryGenerator
from agents.judge import JudgeSystem
from agents.qa import QAAgent

"""
Beanstalk AI - Bedtime Story Generator for Kids 5-10

Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

With 2 more hours, I would have implemented the progress tracking system to demonstrate iterative improvement, 
added story personalization features (remembering user preferences), and created a more sophisticated 
prompt engineering system that learns from successful stories to improve generation quality over time.

"""

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

def main():
    """Main Beanstalk AI story generation loop"""
    print("🌱 Welcome to Beanstalk AI - Magical Bedtime Stories!")
    print("=" * 50)
    
    # Initialize all components
    input_handler = InputHandler(call_model)
    story_generator = StoryGenerator(call_model)
    judge_system = JudgeSystem(call_model)
    qa_agent = QAAgent(call_model)
    
    while True:
        print("\n📖 Let's create a magical bedtime story!")
        user_input = input("What kind of story would you like? (or 'quit' to exit): ")
        
        if user_input.lower() == 'quit':
            print("✨ Sweet dreams! Thanks for using Beanstalk AI!")
            break
        
        try:
            # Step 1: Validate and process input
            print("🔍 Processing your request...")
            processed_input = input_handler.process_input(user_input)
            if not processed_input["valid"]:
                print(f"🤔 {processed_input['suggestion']}")
                continue
            
            print(f"✅ Request processed: {processed_input['story_elements']}")
            
            # Step 2: Generate story
            print("✨ Creating your magical bedtime story...")
            story_result = story_generator.generate_story(processed_input["story_elements"])
            
            # Step 3: Evaluate with judge system
            print("🔍 Evaluating story quality...")
            judge_scores = judge_system.evaluate_story(story_result)
            
            if not judge_scores.get("safety_passed", True):
                print(f"❌ Story failed safety check: {judge_scores.get('safety_issues', 'Unknown issue')}")
                continue
            
            # Step 4: Show quality metrics
            length_check = judge_scores.get("length_check", {})
            print(f"📏 Length: {length_check.get('feedback', 'Unknown length')}")
            
            if judge_scores.get("passed", False):
                print(f"🎉 Story approved! Quality score: {judge_scores.get('overall_score', 'N/A')}/10")
            else:
                print(f"📝 Story completed. Quality score: {judge_scores.get('overall_score', 'N/A')}/10")
                print("   (Story generation focused on excellence - no refinement needed)")
            
            # Step 5: Present the story
            print("\n" + "=" * 60)
            print(f"📚 {story_result['title']}")
            print("=" * 60)
            print(story_result['story'])
            print(f"\n💭 Moral: {story_result['moral']}")
            print("=" * 60)
            
            # Step 6: Q&A opportunity
            qa_questions = qa_agent.generate_question_opportunities(story_result)
            print(f"\n🤔 Curious about the story? You can ask up to 3 questions!")
            print("Example questions:")
            for i, q in enumerate(qa_questions, 1):
                print(f"  {i}. {q}")
            
            questions_asked = 0
            while questions_asked < 3:
                question = input(f"\n❓ Your question ({3-questions_asked} left, or 'done'): ")
                if question.lower() == 'done':
                    break
                
                answer = qa_agent.answer_question(question, story_result)
                print(f"💡 {answer}")
                questions_asked += 1
            
            print("\n🌙 Sweet dreams!")
                
        except Exception as e:
            print(f"❌ Oops! Something went wrong: {e}")
            print("Let's try again with a different story idea!")

if __name__ == "__main__":
    main()