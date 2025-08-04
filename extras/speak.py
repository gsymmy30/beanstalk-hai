# extra/narrate_single.py
"""
Narrate a single story provided manually
"""

import os
from dotenv import load_dotenv
from narrator import SmartBedtimeNarrator

# Load environment variables
load_dotenv()


def narrate_single_story(story_dict):
    """
    Narrate a single story
    
    Args:
        story_dict: Dictionary with 'title', 'story', and 'moral' keys
    """
    try:
        narrator = SmartBedtimeNarrator()
        print(f"\n🌙 Narrating: {story_dict['title']}")
        
        audio_path = narrator.narrate_story(story_dict)
        print(f"\n✅ Success! Audio saved to: {audio_path}")
        return audio_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    # Example story - replace with your own
    my_story = {
        "title": "Paige's Winning Team",
      "story": "Once upon a time in a small town, there lived a lively seven-year-old girl named Paige. Paige was known for her boundless energy and love for playing football. She was the captain of her team, which consisted of her loyal friends, Rex the dog and Sandy the squirrel.\n\nOne sunny afternoon, Paige and her friends gathered on the field, discussing the upcoming game. 'I can't wait to show off our new skills,' Paige exclaimed, her eyes shining with excitement.\n\nHowever, their team was facing a dilemma - they needed a new coach. Paige and her friends searched high and low for someone to lead their team, but no one seemed interested. Determined to find a coach, Paige decided to take matters into her own hands.\n\n'Let's organize tryouts for a new coach,' Paige suggested to Rex and Sandy. They put up posters around town and spread the word, hoping to find someone willing to take on the role. As the day of the tryouts arrived, Paige was feeling nervous but hopeful.\n\nMany people showed up to audition, but none of them seemed quite right for the job. Just when Paige was starting to lose hope, a retired football player named Coach Jake stepped forward. 'I saw your posters and I'd love to help out,' he said with a warm smile.\n\nPaige and her friends were thrilled to have found their new coach. With Coach Jake leading the team, they began practicing diligently. They worked on their skills and strategies, determined to improve and win their next game.\n\nThe day of the big game arrived, and Paige's team was ready. They played their hearts out, using everything they had learned from Coach Jake. In the end, they emerged victorious, with cheers and celebrations filling the air.\n\nPaige and her friends were overjoyed with their win, proud of what they had accomplished together. That night, they gathered around a bonfire, roasting marshmallows and sharing stories of their victory.\n\nAs the night grew darker, Paige felt a sense of peace and contentment wash over her. She knew that with perseverance and teamwork, anything was possible. With a smile on her face, she bid goodnight to her friends and settled into bed.\n\n'What a great day,' Paige whispered to Rex and Sandy, who snuggled close. 'We make a great team.' As she closed her eyes, the events of the day played out in her mind, filling her with a sense of pride and accomplishment. Slowly, she drifted off to sleep, the gentle sounds of the night lulling her into a peaceful slumber.",
      "moral": "The importance of perseverance and working together is highlighted in this story. Paige and her friends faced obstacles but overcame them through teamwork and determination. By staying focused and supporting each other, they were able to achieve their goal of finding a new coach and winning their game. The story serves as a reminder that with hard work and collaboration, success is within reach.",
    }
    
    # Narrate the story
    narrate_single_story(my_story)