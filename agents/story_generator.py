import json
from typing import Dict, Callable, Tuple
from utils.prompts import StoryGenerationPrompts


class StoryGenerator:

    def __init__(self, llm_call_function: Callable):
        self.call_model = llm_call_function

    def _clean_json(self, text: str) -> Dict:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]

        text = text.replace(",]", "]").replace(",}", "}")
        result = json.loads(text)

        if isinstance(result, dict) and "story" in result:
            story = result["story"]

            if "\n\n" not in story and len(story) > 100:
                sentences = story.split(". ")
                paragraphs = []
                current_paragraph = []

                for i, sentence in enumerate(sentences):
                    current_paragraph.append(
                        sentence + ("." if not sentence.endswith(".") else "")
                    )

                    if len(current_paragraph) >= 3 or any(
                        marker in sentence
                        for marker in [
                            "One day",
                            "That night",
                            "Suddenly",
                            "The next",
                            "Later",
                        ]
                    ):
                        paragraphs.append(" ".join(current_paragraph))
                        current_paragraph = []

                if current_paragraph:
                    paragraphs.append(" ".join(current_paragraph))

                result["story"] = "\n\n".join(paragraphs)

        return result

    def generate_story(self, story_request: str) -> Tuple[Dict, Dict]:
        try:
            # ref to the prompt library at utils/prompts.py
            outline = self._clean_json(
                self.call_model(
                    StoryGenerationPrompts.generate_outline_prompt(story_request),
                    max_tokens=1500,
                    temperature=0.7,
                )
            )
            
            story = self._clean_json(
                self.call_model(
                    StoryGenerationPrompts.write_story_from_outline_prompt(outline),
                    max_tokens=3000,
                    temperature=0.7,
                )
            )

            return story, outline

        except Exception as e:
            print(f"Error generating story: {e}")
            return {
                "title": "A Magical Adventure",
                "story": "Once upon a time, there was a curious young explorer who discovered a hidden forest full of wonders...",
                "moral": "Every day holds the possibility of magic.",
            }, {}

    def refine_story(self, story: Dict, improvement_suggestion: str) -> Dict:
        try:
            # ref to the prompt library at utils/prompts.py
            refined = self._clean_json(
                self.call_model(
                    StoryGenerationPrompts.story_refinement_prompt(
                        story, improvement_suggestion
                    ),
                    max_tokens=3000,
                    temperature=0.2,
                )
            )

            if all(key in refined for key in ["title", "story", "moral"]):
                return refined

        except Exception as e:
            print(f"Error refining story: {e}")

        return story
