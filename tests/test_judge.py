#!/usr/bin/env python3
"""
Lightweight test script for JudgeSystem - Tests 3 story quality levels
"""

import os
import openai
from dotenv import load_dotenv
from agents.judge import JudgeSystem

load_dotenv()

def call_model(prompt: str, max_tokens=3000, temperature=0.1) -> str:
    """LLM call function with mock fallback"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai.api_key:
        return mock_response(prompt)
    
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
    if "SAFE for children" in prompt:
        return '{"passed": true, "issues": ""}'
    elif "EXPERT JUDGE" in prompt:
        if "Luna's Library Adventure" in prompt:
            return '''{"character_connection": 8.2, "bedtime_appropriate": 8.5, "storytelling_craft": 7.8, "age_appropriate": 8.1, "feedback": {"character_connection": "Strong child protagonist with clear goals", "bedtime_appropriate": "Good energy progression with peaceful ending", "storytelling_craft": "Engaging narrative with authentic voice", "age_appropriate": "Perfect complexity for target age"}}'''
        elif "Magic Adventure" in prompt:
            return '''{"character_connection": 3.2, "bedtime_appropriate": 2.8, "storytelling_craft": 2.5, "age_appropriate": 4.1, "feedback": {"character_connection": "Weak protagonist with no clear personality", "bedtime_appropriate": "Poor energy management, abrupt ending", "storytelling_craft": "Generic AI patterns, no authentic voice", "age_appropriate": "Too simple and predictable"}}'''
        else:
            return '''{"character_connection": 5.5, "bedtime_appropriate": 6.2, "storytelling_craft": 5.8, "age_appropriate": 6.0, "feedback": {"character_connection": "Adequate but needs more depth", "bedtime_appropriate": "Basic bedtime preparation", "storytelling_craft": "Simple structure", "age_appropriate": "Mostly appropriate"}}'''

def test_stories():
    """Test 3 stories: Good, Bad, Worst"""
    
    print("Testing Beanstalk AI JudgeSystem")
    print("=" * 50)
    
    judge = JudgeSystem(call_model)
    
    # Test stories
    stories = [
        {
            "title": "Luna's Library Adventure",
            "story": """Eight-year-old Maya had always been curious about the old library's mysterious back room. One quiet evening, as golden sunlight streamed through the tall windows, she discovered something magical behind the dusty astronomy books. A small purple dragon named Luna was carefully organizing books by the colors of their covers, creating beautiful rainbow patterns on the shelves. Luna looked up with sparkling eyes, initially shy about being discovered.
            
'I've been so lonely,' Luna whispered. 'I love books, but I've never had anyone to share stories with.' Maya's heart filled with warmth. She wasn't scared at all – Luna seemed like the most wonderful friend she could imagine. 'Would you like to read together?' Maya asked gently. Luna's face lit up with pure joy.

They spent the evening exploring magical tales about distant planets and friendly aliens, with Luna sharing fascinating facts about each story. As the library grew quiet and peaceful, Luna showed Maya her favorite cozy reading nook, complete with soft cushions and twinkling fairy lights. 'This is where I come to dream,' Luna said softly.

Maya promised to visit again soon, and Luna gave her a special bookmark that shimmered like starlight. Walking home under the gentle evening sky, Maya felt wonderfully happy knowing she had made such a special friend. That night, she drifted off to sleep thinking about all the magical stories she and Luna would discover together, feeling safe and loved and excited for tomorrow's adventures.""",
            "moral": "Friendship can be found in the most unexpected places, and kindness opens doors to wonderful adventures."
        },
        {
            "title": "Bob the Magic Kid",
            "story": """Bob was a kid. He liked stuff. One day Bob found a thing. It was magic or whatever. Bob used the thing and went to a place. There were other people there who were bad. Bob showed them the magic thing. He won because he had the thing. Then Bob went home. His mom asked where he was. Bob said nowhere. The end.""",
            "moral": "Hard work and kindness to nature bring wonderful rewards."
        },
        {
            "title": "The Magic Adventure",
            "story": """Once upon a time there was a little girl named Sarah. She was very curious and loved adventures. One day she found a magic wand in her backyard. The wand was shiny and had sparkles.

Sarah picked up the wand and suddenly everything changed. She could fly! She flew around her neighborhood and saw lots of things. Then she met a talking rabbit who told her about an evil wizard who was making everyone sad.

The rabbit said Sarah had to stop the wizard or else bad things would happen. Sarah was scared but she knew she had to be brave. She flew to the wizard's castle which was dark and scary.

When she got there, the wizard was casting a spell. Sarah pointed her wand at him and said "Stop being mean!" The wizard's spell bounced back at him and he turned into a nice person. Everyone was happy again.

Sarah flew home and told her mom about her adventure. Her mom said it was just a dream but Sarah knew it was real. She hid the wand under her bed for next time.""",
            "moral": "Always be brave and help others."
        }
    ]
    
    quality_labels = ["GOOD STORY", "AVERAGE STORY", "POOR STORY"]
    
    for i, (story, label) in enumerate(zip(stories, quality_labels)):
        print(f"\nTEST {i+1}: {label}")
        print("-" * 30)
        print(f"Title: {story['title']}")
        print(f"Length: {len(story['story'].split())} words")
        
        try:
            evaluation = judge.evaluate_story(story)
            
            # Safety check
            if not evaluation.get("safety_passed", True):
                print("SAFETY: FAILED")
                print(f"Issues: {evaluation.get('safety_issues', 'Unknown')}")
                continue
            else:
                print("SAFETY: PASSED")
            
            # Length check
            length_check = evaluation.get("length_check", {})
            read_time = length_check.get("estimated_read_time", 0)
            acceptable = length_check.get("acceptable", False)
            
            # Quality scores
            print("\nSCORES:")
            dimensions = [
                ("character_connection", "Character Connection"),
                ("bedtime_appropriate", "Bedtime Appropriate"),
                ("storytelling_craft", "Storytelling Craft"),
                ("age_appropriate", "Age Appropriate")
            ]
            
            for dim_key, dim_name in dimensions:
                score = evaluation.get(dim_key, 0)
                print(f"  {dim_name}: {score}/10")
            
            overall = evaluation.get("overall_score", 0)
            passed = evaluation.get("passed", False)
            print(f"  Overall Score: {overall}/10")
            
        except Exception as e:
            print(f"ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("Test complete")

if __name__ == "__main__":
    test_stories()