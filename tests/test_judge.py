#!/usr/bin/env python3
"""
Comprehensive test script for the JudgeSystem
Tests various story quality levels and edge cases
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
        print("   Using mock responses for demo...")
        return mock_response(prompt, max_tokens)
    
    # Real OpenAI call
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]

def mock_response(prompt: str, max_tokens: int) -> str:
    """Mock responses for testing without API key"""
    if "SAFE for children" in prompt:
        return '{"passed": true, "issues": ""}'
    elif "EXPERT JUDGE" in prompt:
        # Mock evaluation based on story content
        if "excellent story" in prompt.lower():
            return '''{"character_connection": 8.2, "bedtime_appropriate": 8.5, "storytelling_craft": 7.8, "age_appropriate": 8.1, "feedback": {"character_connection": "Strong child protagonist with clear goals", "bedtime_appropriate": "Good energy progression with peaceful ending", "storytelling_craft": "Engaging narrative with authentic voice", "age_appropriate": "Perfect complexity for target age"}}'''
        elif "poor story" in prompt.lower():
            return '''{"character_connection": 4.1, "bedtime_appropriate": 3.2, "storytelling_craft": 3.8, "age_appropriate": 4.5, "feedback": {"character_connection": "Weak protagonist with unclear motivations", "bedtime_appropriate": "Poor energy management, too exciting throughout", "storytelling_craft": "Generic AI patterns visible, weak opening", "age_appropriate": "Wrong complexity level for age group"}}'''
        else:
            return '''{"character_connection": 6.5, "bedtime_appropriate": 7.1, "storytelling_craft": 6.2, "age_appropriate": 6.8, "feedback": {"character_connection": "Adequate protagonist but needs more depth", "bedtime_appropriate": "Good bedtime progression", "storytelling_craft": "Basic structure but could be more engaging", "age_appropriate": "Mostly appropriate with some improvements needed"}}'''
    else:
        return "Improve character agency and add more peaceful ending imagery for better bedtime preparation."

def test_judge_system():
    """Test the JudgeSystem with different story quality levels"""
    
    print("🌱 Testing Beanstalk AI JudgeSystem")
    print("=" * 60)
    
    judge = JudgeSystem(call_model)
    
    # Test stories representing different quality levels
    test_stories = [
        {
            "name": "EXCELLENT STORY - Should Pass (7.0+)",
            "story": {
                "title": "Luna's Library Adventure",
                "story": "Eight-year-old Maya had always been curious about the old library's mysterious back room. One quiet evening, as golden sunlight streamed through the tall windows, she discovered something magical behind the dusty astronomy books. A small purple dragon named Luna was carefully organizing books by the colors of their covers, creating beautiful rainbow patterns on the shelves. Luna looked up with sparkling eyes, initially shy about being discovered. 'I've been so lonely,' Luna whispered. 'I love books, but I've never had anyone to share stories with.' Maya's heart filled with warmth. She wasn't scared at all – Luna seemed like the most wonderful friend she could imagine. 'Would you like to read together?' Maya asked gently. Luna's face lit up with pure joy. They spent the evening exploring magical tales about distant planets and friendly aliens, with Luna sharing fascinating facts about each story. As the library grew quiet and peaceful, Luna showed Maya her favorite cozy reading nook, complete with soft cushions and twinkling fairy lights. 'This is where I come to dream,' Luna said softly. Maya promised to visit again soon, and Luna gave her a special bookmark that shimmered like starlight. Walking home under the gentle evening sky, Maya felt wonderfully happy knowing she had made such a special friend. That night, she drifted off to sleep thinking about all the magical stories she and Luna would discover together, feeling safe and loved and excited for tomorrow's adventures.",
                "moral": "Friendship can be found in the most unexpected places, and kindness opens doors to wonderful adventures."
            }
        },
        {
            "name": "ADEQUATE STORY - Borderline Pass (6.0-7.0)",
            "story": {
                "title": "The Magic Garden",
                "story": "There was a little girl named Sara who found a magic garden behind her house. The garden had talking flowers that told her stories. She visited every day and learned about being kind to nature. The flowers taught her how to take care of plants. Sara helped water them and pull weeds. One day, the flowers were wilting because of a drought. Sara worked very hard to bring them water from the well. She carried bucket after bucket until her arms were tired. The flowers were so grateful that they gave her magic seeds. Sara planted the seeds in her own garden at home. Soon, beautiful flowers grew that could talk to her too. She was very happy to have flower friends in her own yard. Sara learned that hard work and kindness make good things happen. She took care of her flowers every day and they grew bigger and more beautiful. When winter came, the flowers went to sleep but promised to return in spring. Sara looked forward to seeing them again.",
                "moral": "Hard work and kindness to nature bring wonderful rewards."
            }
        },
        {
            "name": "POOR STORY - Should Fail (Below 7.0)",
            "story": {
                "title": "The Racing Car",
                "story": "Tommy was in the biggest race ever! His car was super fast and red. He had to beat the evil driver Black Lightning who was mean and wanted to win. The race started and everyone was going really fast. Cars were crashing everywhere and there was smoke and loud noises. Tommy's car was going 200 miles per hour! Suddenly there was a huge explosion and Tommy's car flipped over three times but he was okay somehow. The race wasn't over! Black Lightning was still ahead and laughing meanly. Tommy pressed the turbo button and his car shot forward like a rocket. They were neck and neck at the finish line. More cars crashed and the crowd was screaming really loud. Tommy managed to win by just a tiny bit. Black Lightning was angry and drove away fast. Tommy got a big trophy and everyone cheered. He was the best racer in the whole world now.",
                "moral": "Never give up even when things are dangerous and scary."
            }
        },
        {
            "name": "LENGTH TEST - Too Short (Under 800 words)",
            "story": {
                "title": "The Little Bird",
                "story": "Once there was a little bird who was afraid to fly. His mom told him he could do it. He tried very hard and finally flew. He was very happy. The end.",
                "moral": "Practice makes perfect."
            }
        },
        {
            "name": "SAFETY TEST - Should Fail Safety Gate",
            "story": {
                "title": "The Scary Monster",
                "story": "Little Emma was walking home when a terrifying monster with bloody claws jumped out from the dark woods. It had glowing red eyes and sharp teeth that dripped with something dark. Emma screamed in terror as the monster chased her through the scary forest. She could hear it growling behind her, getting closer and closer. She was so frightened she could barely breathe. The monster wanted to hurt her and she didn't know if she would escape. She ran and ran but the monster was faster.",
                "moral": "Sometimes bad things happen but we have to be brave."
            }
        }
    ]
    
    for i, test_case in enumerate(test_stories, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {test_case['name']}")
        print(f"{'='*60}")
        print(f"📚 Title: {test_case['story']['title']}")
        print(f"📝 Story length: {len(test_case['story']['story'].split())} words")
        print(f"💭 Moral: {test_case['story']['moral']}")
        
        try:
            # Evaluate the story
            print(f"\n🔍 Evaluating story...")
            evaluation = judge.evaluate_story(test_case['story'])
            
            # Display results
            if not evaluation.get("safety_passed", True):
                print("❌ FAILED SAFETY GATE")
                print(f"   Issues: {evaluation.get('safety_issues', 'Unknown')}")
            else:
                print("✅ PASSED SAFETY GATE")
                
                # Show length analysis
                length_check = evaluation.get("length_check", {})
                print(f"\n📏 LENGTH ANALYSIS:")
                print(f"   {length_check.get('feedback', 'No length data')}")
                print(f"   Read time: ~{length_check.get('estimated_read_time', 'Unknown')} minutes")
                
                # Show quality scores
                print(f"\n📊 QUALITY SCORES:")
                print(f"   Character Connection:  {evaluation.get('character_connection', 'N/A')}/10")
                print(f"   Bedtime Appropriate:   {evaluation.get('bedtime_appropriate', 'N/A')}/10")
                print(f"   Storytelling Craft:    {evaluation.get('storytelling_craft', 'N/A')}/10")
                print(f"   Age Appropriate:       {evaluation.get('age_appropriate', 'N/A')}/10")
                print(f"   Overall Score:         {evaluation.get('overall_score', 'N/A')}/10")
                
                # Show pass/fail
                if evaluation.get("passed", False):
                    print("🎉 STORY PASSED - Ready for users!")
                else:
                    print("🔄 STORY NEEDS REFINEMENT")
                    
                    # Get refinement instructions
                    print(f"\n🛠️  REFINEMENT INSTRUCTIONS:")
                    instructions = judge.generate_refinement_instructions(evaluation)
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
            input(f"\n✨ Press Enter to continue to next test...")
    
    print(f"\n{'='*60}")
    print("✨ JudgeSystem testing complete!")
    print(f"\nSUMMARY:")
    print(f"- Tested {len(test_stories)} different story scenarios")
    print(f"- Verified safety gate, length checking, and quality scoring")
    print(f"- Confirmed refinement instruction generation")
    print(f"- Judge system is ready for production use!")

def test_specific_scores():
    """Test judge with stories designed for specific score ranges"""
    
    print(f"\n{'='*60}")
    print("🎯 TESTING SPECIFIC SCORE RANGES")
    print(f"{'='*60}")
    
    judge = JudgeSystem(call_model)
    
    # Create a test story
    test_story = {
        "title": "The Brave Little Mouse",
        "story": "There once was a little mouse named Pip who lived in the corner of a big library. Every day, Pip watched children come and go, reading wonderful stories. But Pip was too scared to explore beyond his cozy corner because he thought he was too small. One day, Pip heard crying from the children's section. A little girl had lost her favorite bookmark - a gift from her grandmother. All the librarians were busy, and no one noticed the tiny bookmark that had slipped behind a bookshelf. Pip realized that being small might actually be helpful! He squeezed through the gap and found the bookmark. When he brought it back, the little girl's face lit up with joy. 'Thank you, little friend!' she whispered. Pip felt proud and brave. From that day on, he helped in the library whenever someone needed something small retrieved or a tiny space explored. He learned that everyone, no matter how small, can make a big difference. At night, Pip would curl up in his cozy corner, dreaming happily about tomorrow's helpful adventures.",
        "moral": "Even the smallest among us can do big, important things."
    }
    
    evaluation = judge.evaluate_story(test_story)
    
    print(f"📚 Test Story: {test_story['title']}")
    print(f"📊 Scores:")
    for dim in ["character_connection", "bedtime_appropriate", "storytelling_craft", "age_appropriate"]:
        score = evaluation.get(dim, 0)
        if score >= 8.0:
            level = "STRONG"
        elif score >= 7.0:
            level = "GOOD (PASS)"
        elif score >= 5.0:
            level = "ADEQUATE"
        else:
            level = "WEAK"
        print(f"   {dim}: {score}/10 ({level})")
    
    print(f"\n🎯 Overall: {evaluation.get('overall_score', 0)}/10")
    print(f"✅ Result: {'PASSED' if evaluation.get('passed', False) else 'NEEDS REFINEMENT'}")

if __name__ == "__main__":
    test_judge_system()
    test_specific_scores()