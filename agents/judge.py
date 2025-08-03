import json
from typing import Dict, Callable
from utils.prompts import JudgePrompts

class JudgeSystem:
    """
    Research-backed bedtime story evaluation system with detailed 10-point rubric
    and optimal length checking for 8-minute read time.
    """
    
    def __init__(self, llm_call_function: Callable):
        self.call_model = llm_call_function
        
        # Research-based scoring weights
        self.weights = {
            "character_connection": 0.30,
            "bedtime_appropriate": 0.25,
            "storytelling_craft": 0.25,
            "age_appropriate": 0.20
        }
        
        # Quality thresholds
        self.pass_threshold = 7.0      # Must achieve 7.0+ to pass
        self.bedtime_floor = 6.0       # Bedtime score cannot be below 6.0
        self.dimension_floor = 4.0     # No dimension can be below 4.0
        
        # Length parameters for ~8 minute read
        self.target_word_count = 1000  # Ideal length
        self.min_word_count = 800      # Minimum acceptable
        self.max_word_count = 1200     # Maximum acceptable
        self.reading_speed = 125       # Words per minute (bedtime pace)
    
    def evaluate_story(self, story: Dict) -> Dict:
        """
        Evaluate story using detailed 10-point rubric with length and safety checks.
        
        Args:
            story: {"title": str, "story": str, "moral": str}
            
        Returns:
            {
                "safety_passed": bool,
                "character_connection": float (1-10),
                "bedtime_appropriate": float (1-10), 
                "storytelling_craft": float (1-10),
                "age_appropriate": float (1-10),
                "overall_score": float (1-10),
                "length_check": dict,
                "passed": bool,
                "feedback": dict,
                "safety_issues": str (if safety failed)
            }
        """
        
        # Step 1: Length Analysis
        length_analysis = self._analyze_length(story)
        
        # Step 2: Safety Gate
        safety_result = self._evaluate_safety(story)
        if not safety_result["passed"]:
            return {
                "safety_passed": False,
                "safety_issues": safety_result["issues"],
                "length_check": length_analysis,
                "passed": False,
                "overall_score": 0.0
            }
        
        # Step 3: Quality Evaluation
        evaluation_prompt = JudgePrompts.detailed_evaluation_prompt(story, length_analysis)
        
        try:
            response = self.call_model(evaluation_prompt, max_tokens=1400, temperature=0.1)
            evaluation = json.loads(response)
            
            # Calculate weighted overall score
            overall_score = sum(
                evaluation[dimension] * weight 
                for dimension, weight in self.weights.items()
                if dimension in evaluation
            )
            
            # Apply pass conditions
            bedtime_score = evaluation.get("bedtime_appropriate", 0)
            all_dimensions_pass = all(
                evaluation.get(dim, 0) >= self.dimension_floor 
                for dim in self.weights.keys()
            )
            
            passed = (overall_score >= self.pass_threshold and 
                     bedtime_score >= self.bedtime_floor and
                     all_dimensions_pass and
                     length_analysis["acceptable"])
            
            evaluation.update({
                "safety_passed": True,
                "overall_score": round(overall_score, 2),
                "length_check": length_analysis,
                "passed": passed
            })
            
            return evaluation
            
        except (json.JSONDecodeError, ValueError, KeyError):
            return self._fallback_evaluation(story, length_analysis)
    
    def _analyze_length(self, story: Dict) -> Dict:
        """Analyze story length for optimal 8-minute reading time."""
        
        story_text = story.get("story", "")
        word_count = len(story_text.split())
        estimated_read_time = word_count / self.reading_speed
        
        # Determine if length is acceptable
        acceptable = self.min_word_count <= word_count <= self.max_word_count
        
        # Generate length feedback
        if word_count < self.min_word_count:
            length_feedback = f"Too short ({word_count} words, ~{estimated_read_time:.1f} min). Need {self.target_word_count} words for ~8 min read."
        elif word_count > self.max_word_count:
            length_feedback = f"Too long ({word_count} words, ~{estimated_read_time:.1f} min). Target {self.target_word_count} words for ~8 min read."
        else:
            length_feedback = f"Perfect length ({word_count} words, ~{estimated_read_time:.1f} min read time)."
        
        return {
            "word_count": word_count,
            "estimated_read_time": round(estimated_read_time, 1),
            "acceptable": acceptable,
            "feedback": length_feedback,
            "target_range": f"{self.min_word_count}-{self.max_word_count} words"
        }
    
    def _evaluate_safety(self, story: Dict) -> Dict:
        """Safety gate evaluation using LLM intelligence."""
        
        safety_prompt = JudgePrompts.safety_evaluation_prompt(story)
        
        try:
            response = self.call_model(safety_prompt, max_tokens=300, temperature=0.1)
            result = json.loads(response)
            return result
            
        except (json.JSONDecodeError, ValueError, KeyError):
            # Conservative fallback - assume unsafe if we can't evaluate
            return {
                "passed": False,
                "issues": "Unable to evaluate safety - LLM assessment required for content approval"
            }
    
    def _fallback_evaluation(self, story: Dict, length_analysis: Dict) -> Dict:
        """Conservative fallback when LLM evaluation fails."""
        
        return {
            "safety_passed": True,
            "character_connection": 5.0,
            "bedtime_appropriate": 5.0,
            "storytelling_craft": 4.5,
            "age_appropriate": 5.0,
            "overall_score": 4.9,
            "length_check": length_analysis,
            "passed": False,  # Conservative - require proper evaluation to pass
            "feedback": {
                "character_connection": "Unable to evaluate - system fallback. Story needs LLM assessment.",
                "bedtime_appropriate": "Unable to evaluate - system fallback. Story needs LLM assessment.", 
                "storytelling_craft": "Unable to evaluate - system fallback. Story needs LLM assessment.",
                "age_appropriate": "Unable to evaluate - system fallback. Story needs LLM assessment."
            }
        }