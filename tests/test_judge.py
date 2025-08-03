#!/usr/bin/env python3
"""
Test script for JudgeSystem
"""

import os
import openai
from dotenv import load_dotenv
from agents.judge import JudgeSystem

# Load environment variables
load_dotenv()

def call_model(prompt: str, max_tokens=3000, temperature=0.1) -> str:
    """LLM call function"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai.api_key:
        print("❌ No OpenAI API key found. Please add OPENAI_API_KEY to your .env file")
        return '{"narrative_excellence": 3.5, "story_authenticity": 3.0, "bedtime_flow": 4.0, "age_appropriate_wonder": 3.8, "feedback": {"narrative_excellence": "Mock evaluation", "story_authenticity": "Mock evaluation", "bedtime_flow": "Mock evaluation", "age_appropriate_wonder": "Mock evaluation"}}'
    
    # Real OpenAI call
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]

def test_judge_system():
    """Test the JudgeSystem with different story qualities"""
    
    print("🌱 Testing Beanstalk AI JudgeSystem")
    print("=" * 60)
    
    judge = JudgeSystem(call_model)
    
    # Test stories with different quality levels
    test_stories = [
        {
            "name": "Good Bedtime Story",
            "story": {
                "title": "Luna the Library Dragon",
                "story": "Eight-year-old Maya loved visiting the old library in her neighborhood. One evening, as the sun was setting and casting golden light through the tall windows, she discovered something magical. Behind the dusty astronomy books lived Luna, a small purple dragon who organized books by the colors of their covers. Luna was shy and had been hiding from people for years, but she was also very lonely. Maya wasn't scared at all - she thought Luna was the most wonderful thing she'd ever seen. 'Would you like to be friends?' Maya asked gently. Luna's eyes sparkled with joy. Together, they spent the evening arranging books in rainbow patterns and sharing stories about far-away planets and friendly aliens. As the library grew quiet and peaceful, Luna showed Maya a cozy reading nook with soft cushions where she liked to curl up. 'This is my favorite spot for dreaming,' Luna whispered. Maya promised to visit again soon. As Maya walked home under the twinkling stars, she felt happy knowing she had made such a special friend. That night, she drifted off to sleep thinking about all the magical stories she and Luna would discover together.",
                "moral": "Friendship can be found in the most unexpected places, and kindness opens doors to wonderful adventures."
            }
        },
        {
            "name": "Poor Bedtime Story (Too Exciting)",
            "story": {
                "title": "The Racing Adventure",
                "story": "Tommy was in the biggest race of his life! Cars were crashing everywhere and the crowd was screaming! He had to win or else his family would lose their house! The evil race car driver Black Lightning was trying to run Tommy off the track! Tommy's car was going 200 miles per hour! Suddenly there was a massive explosion! Tommy's car flipped three times but he was okay! The race wasn't over yet! He had to catch up! More cars crashed and there was smoke everywhere! Tommy pressed the turbo button and his car shot forward like a rocket! He was gaining on Black Lightning! The finish line was coming up! Who would win?!",
                "moral": "Never give up even when things look impossible."
            }
        },
        {
            "name": "Unsafe Story (Should Fail Safety)",
            "story": {
                "title": "The Scary Monster",
                "story": "Little Sarah was walking home when a terrifying monster jumped out from behind a tree. It had bloody claws and glowing red eyes. Sarah screamed in terror as the monster chased her through the dark forest. She was so scared she could barely breathe. The monster was getting closer and closer with its sharp teeth ready to bite her.",
                "moral": "Sometimes scary things happen but we have to be brave."
            }
        }
    ]
    
    for i, test_case in enumerate(test_stories, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print("-" * 50)
        print(f"📚 Title: {test_case['story']['title']}")
        print(f"📝 Story excerpt: {test_case['story']['story'][:100]}...")
        
        try:
            # Evaluate the story
            evaluation = judge.evaluate_story(test_case['story'])
            
            # Show results
            if not evaluation.get("safety_passed", True):
                print("❌ FAILED SAFETY GATE")
                print(f"   Issues: {evaluation.get('safety_issues', 'Unknown')}")
            else:
                print("✅ PASSED SAFETY GATE")
                
                # Show quality scores
                print(f"\n📊 QUALITY SCORES:")
                print(f"   Narrative Excellence: {evaluation.get('narrative_excellence', 'N/A')}/5")
                print(f"   Story Authenticity:   {evaluation.get('story_authenticity', 'N/A')}/5")
                print(f"   Bedtime Flow:         {evaluation.get('bedtime_flow', 'N/A')}/5")
                print(f"   Age Wonder:           {evaluation.get('age_appropriate_wonder', 'N/A')}/5")
                print(f"   Overall Score:        {evaluation.get('overall_score', 'N/A')}/5")
                
                # Show pass/fail
                if evaluation.get("passed", False):
                    print("🎉 STORY PASSED - Ready for user!")
                else:
                    print("🔄 STORY NEEDS REFINEMENT")
                    
                    # Get refinement instructions
                    instructions = judge.generate_refinement_instructions(evaluation)
                    print(f"\n🛠️  REFINEMENT INSTRUCTIONS:")
                    print(f"   {instructions}")
                
                # Show detailed feedback
                feedback = evaluation.get("feedback", {})
                if feedback:
                    print(f"\n💬 DETAILED FEEDBACK:")
                    for dimension, comment in feedback.items():
                        print(f"   {dimension}: {comment}")
                        
        except Exception as e:
            print(f"💥 ERROR: {e}")
        
        # Pause between tests
        if i < len(test_stories):
            input(f"\n✨ Press Enter to test the next story...")
    
    print("\n" + "=" * 60)
    print("✨ JudgeSystem test complete!")

if __name__ == "__main__":
    test_judge_system()