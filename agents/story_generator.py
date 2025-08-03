import json
from typing import Dict, Callable
from utils.prompts import StoryGenerationPrompts

class StoryGenerator:
    """
    Core story generation agent that creates engaging, varied bedtime stories
    with proper titles and morals.
    """
    
    def __init__(self, llm_call_function: Callable):
        self.call_model = llm_call_function
    
    def generate_story(self, story_request: str) -> Dict:
        """
        Generate a complete bedtime story with title, narrative, and moral.
        
        Args:
            story_request: Processed story request from InputHandler
            
        Returns:
            {
                "title": str,
                "story": str,
                "moral": str
            }
        """
        
        generation_prompt = StoryGenerationPrompts.complete_story_prompt(story_request)
        
        try:
            response = self.call_model(generation_prompt, max_tokens=1200, temperature=0.7)
            result = json.loads(response)
            
            # Ensure we have all required fields
            if not all(key in result for key in ["title", "story", "moral"]):
                raise ValueError("Invalid story format")
                
            return result
            
        except (json.JSONDecodeError, ValueError, KeyError):
            # Fallback story if LLM fails
            return self._create_fallback_story(story_request)
    
    def refine_story(self, original_story: Dict, refinement_instructions: str) -> Dict:
        """
        Refine an existing story based on judge feedback.
        
        Args:
            original_story: The story to improve
            refinement_instructions: Specific improvements needed
            
        Returns:
            Improved story with same structure
        """
        
        refinement_prompt = StoryGenerationPrompts.refinement_prompt(
            original_story, refinement_instructions
        )
        
        try:
            response = self.call_model(refinement_prompt, max_tokens=1200, temperature=0.6)
            result = json.loads(response)
            
            if not all(key in result for key in ["title", "story", "moral"]):
                raise ValueError("Invalid refined story format")
                
            return result
            
        except (json.JSONDecodeError, ValueError, KeyError):
            # Return original if refinement fails
            return original_story
    
    def _create_fallback_story(self, story_request: str) -> Dict:
        """Simple fallback story when LLM completely fails."""
        
        return {
            "title": "A Magical Adventure",
            "story": f"Once upon a time, there was a kind and curious child who loved adventures. One evening, they discovered something wonderful that led to an amazing journey filled with friendship and joy. After their adventure, they returned home feeling happy and safe, ready for sweet dreams.",
            "moral": "Every day holds the possibility of magic and wonder."
        }