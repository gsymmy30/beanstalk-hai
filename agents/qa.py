import json
from typing import Dict, List, Callable
from utils.prompts import QAPrompts

class QAAgent:
    """
    Post-story Q&A that generates contextual example questions 
    and answers children's curiosity about the story.
    """
    
    def __init__(self, llm_call_function: Callable):
        self.call_model = llm_call_function

    def generate_question_opportunities(self, story: Dict) -> List[str]:
        """
        Generate 3 example questions that would be interesting for kids to ask
        about this specific story.
        
        Args:
            story: {"title": str, "story": str, "moral": str}
            
        Returns:
            List of 3 engaging, story-specific example questions
        """
        # ref to the prompt library at utils/prompts.py
        question_prompt = QAPrompts.generate_questions_prompt(story)
        try:
            response = self.call_model(question_prompt, max_tokens=400, temperature=0.3)
            result = json.loads(response)
            questions = result.get("questions", [])
            
            # taking 3
            if len(questions) >= 3:
                return questions[:3]
            elif len(questions) > 0:
                return questions
            else:
                return self._fallback_questions(story)
        except (json.JSONDecodeError, ValueError, KeyError):
            return self._fallback_questions(story)
    
    def answer_question(self, question: str, story_context: Dict) -> str:
        """
        Answer a child's question about the story in an age-appropriate,
        engaging way.
        
        Args:
            question: Child's question about the story
            story_context: The original story for context
            
        Returns:
            Age-appropriate answer that maintains the story's magic
        """
        # ref to the prompt library at utils/prompts.py
        answer_prompt = QAPrompts.answer_question_prompt(question, story_context)
        
        try:
            answer = self.call_model(answer_prompt, max_tokens=300, temperature=0.4)
            answer = answer.strip()
            if answer.startswith('"') and answer.endswith('"'):
                answer = answer[1:-1]
            return answer
            
        except Exception:
            return self._fallback_answer(question, story_context)
    
    def _fallback_questions(self, story: Dict) -> List[str]:
        return [
            "What was your favorite part of the story?",
            "What do you think happened next?", 
            "If you could be in the story, what would you do?"
        ]
    def _fallback_answer(self, question: str, story_context: Dict) -> str:
        return f"That's such a wonderful question! Based on our story, I think there could be many magical possibilities. What do you imagine the answer might be?"