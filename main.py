import os
import openai
from dotenv import load_dotenv
from agents.input_handler import InputHandler
from agents.story_generator import StoryGenerator
from agents.judge import JudgeSystem
from agents.qa import QAAgent
from utils.story_tracker import StoryTracker

"""
Beanstalk AI - Bedtime Story Generator for Kids 5-10
"""

load_dotenv()

def call_model(prompt: str, max_tokens=3000, temperature=0.1) -> str:
    """OpenAI API wrapper"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai.api_key:
        print("No OpenAI API key found. Add OPENAI_API_KEY to your .env file")
        return '{"title": "Mock Story", "story": "This is a test story.", "moral": "Always test your code!"}'
    
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]

def show_menu():
    """Main menu display"""
    print("\n" + "=" * 50)
    print("🌱✨ BEANSTALK AI ✨🌱".center(50))
    print("Magical Bedtime Stories for Kids 5-10".center(50))
    print("=" * 50)
    print()
    print("  📖  1. Create a new story")
    print("  📊  2. View story report") 
    print("  🌙  3. Exit")
    print()
    print("=" * 50)

def display_scores(judge_scores):
    """Show story quality metrics"""
    print(f"\nQuality Scores")
    print("-" * 20)
    
    scores = [
        ("character_connection", "Character"),
        ("bedtime_appropriate", "Bedtime"),
        ("storytelling_craft", "Storytelling"),
        ("age_appropriate", "Age Level")
    ]
    
    for dim_key, dim_name in scores:
        score = judge_scores.get(dim_key, 0)
        print(f"   {dim_name:<12} {score:>4.1f}/10")
    
    overall = judge_scores.get("overall_score", 0)
    print("-" * 20)
    print(f"   {'Overall':<12} {overall:>4.1f}/10")

def create_story(input_handler, story_generator, judge_system, qa_agent, story_tracker):
    """Handle the story creation workflow with refinement"""
    while True:
        print("\n📖 What kind of bedtime story would you like?")
        print("Examples: 'brave mouse', 'dragon who loves books', 'girl who finds magic paintbrush'")
        
        user_input = input("\nYour story idea (or 'back' to return to menu): ").strip()
        
        if user_input.lower() == 'back':
            return
        
        if not user_input:
            print("I need an idea to work with! Try again.")
            continue
        
        try:
            # Validate input first
            processed_input = input_handler.process_input(user_input)
            if not processed_input["valid"]:
                print(f"\n{processed_input['suggestion']}")
                continue
            
            # Generate initial story
            print("\nCreating your story...")
            initial_story = story_generator.generate_story(processed_input["story_elements"])
            initial_scores = judge_system.evaluate_story(initial_story)
            
            # Safety check on initial story
            if not initial_scores.get("safety_passed", True):
                print("\nStory didn't pass safety check. Let's try a different idea!")
                continue
            
            # Refine the story based on judge feedback
            print("Refining the story...")
            refined_story = story_generator.refine_story(initial_story, initial_scores)
            
            # Get final judge scores on refined story
            final_scores = judge_system.evaluate_story(refined_story)
            
            # Use refined story and final scores
            story_result = refined_story
            judge_scores = final_scores
            
            # Save to tracker (final refined version)
            story_tracker.add_story(
                story=story_result, 
                evaluation=judge_scores, 
                user_request=user_input
            )
            
            # Safety check on final refined story
            if not judge_scores.get("safety_passed", True):
                print("\nRefined story didn't pass safety check. Let's try a different idea!")
                continue
            
            # Display final story
            print("\n" + "YOUR STORY".center(50))
            print("=" * 50)
            print(f"\n📖 {story_result['title']}")
            print(f"\n{story_result['story']}")
            print(f"\n💫 {story_result['moral']}")
            
            # Show quality scores (final refined scores)
            display_scores(judge_scores)
            
            # Q&A session
            qa_questions = qa_agent.generate_question_opportunities(story_result)
            print(f"\nQuestions you might ask about this story:")
            for i, q in enumerate(qa_questions, 1):
                print(f"   {i}. {q}")
            
            questions_asked = 0
            while questions_asked < 3:
                question = input(f"\nAsk a question ({3-questions_asked} left, or 'done'): ").strip()
                if question.lower() == 'done' or not question:
                    break
                
                answer = qa_agent.answer_question(question, story_result)
                print(f"\n{answer}")
                questions_asked += 1
            
            print(f"\n🌙 Story complete! Press Enter to return to menu...")
            input()
            return
            
        except Exception as e:
            print(f"\nSomething went wrong: {e}")
            print("Let's try again!")
            continue

def main():
    """Main application loop"""
    # Initialize components
    input_handler = InputHandler(call_model)
    story_generator = StoryGenerator(call_model)
    judge_system = JudgeSystem(call_model)
    qa_agent = QAAgent(call_model)
    story_tracker = StoryTracker()
    
    while True:
        show_menu()
        
        # Show stats if stories exist
        stats = story_tracker.get_stats()
        if stats["total"] > 0:
            print(f"{stats['total']} stories created | Avg score: {stats['average_score']}/10")
        
        choice = input("\nChoose an option (1-3): ").strip()
        
        if choice == '3':
            print("\n🌙✨ Sweet dreams! Thanks for using Beanstalk AI! ✨🌙")
            break
        elif choice == '2':
            if stats["total"] == 0:
                print("\nNo stories yet! Create your first story to see the report.")
                continue
            story_tracker.generate_html_report()
            print("\nReport saved as 'story_report.html' - open it in your browser!")
            input("Press Enter to continue...")
        elif choice == '1':
            create_story(input_handler, story_generator, judge_system, qa_agent, story_tracker)
        else:
            print("\nPlease choose 1, 2, or 3")

if __name__ == "__main__":
    main()