import json
from typing import Dict, Callable
from utils.prompts import InputValidationPrompts

class InputHandler:
    """
    LLM-powered input validation that handles edge cases and weird inputs
    while maintaining minimal cognitive load for users.
    """
    
    def __init__(self, llm_call_function: Callable):
        self.call_model = llm_call_function
    
    def process_input(self, user_input: str) -> Dict:
        """
        Process user input using LLM to validate and enhance story requests.
        
        Args:
            user_input: Raw user input (could be anything!)
            
        Returns:
            {
                "valid": bool,
                "story_elements": str,  # Enhanced/cleaned version if valid
                "suggestion": str       # Re-prompt example if invalid
            }
        """
        
        # Handle empty/minimal input quickly
        if not user_input or len(user_input.strip()) < 2:
            return {
                "valid": False,
                "story_elements": "",
                "suggestion": "I need a bit more to work with! Try something like: 'A story about a brave mouse who lives in a library'"
            }
        
        # Use LLM to intelligently validate and process
        validation_prompt = InputValidationPrompts.validation_prompt(user_input)
        
        try:
            response = self.call_model(validation_prompt, max_tokens=300, temperature=0.1)
            result = json.loads(response)
            
            # Ensure we have all required fields
            if not all(key in result for key in ["valid", "story_elements", "suggestion"]):
                raise ValueError("Invalid response format")
                
            return result
            
        except (json.JSONDecodeError, ValueError, KeyError):
            # Simple fallback if LLM fails
            return {
                "valid": False,
                "story_elements": "",
                "suggestion": "Something went wrong! Please try again with a story idea like: 'A story about a curious cat who explores a magical garden'"
            }