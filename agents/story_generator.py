import json
from typing import Dict, Callable
from utils.prompts import StoryGenerationPrompts

class StoryGenerator:
   """Story generator with two-phase approach"""
   
   def __init__(self, llm_call_function: Callable):
       self.call_model = llm_call_function
   
   def _clean_json(self, text: str) -> Dict:
    """Parse JSON from LLM response, preserving newlines"""
    text = text.strip()
    if text.startswith('```json'):
        text = text[7:]
    if text.endswith('```'):
        text = text[:-3]
    
    # Fix JSON syntax issues
    text = text.replace(',]', ']').replace(',}', '}')
    
    # Parse JSON
    result = json.loads(text)
    
    # Ensure story has proper paragraph breaks
    if isinstance(result, dict) and 'story' in result:
        story = result['story']
        
        # If story lacks paragraph breaks, add them intelligently
        if '\n\n' not in story and len(story) > 100:
            # Split on sentence boundaries that likely indicate new paragraphs
            sentences = story.split('. ')
            
            # Rebuild with paragraph breaks at logical points
            paragraphs = []
            current_paragraph = []
            
            for i, sentence in enumerate(sentences):
                # Add sentence to current paragraph
                current_paragraph.append(sentence + ('.' if not sentence.endswith('.') else ''))
                
                # Start new paragraph after 3-4 sentences or at scene changes
                if (len(current_paragraph) >= 3 or 
                    any(marker in sentence for marker in ['One day', 'That night', 'Suddenly', 'The next', 'Later'])):
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
            
            # Add any remaining sentences
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
            
            # Join with double newlines
            result['story'] = '\n\n'.join(paragraphs)
    
    return result
   
   def generate_story(self, story_request: str) -> tuple[Dict, Dict]:
       """Generate story and return both story and outline"""
       try:
           # Get outline
           outline = self._clean_json(
               self.call_model(
                   StoryGenerationPrompts.generate_outline_prompt(story_request),
                   max_tokens=1500,
                   temperature=0.7
               )
           )
           
           # Get story from outline
           story = self._clean_json(
               self.call_model(
                   StoryGenerationPrompts.write_story_from_outline_prompt(outline),
                   max_tokens=3000,
                   temperature=0.7
               )
           )
           
           return story, outline
           
       except:
           # Fallback
           return {
               "title": "A Magical Adventure",
               "story": "Once upon a time, there was a curious young explorer who discovered a hidden forest full of wonders...",
               "moral": "Every day holds the possibility of magic."
           }, {}
   
   def refine_story(self, story: Dict, outline: Dict, feedback: Dict) -> Dict:
       """Refine story using outline and feedback"""
       try:
           refined = self._clean_json(
               self.call_model(
                   StoryGenerationPrompts.story_refinement_prompt(story, feedback, outline),
                   max_tokens=3000,
                   temperature=0.3
               )
           )
           
           # Validate refined story has required fields
           if all(key in refined for key in ["title", "story", "moral"]):
               return refined
               
       except:
           pass
       
       return story  # Return original if refinement fails