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

def call_model(prompt: str, max_tokens=3000, temperature=0.7) -> str:
    """Call OpenAI's API"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai.api_key:
        print("\n⚠️  No API key found. Add OPENAI_API_KEY to your .env file")
        return '{"title": "NA", "story": "NA", "moral": "NA"}'
    
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]

def show_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("🌱✨ BEANSTALK AI ✨🌱".center(50))
    print("Magical Bedtime Stories for Kids 5-10".center(50))
    print("=" * 50)
    print()
    print("  📖  1. Create a new story")
    print("  📊  2. View story report") 
    print("  🌙  3. Exit")
    print()

def display_outline(outline):
    """Show the story outline in a clean format"""
    if not outline:
        return
        
    print("\n📝 Story Outline")
    print("-" * 40)
    
    # Main character
    protagonist = outline.get('protagonist', {})
    if protagonist:
        name = protagonist.get('name', 'Unknown')
        age = protagonist.get('age', '?')
        trait = protagonist.get('personality', 'N/A')
        char_type = protagonist.get('type', 'character')
        
        # Format based on type
        if char_type.lower() in ['human', 'child', 'boy', 'girl']:
            print(f"👦 Main Character: {name}, age {age}")
        else:
            print(f"🐲 Main Character: {name} the {char_type}")
        print(f"   Personality: {trait}")
    
    # Friends
    helpers = outline.get('helpers', [])
    if helpers:
        print(f"🐾 Friends:")
        for helper in helpers[:3]:
            if isinstance(helper, dict):
                h_name = helper.get('name', 'Unknown')
                h_type = helper.get('type', 'friend')
                print(f"   - {h_name} the {h_type}")
    
    # Story basics
    setting = outline.get('setting', 'N/A')
    conflict = outline.get('conflict', 'N/A')
    
    print(f"📍 Setting: {setting}")
    print(f"❓ Challenge: {conflict}")
    print("-" * 40)

def display_scores(scores):
    """Display quality scores in a visual way"""
    print(f"\n📊 Story Quality")
    print("-" * 30)
    
    overall = scores.get("overall_score", 0)
    stars = "⭐" * int(overall / 2)
    print(f"Overall: {stars} ({overall:.1f}/10)")

def create_story(input_handler, story_generator, judge_system, qa_agent, story_tracker):
    """Create a new bedtime story"""
    
    print("\n📖 What story shall we create tonight?")
    print("💡 Try: 'a girl named Luna and her best friend Max, who happens to be a dragon'")
    
    user_input = input("\n➤ Your idea: ").strip()
    
    if user_input.lower() in ['menu', 'back', 'exit', '']:
        return False
    
    try:
        # Process the idea
        print("\n✨ Creating your story", end="")
        processed = input_handler.process_input(user_input)
        
        if not processed["valid"]:
            print(f"\n\n💭 {processed['suggestion']}")
            return True
        
        print(".", end="", flush=True)
        
        # Generate the story AND outline
        story, outline = story_generator.generate_story(processed["story_elements"])
        print(".", end="", flush=True)
        
        # Show outline
        if outline:
            print(".")
            display_outline(outline)
            print("\n⏳ Writing full story", end="")
        
        # Evaluate quality
        print(".", end="", flush=True)
        scores = judge_system.evaluate_story(story)
        
        # Safety check
        if not scores.get("safety_passed", True):
            print("\n\n⚠️  Let's try a different story idea!")
            return True
        
        print(".", end="", flush=True)
        
        # Refine the story
        print("\n🔧 Polishing", end="")
        final_story = story
        final_scores = scores
        
        refined = story_generator.refine_story(story, outline, scores)
        if refined['story'] != story['story']:
            print(".", end="", flush=True)
            
            # Show what was improved
            if refined.get('improvements'):
                print(f" ✨")
                print(f"   📝 {refined['improvements']}")
            
            # Re-evaluate the refined story
            refined_scores = judge_system.evaluate_story(refined)
            
            # Only use refined version if it actually improved
            if refined_scores.get("overall_score", 0) > scores.get("overall_score", 0):
                final_story = refined
                final_scores = refined_scores
                print("   ✅ Story improved!")
            else:
                print("   ↔️  Keeping original version")
        else:
            print(" Done!")
        
        # Save the story
        story_tracker.add_story(
            story=final_story, 
            evaluation=final_scores, 
            user_request=user_input
        )
        
        # Display the story
        word_count = len(final_story['story'].split())
        reading_time = max(1, word_count // 150)
        
        print("\n" + "=" * 50)
        print("✨ YOUR BEDTIME STORY ✨".center(50))
        print("=" * 50)
        print(f"\n📚 {final_story['title']}")
        print(f"⏱️  About {reading_time} minute{'s' if reading_time > 1 else ''} to read")
        print("-" * 50)
        print(f"\n{final_story['story']}")
        print(f"\n💫 {final_story['moral']}")
        print("-" * 50)
        
        # Show quality
        display_scores(final_scores)
        
        # Q&A section
        print("\n💬 Got questions about the story?")
        qa_questions = qa_agent.generate_question_opportunities(final_story)
        
        if qa_questions:
            print("Here are some things you could ask:")
            for i, q in enumerate(qa_questions[:3], 1):
                print(f"  {i}. {q}")
            
            print("\n(Ask a question or press Enter to finish)")
            
            asked = 0
            while asked < 3:
                question = input(f"\n❓ ").strip()
                if not question:
                    break
                    
                answer = qa_agent.answer_question(question, final_story)
                print(f"\n💡 {answer}")
                asked += 1
        
        print("\n✨ Story complete!")
        input("Press Enter to continue...")
        return True
        
    except Exception:
        print(f"\n\nOops! Let's try again with a different idea.")
        return True

def main():
    """Run Beanstalk AI"""
    
    # Set up
    input_handler = InputHandler(call_model)
    story_generator = StoryGenerator(call_model)
    judge_system = JudgeSystem(call_model)
    qa_agent = QAAgent(call_model)
    story_tracker = StoryTracker()
    
    print("\n🌟 Welcome to Beanstalk AI!")
    print("   Where bedtime stories come to life...")
    
    while True:
        show_menu()
        
        # Show stats if we have stories
        stats = story_tracker.get_stats()
        if stats["total"] > 0:
            avg_score = stats['average_score']
            print(f"📚 Stories created: {stats['total']} (avg: {avg_score:.1f}/10)")
        
        choice = input("\n➤ Choose: ").strip()
        
        if choice == '1':
            # Create stories
            creating = True
            while creating:
                creating = create_story(
                    input_handler, 
                    story_generator, 
                    judge_system, 
                    qa_agent, 
                    story_tracker
                )
                
        elif choice == '2':
            # View report
            if stats["total"] == 0:
                print("\n📭 No stories yet! Create one first.")
            else:
                story_tracker.generate_html_report()
                print("\n✅ Report saved as 'story_report.html'")
                print("   Open it in your browser to see your stories!")
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            # Exit
            print("\n🌙 Sweet dreams!")
            print("   Thanks for using Beanstalk AI")
            break
            
        else:
            print("\n❌ Just type 1, 2, or 3")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Sweet dreams!")
    except Exception as e:
        print(f"\n❌ Something went wrong: {e}")
        print("Please restart the app.")