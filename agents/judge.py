import json
from typing import Dict, Callable
from utils.prompts import JudgePrompts

class JudgeSystem:
    """
    Research-backed story evaluation system focused on creating amazing stories 
    that happen to be perfect for bedtime.
    """
    
    def __init__(self, llm_call_function: Callable):
        self.call_model = llm_call_function
        
        # Research-based scoring weights
        self.weights = {
            "narrative_excellence": 0.35,
            "story_authenticity": 0.25,
            "bedtime_flow": 0.25,
            "age_appropriate_wonder": 0.15
        }
        
        self.pass_threshold = 4.0
        self.bedtime_floor = 3.5  # Bedtime Flow must be at least 3.5
    
    def evaluate_story(self, story: Dict) -> Dict:
        """
        Evaluate story with safety gate + 4-dimensional quality scoring.
        
        Args:
            story: {"title": str, "story": str, "moral": str}
            
        Returns:
            {
                "safety_passed": bool,
                "narrative_excellence": float,
                "story_authenticity": float, 
                "bedtime_flow": float,
                "age_appropriate_wonder": float,
                "overall_score": float,
                "passed": bool,
                "feedback": Dict,
                "safety_issues": str (if safety failed)
            }
        """
        
        # Step 1: Safety Gate
        safety_result = self._evaluate_safety(story)
        if not safety_result["passed"]:
            return {
                "safety_passed": False,
                "safety_issues": safety_result["issues"],
                "passed": False,
                "overall_score": 0.0
            }
        
        # Step 2: Quality Evaluation
        evaluation_prompt = JudgePrompts.quality_evaluation_prompt(story)
        
        try:
            response = self.call_model(evaluation_prompt, max_tokens=1000, temperature=0.1)
            evaluation = json.loads(response)
            
            # Calculate weighted overall score
            overall_score = sum(
                evaluation[dimension] * weight 
                for dimension, weight in self.weights.items()
                if dimension in evaluation
            )
            
            # Check pass conditions
            bedtime_score = evaluation.get("bedtime_flow", 0)
            passed = (overall_score >= self.pass_threshold and 
                     bedtime_score >= self.bedtime_floor)
            
            evaluation.update({
                "safety_passed": True,
                "overall_score": round(overall_score, 2),
                "passed": passed
            })
            
            return evaluation
            
        except (json.JSONDecodeError, ValueError, KeyError):
            return self._fallback_evaluation(story)
    
    def needs_refinement(self, scores: Dict) -> bool:
        """Check if story needs refinement based on scores."""
        return not scores.get("passed", False)
    
    def generate_refinement_instructions(self, scores: Dict) -> str:
        """Generate specific improvement instructions based on evaluation."""
        
        refinement_prompt = JudgePrompts.refinement_instructions_prompt(scores)
        
        try:
            instructions = self.call_model(refinement_prompt, max_tokens=400, temperature=0.1)
            return instructions.strip()
            
        except Exception:
            return self._fallback_refinement_instructions(scores)
    
    def _evaluate_safety(self, story: Dict) -> Dict:
        """Safety gate evaluation - pass/fail only."""
        
        safety_prompt = JudgePrompts.safety_gate_prompt(story)
        
        try:
            response = self.call_model(safety_prompt, max_tokens=300, temperature=0.1)
            result = json.loads(response)
            return result
            
        except (json.JSONDecodeError, ValueError, KeyError):
            # Conservative fallback - assume safe unless obviously problematic
            story_text = story.get("story", "").lower()
            unsafe_words = ["die", "death", "kill", "blood", "scary", "terrifying", "nightmare"]
            
            if any(word in story_text for word in unsafe_words):
                return {
                    "passed": False,
                    "issues": "Story contains potentially unsafe content for bedtime"
                }
            
            return {"passed": True, "issues": ""}
    
    def _fallback_evaluation(self, story: Dict) -> Dict:
        """Simple fallback evaluation when LLM fails."""
        
        # Conservative fallback - assume average quality
        base_score = 3.0  # Below pass threshold to be safe
        
        return {
            "safety_passed": True,
            "narrative_excellence": base_score,
            "story_authenticity": base_score,
            "bedtime_flow": base_score,
            "age_appropriate_wonder": base_score,
            "overall_score": base_score,
            "passed": False,  # Conservative - require LLM evaluation to pass
            "feedback": {
                "narrative_excellence": "System fallback - LLM evaluation failed",
                "story_authenticity": "System fallback - LLM evaluation failed", 
                "bedtime_flow": "System fallback - LLM evaluation failed",
                "age_appropriate_wonder": "System fallback - LLM evaluation failed"
            }
        }
    
    def _fallback_refinement_instructions(self, scores: Dict) -> str:
        """Generate basic refinement instructions when LLM fails."""
        
        low_scores = []
        for dimension, score in scores.items():
            if isinstance(score, (int, float)) and score < 4.0:
                low_scores.append(dimension)
        
        if "bedtime_flow" in low_scores:
            return "Make the story start more engaging but wind down to a peaceful, cozy ending where characters feel safe and sleepy."
        elif "narrative_excellence" in low_scores:
            return "Strengthen the plot with more interesting events and let the child protagonist solve the main problem independently."
        elif "story_authenticity" in low_scores:
            return "Add more specific, vivid details and unique plot elements to make the story feel less generic and more engaging."
        else:
            return "Improve the story's appeal for children aged 5-10 with more age-appropriate challenges and empowering themes."