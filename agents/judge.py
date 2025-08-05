import json
from typing import Dict, Callable
from utils.prompts import JudgePrompts


class JudgeSystem:

    def __init__(self, llm_call_function: Callable):
        self.call_model = llm_call_function
        self.pass_threshold = 5.0
        self.min_word_count = 500
        self.max_word_count = 800
        self.reading_speed = 125

    def evaluate_story(self, story: Dict) -> Dict:
        length_analysis = self._analyze_length(story)

        # ref to the prompt library at utils/prompts.py
        evaluation_prompt = JudgePrompts.unified_evaluation_prompt(story)

        try:
            response = self.call_model(
                evaluation_prompt, max_tokens=1000, temperature=0.3
            )
            evaluation = json.loads(response)

            if not evaluation.get("pass", False) and evaluation.get("scores") is None:
                return {
                    "pass": False,
                    "safety_passed": False,
                    "reason": evaluation.get("reason", "Safety concerns"),
                    "scores": None,
                    "overall": 0.0,
                    "feedback": evaluation.get("reason", "Story failed safety check"),
                    "improvement": evaluation.get("improvement", ""),
                    "length_check": length_analysis,
                }

            scores = evaluation.get("scores", {})
            overall = evaluation.get("overall", 0.0)

            all_scores_pass = all(
                scores.get(dim, 0) >= self.pass_threshold
                for dim in [
                    "bedtime_readiness",
                    "creative_spark",
                    "story_quality",
                    "age_readability",
                ]
            )

            return {
                "pass": evaluation.get("pass", False) and all_scores_pass,
                "safety_passed": True,
                "scores": scores,
                "overall": evaluation.get("overall", 0.0),
                "feedback": evaluation.get("feedback", ""),
                "improvement": evaluation.get("improvement", ""),
                "length_check": length_analysis,
            }

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error parsing evaluation response: {e}")
            return self._fallback_evaluation(story, length_analysis)

    def _analyze_length(self, story: Dict) -> Dict:
        story_text = story.get("story", "")
        word_count = len(story_text.split())
        estimated_read_time = word_count / self.reading_speed
        acceptable = self.min_word_count <= word_count <= self.max_word_count

        return {
            "word_count": word_count,
            "estimated_read_time": round(estimated_read_time, 1),
            "acceptable": acceptable,
            "target_range": f"{self.min_word_count}-{self.max_word_count} words",
            "feedback": self._get_length_feedback(word_count),
        }

    def _get_length_feedback(self, word_count: int) -> str:
        if word_count < self.min_word_count:
            return f"Too short ({word_count} words). Aim for {self.min_word_count}-{self.max_word_count} words for a 5-7 minute bedtime read."
        elif word_count > self.max_word_count:
            return f"Too long ({word_count} words). Aim for {self.min_word_count}-{self.max_word_count} words to keep bedtime routine on track."
        else:
            return f"Good length ({word_count} words) for bedtime reading."

    def _fallback_evaluation(self, story: Dict, length_analysis: Dict) -> Dict:
        return {
            "pass": False,
            "safety_passed": True,
            "scores": {
                "bedtime_readiness": 4.0,
                "creative_spark": 4.0,
                "story_quality": 4.0,
                "age_readability": 4.0,
            },
            "overall": 4.0,
            "feedback": "Unable to evaluate - system fallback. Story needs manual review.",
            "improvement": "Story is excellent as is.",
            "length_check": length_analysis,
        }
