#!/usr/bin/env python3
"""
Test the complete Beanstalk AI pipeline end-to-end
"""

import os
import openai
from dotenv import load_dotenv
from agents.input_handler import InputHandler
from agents.story_generator import StoryGenerator
from agents.judge import JudgeSystem
from agents.qa import QAAgent

# Load environment variables
load_dotenv()

def call_model(prompt: str, max_tokens=3000, temperature=0.1) -> str:
    """LLM call function"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai.api_key:
        print("❌ No OpenAI API key found. Set OPENAI_API_KEY in your .env file")
        print("   Using mock responses for demo...")
        return mock_response(prompt)
    
    # Real OpenAI call
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]

def mock_response(prompt: str) -> str:
    """Mock responses for testing without API key"""
    if "analyze this user input" in prompt.lower():
        return '{"valid": true, "story_elements": "A story about a brave mouse in a library", "suggestion": ""}'
    elif "safety" in prompt.lower():
        return '{"passed": true, "issues": ""}'
    elif "generate example questions" in prompt.lower():
        return '{"questions": ["What books does the mouse like to read?", "How did the mouse learn to be brave?", "What other animals live in the library?"]}'
    elif "answer" in prompt.lower():
        return "That's a wonderful question! I think the mouse probably loves adventure books the most."
    else:
        return '{"title": "The Brave Library Mouse", "story": "Once upon a time, there was a little mouse named Pip who lived in the corner of the town library...", "moral": "Even the smallest among us can be heroes."}'

def test_full_pipeline():
    """Test the complete Beanstalk AI system"""
    
    print("🌱 BEANSTALK AI - FULL PIPELINE TEST")
    print("=" * 60)
    
    # Initialize all agents
    input_handler = InputHandler(call_model)
    story_generator = StoryGenerator(call_model)
    judge_system = JudgeSystem(call_model)
    qa_agent = QAAgent(call_model)
    
    # Test inputs
    test_inputs = [
        "A story about a mouse who lives in a library",
        "dragon",
        "sdfdfgg"  # Should get enhanced by input handler
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n🎬 TEST {i}: '{user_input}'")
        print("=" * 50)
        
        try:
            # STEP 1: Input Processing
            print("1️⃣  Processing input...")
            processed = input_handler.process_input(user_input)
            
            if not processed["valid"]:
                print(f"❌ Invalid input: {processed['suggestion']}")
                continue
            
            print(f"✅ Input processed: {processed['story_elements']}")
            
            # STEP 2: Story Generation
            print("\n2️⃣  Generating story...")
            story = story_generator.generate_story(processed["story_elements"])
            print(f"✅ Story generated: '{story['title']}'")
            print(f"   Word count: {len(story['story'].split())} words")
            
            # STEP 3: Judge Evaluation
            print("\n3️⃣  Evaluating with judge...")
            evaluation = judge_system.evaluate_story(story)
            
            if not evaluation.get("safety_passed", True):
                print(f"❌ Failed safety gate: {evaluation.get('safety_issues', 'Unknown')}")
                continue
            
            print(f"✅ Safety passed")
            print(f"📊 Overall score: {evaluation.get('overall_score', 'N/A')}/5")
            
            refinement_count = 0
            while judge_system.needs_refinement(evaluation) and refinement_count < 2:
                print(f"\n🔄 Refinement needed (attempt {refinement_count + 1})...")
                instructions = judge_system.generate_refinement_instructions(evaluation)
                print(f"   Instructions: {instructions[:100]}...")
                
                story = story_generator.refine_story(story, instructions)
                evaluation = judge_system.evaluate_story(story)
                refinement_count += 1
            
            if evaluation.get("passed", False):
                print("🎉 Story approved by judge!")
            else:
                print("⚠️  Story accepted after max refinements")
            
            # STEP 4: Present Story
            print(f"\n4️⃣  Final Story:")
            print(f"📚 {story['title']}")
            print("-" * 30)
            print(story['story'][:200] + "..." if len(story['story']) > 200 else story['story'])
            print(f"\n💭 Moral: {story['moral']}")
            
            # STEP 5: Q&A Session
            print(f"\n5️⃣  Q&A Opportunity:")
            questions = qa_agent.generate_question_opportunities(story)
            print("🤔 Example questions you could ask:")
            for j, q in enumerate(questions, 1):
                print(f"   {j}. {q}")
            
            # Simulate asking a question
            if questions:
                sample_question = questions[0]
                print(f"\n❓ Let's try asking: '{sample_question}'")
                answer = qa_agent.answer_question(sample_question, story)
                print(f"💡 Answer: {answer}")
            
            print(f"\n✨ Test {i} completed successfully!")
            
        except Exception as e:
            print(f"💥 Error in test {i}: {e}")
        
        if i < len(test_inputs):
            input(f"\n➡️  Press Enter for next test...")
    
    print("\n" + "=" * 60)
    print("🎉 FULL PIPELINE TEST COMPLETE!")
    print("\nBeanstalk AI successfully demonstrated:")
    print("✅ Smart input handling")
    print("✅ Story generation") 
    print("✅ Research-backed quality evaluation")
    print("✅ Story refinement")
    print("✅ Interactive Q&A")

if __name__ == "__main__":
    test_full_pipeline()