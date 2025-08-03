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

def display_judge_metrics(judge_scores: dict) -> None:
    """Display detailed judge evaluation metrics in a user-friendly format"""
    
    print("\n" + "🔍 STORY QUALITY EVALUATION" + " " * 20)
    print("=" * 60)
    
    # Safety Check
    if not judge_scores.get("safety_passed", True):
        print("❌ SAFETY CHECK: FAILED")
        print(f"   Issues: {judge_scores.get('safety_issues', 'Unknown safety concern')}")
        print("=" * 60)
        return
    else:
        print("✅ SAFETY CHECK: PASSED")
    
    # Length Analysis
    length_check = judge_scores.get("length_check", {})
    if length_check:
        word_count = length_check.get("word_count", 0)
        read_time = length_check.get("estimated_read_time", 0)
        acceptable = length_check.get("acceptable", False)
        
        status = "✅ OPTIMAL" if acceptable else "⚠️  NEEDS ADJUSTMENT"
        print(f"\n📏 LENGTH ANALYSIS: {status}")
        print(f"   Word Count: {word_count} words")
        print(f"   Read Time: ~{read_time} minutes")
        print(f"   Target Range: {length_check.get('target_range', 'Unknown')}")
        print(f"   Assessment: {length_check.get('feedback', 'No feedback available')}")
    
    # Quality Scores
    print(f"\n📊 QUALITY SCORES (Research-Based 10-Point Rubric):")
    print("-" * 50)
    
    # Define scoring dimensions with weights
    dimensions = [
        ("character_connection", "Character Connection", "30%"),
        ("bedtime_appropriate", "Bedtime Appropriate", "25%"),
        ("storytelling_craft", "Storytelling Craft", "25%"),
        ("age_appropriate", "Age Appropriate", "20%")
    ]
    
    total_weighted_score = 0
    for dim_key, dim_name, weight in dimensions:
        score = judge_scores.get(dim_key, 0)
        
        # Determine score level
        if score >= 9.0:
            level = "🌟 EXCEPTIONAL"
        elif score >= 7.0:
            level = "🎯 STRONG"
        elif score >= 5.0:
            level = "📝 ADEQUATE"
        elif score >= 3.0:
            level = "⚠️  WEAK"
        else:
            level = "❌ POOR"
        
        print(f"   {dim_name:<20} {score:>4.1f}/10  {level:<15} (Weight: {weight})")
        
        # Add to weighted calculation
        weight_val = float(weight.strip('%')) / 100
        total_weighted_score += score * weight_val
    
    # Overall Score
    overall_score = judge_scores.get("overall_score", total_weighted_score)
    passed = judge_scores.get("passed", False)
    
    print("-" * 50)
    if passed:
        status_icon = "🎉"
        status_text = "APPROVED FOR PUBLICATION"
    else:
        status_icon = "🔄"
        status_text = "NEEDS REFINEMENT"
    
    print(f"   {'OVERALL SCORE':<20} {overall_score:>4.1f}/10  {status_icon} {status_text}")
    
    # Pass/Fail Requirements
    print(f"\n📋 EVALUATION CRITERIA:")
    print(f"   ✓ Safety Gate: {'PASSED' if judge_scores.get('safety_passed', True) else 'FAILED'}")
    print(f"   ✓ Overall Score ≥ 7.0: {'PASSED' if overall_score >= 7.0 else f'FAILED ({overall_score:.1f}/7.0)'}")
    print(f"   ✓ Bedtime Score ≥ 6.0: {'PASSED' if judge_scores.get('bedtime_appropriate', 0) >= 6.0 else 'FAILED'}")
    print(f"   ✓ All Dimensions ≥ 4.0: {'PASSED' if all(judge_scores.get(d[0], 0) >= 4.0 for d in dimensions) else 'FAILED'}")
    print(f"   ✓ Length Acceptable: {'PASSED' if length_check.get('acceptable', False) else 'FAILED'}")
    
    # Detailed Feedback (if available)
    feedback = judge_scores.get("feedback", {})
    if feedback:
        print(f"\n💬 DETAILED FEEDBACK:")
        print("-" * 40)
        for dim_key, dim_name, _ in dimensions:
            if dim_key in feedback:
                print(f"\n📝 {dim_name}:")
                # Wrap long feedback text
                feedback_text = feedback[dim_key]
                words = feedback_text.split()
                lines = []
                current_line = "   "
                for word in words:
                    if len(current_line + word) > 65:
                        lines.append(current_line.rstrip())
                        current_line = "   " + word + " "
                    else:
                        current_line += word + " "
                if current_line.strip():
                    lines.append(current_line.rstrip())
                
                for line in lines:
                    print(line)
    
    print("=" * 60)

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
            
            # Step 4: Display detailed judge metrics
            display_judge_metrics(judge_scores)
            
            # Check if story passed safety
            if not judge_scores.get("safety_passed", True):
                print(f"\n❌ Story failed safety evaluation. Please try a different story request.")
                continue
            
            # Step 5: Present the story
            print("\n" + "📚 YOUR BEDTIME STORY" + " " * 25)
            print("=" * 60)
            print(f"🏷️  Title: {story_result['title']}")
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