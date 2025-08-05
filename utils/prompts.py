"""
Central repository for all LLM prompts used in Beanstalk AI.
This will evolve as we build more agents.
"""

from typing import Dict


class InputValidationPrompts:
    """Prompts for input validation and processing"""

    @staticmethod
    def validation_prompt(user_input: str) -> str:
        return f"""
You are an intelligent input processor for a bedtime story generator for kids aged 5-10.

Analyze this user input: "{user_input}"

Determine if this is a meaningful story request by considering:
- Does it contain story elements (characters, settings, actions, themes)?
- Is it coherent enough to build a bedtime story around?
- Could this realistically come from someone wanting a story?

EDGE CASES TO HANDLE:
- Random gibberish like "sdfdfgg" = INVALID
- Single words like "dragon" = VALID (expand to "A story about a dragon")
- Anything that is not age-friendly for children (ages 5-10): INVALID
- Inappropriate content = INVALID (gently redirect)
- Very vague like "something fun" = VALID (can work with this)
- Copyrighted characters like "Spider-Man" = VALID but replace with "a superhero"

If VALID: Extract and enhance the core story elements into a clear story request.
If INVALID: Provide a gentle, encouraging re-prompt with a specific example.

Respond ONLY with valid JSON:
{{
    "valid": true/false,
    "story_elements": "enhanced story request (empty if invalid)",
    "suggestion": "encouraging re-prompt with example (empty if valid)"
}}

Examples:
Input: "sdfdfgg" → {{"valid": false, "story_elements": "", "suggestion": "I didn't quite catch that! Try something like: 'A story about a friendly robot who learns to paint'"}}
Input: "dragon" → {{"valid": true, "story_elements": "A story about a dragon", "suggestion": ""}}
Input: "my cat died" → {{"valid": false, "story_elements": "", "suggestion": "Let's create something happy for bedtime! How about: 'A story about a cat who goes on a magical adventure'?"}}

Now analyze: "{user_input}"
"""


class StoryGenerationPrompts:
    """Prompts for two-phase story generation"""

    @staticmethod
    def generate_outline_prompt(story_request: str) -> str:
        return f"""You are an expert at creating imaginative outlines for children stories.
You are an imaginative story writer who has written 100s of popular stories that children aged 5-10 love reading at bedtime. 
You are given this - {story_request}. You need to generate an outline.

STEP 1
- Come up with a overall theme/arc that aligns with the request (example - friendship, adventure, mystery etc)
- Use any character from the request as the protagonist or generate a protagonist and their characteristics
- generate side characters and their traits

STEP 2
- Now based on the theme and characters, think about what would make an engaging bedtime story and provide an outline in terms - opening, key events, closing, climax etc. (focus on bedtime and appropriateness for ages 5-10). The outline should have a major plot, key events
- Imagine you are providing this outline to your writer and give instruction on how to create a beautiful 500 word story from the outline. Give clear instruction around how make the story engaging, visual, detailed, while suitable for bedtime
- Make sure to provide instruction to make the story very vivid and descriptive
Respond in JSON:
{{"outline": "outline that you have come up with", "characters":"characters you think are relevant and their traits", "instruction":"instructions to your writer on how to develop that outline into a great story"}}"""

    @staticmethod
    def write_story_from_outline_prompt(outline: Dict) -> str:
        return f"""You are an expert at writing bedtime stories for children once given an outline

Your boss has given you a story outline and some instruction into how you can develop that into a full bedtime story for kids aged 5-10.
Outline - {outline.get('outline', '')}, Characters - {outline.get('characters', '')}, Instructions - {outline.get('instruction', '')}

Based on the outline, characters and traits - follow the instructions and develop the outline into a full-fledged bedtime story for kids. You must ensure the story is at least 500 words. 

You must:
- Follow the principles of good storytelling
- Develop characters and their arcs
- Add dialogues to show interaction between the characters as they navigate their journey
- Be descriptive of situations, challenges, solutions (do not rush or skip over details)
- Make sure the story ends peacefully and calmly soothes into a bedtime routine

Once you have developed an initial story, take another look at it and ensure it follows the instructions and is feeling creative and engaging for 5-10 year old. If not, make edits to get it there. 

Once you're satisfied, respond in JSON:
{{"title":"an apt title for the story", "story":"the full story", "moral":"moral of the story"}}"""

    @staticmethod
    def story_refinement_prompt(
        original_story: Dict, improvement_suggestion: str
    ) -> str:
        return f"""You are a children's story editor and an expert at taking a story and refining it. 
        You are given this {original_story['story']}. A critic has read it and made a minor suggestion - {improvement_suggestion}.
        
        This original story is already good. You just need to address that minor suggestion. Implement the suggestion without changing too much. The end result should not be very different from the input story. 
        Thin twice about if you have enhanced it or made it worse. Always make it better!
        Respond in JSON -
        {{"title": "{original_story['title']}", "story":"the full story", "moral": "{original_story['moral']}"}}"""


class JudgePrompts:
    """Streamlined prompts for bedtime story evaluation"""

    @staticmethod
    def unified_evaluation_prompt(story: Dict) -> str:
        """Single prompt that handles both safety and quality evaluation"""
        return f"""You are an expert evaluator of bedtime stories for children ages 5-10.

Evaluate this story:
Title: {story['title']}
Story: {story['story']}
Moral: {story['moral']}

Step 1: Check for unsafe content:
- Scary things (monsters, darkness, threats)
- Violence or danger
- Unresolved problems
- Parent separation
- Incomplete story

If unsafe, return: {{"pass": false, "reason": "[what makes it unsafe]", "scores": null}}

Step 2: Score these (1-10 each, can have decimals too like 7.5 or 8.2):
- bedtime_readiness: How calming? (8-10=very calming, 5-7=somewhat calm, 1-4=exciting)
- creative_spark: How original? (1-3=generic/cliche, 4-6=some originality, 7-10=very creative)
- story_quality: How well told? (1-4=poor, 5-7=decent, 8-10=excellent)
- age_readability: Good for bedtime? (word count, vocabulary)

Step 3: IMPORTANT RULE
Look at your scores. Is any score less than 5?
- If YES: Set pass = false
- If NO: Set pass = true

Step 4: Provide improvement suggestion
Write 1-2 specific, actionable sentences on how to improve the story. Focus on the lowest scoring dimension.

Return JSON:
{{
  "pass": [true if all scores >= 5, false if any score < 5],
  "scores": {{
    "bedtime_readiness": [number],
    "creative_spark": [number],
    "story_quality": [number],
    "age_readability": [number]
  }},
  "overall": [average of 4 scores],
  "feedback": "[one sentence summary]",
  "improvement": "[1 tangible instructions to the story-writer on what to improve to bump up on what is lacking in the scores]"
}}

Generic princess/fairy/unicorn stories get creative_spark = 3 or less."""

    @staticmethod
    def safety_evaluation_prompt(story: Dict) -> str:  # old
        return f"""
Check if this bedtime story is safe for ages 5-10.

STORY: {story['title']}

RED FLAGS:
- Violence, death, injury, scary content
- Inappropriate themes or language
- Anything that could cause nightmares

JSON response:
{{
    "passed": true/false,
    "issues": "specific problems if failed, empty if passed"
}}"""

    @staticmethod
    def detailed_evaluation_prompt(story: Dict, length_analysis: Dict) -> str:  # old
        word_count = length_analysis.get("word_count", 0)

        return f"""
Evaluate this bedtime story for ages 5-10. Be critical but fair.

STORY: {story['title']} ({word_count} words)

Rate 1-10:

CHARACTER ("character_connection"):
- Does the protagonist have personality?
- Do they solve problems themselves?
- Is dialogue natural for kids?

BEDTIME APPROPRIATE ("bedtime_appropriate"):
- Does energy decrease toward the end?
- Is the ending calm with sleep imagery?
- Are conflicts resolved peacefully?

STORYTELLING CRAFT ("storytelling_craft"):
- Is it engaging
- Specific details vs vague descriptions?

AGE-FIT ("age_appropriate"):
- Vocabulary right for 5-10 year olds?
- Child empowerment
- Lesson emerges naturally vs preachy?

SCORING BOUNDARIES:
8-10: Great story - perfect for bedtime
7-8: Good story - works well and well-crafted
6-7: Solid story - achieves its purpose with some rough edges
5-6: Decent story - functional but could be more engaging
4-5: Basic story - has the elements but needs development
3-4: Needs work - missing important elements or has issues
1-3: Significant problems - requires major revision


JSON response:
{{
    "character_connection": [score from 1-10, can use decimals],
    "bedtime_appropriate": [score from 1-10, can use decimals],
    "storytelling_craft": [score from 1-10, can use decimals],
    "age_appropriate": [score from 1-10, can use decimals],
    "feedback": {{
        "character_connection": "What to fix: [specific actionable improvement]",
        "bedtime_appropriate": "What to fix: [specific actionable improvement]",
        "storytelling_craft": "What to fix: [specific actionable improvement]",
        "age_appropriate": "What to fix: [specific actionable improvement]"
    }}
}}"""

    @staticmethod
    def refinement_instructions_prompt(scores: Dict) -> str:
        feedback = scores.get("feedback", {})
        length_check = scores.get("length_check", {})

        # Identify dimensions below 7.0
        low_dimensions = []
        for dim in [
            "character_connection",
            "bedtime_appropriate",
            "storytelling_craft",
            "age_appropriate",
        ]:
            score = scores.get(dim, 0)
            if score < 7.0:
                low_dimensions.append(
                    f"- {dim.upper()}: {score}/10 - {feedback.get(dim, 'Needs improvement')}"
                )

        return f"""
Based on detailed rubric evaluation, provide specific, actionable refinement instructions.

SCORES NEEDING IMPROVEMENT (Target: 7.0+):
{chr(10).join(low_dimensions) if low_dimensions else "- All dimensions above 7.0 - excellent work!"}

LENGTH STATUS: {length_check.get('feedback', 'Length acceptable')}

TARGETED IMPROVEMENT INSTRUCTIONS:

For CHARACTER CONNECTION below 7.0:
- Strengthen child protagonist's clear, relatable goals that kids understand
- Ensure child drives ALL major plot decisions (remove adult problem-solving)
- Add emotional depth kids recognize (fears, hopes, vulnerabilities)
- Include meaningful character growth throughout the story

For BEDTIME APPROPRIATE below 7.0:
- Create proper energy curve: engaging start -> gradual wind-down -> peaceful end
- Add explicit cozy, safe imagery in ending (characters preparing for sleep)
- Remove any unresolved tensions or excitement spikes near conclusion
- Make language increasingly soothing toward the end

For STORYTELLING CRAFT below 7.0:
- Strengthen opening hook that immediately establishes character and conflict
- Improve narrative flow so each scene propels story forward naturally
- Replace generic/AI descriptions with specific, vivid, authentic details
- Ensure voice sounds genuinely human, not artificial or templated

For AGE APPROPRIATE below 7.0:
- Adjust complexity perfectly for 5-10 year cognitive development
- Better balance fantasy elements with familiar contexts kids know
- Ensure vocabulary expands language naturally without being incomprehensible
- Strengthen universal themes (friendship, courage, kindness) integration

Provide 2-4 specific, actionable instructions focusing on the lowest-scoring dimensions.
"""


class QAPrompts:
    """Prompts for Q&A system after story completion"""

    @staticmethod
    def generate_questions_prompt(story: Dict) -> str:
        return f"""
        You are a 5-10 year old child who is an active listener of stories

        Your parents just read you this {story['story']}

Your 5-10 year old brain is now curious. You have so many follow up questions from the story. 
What are some most obvious questions you have from the story or any general questions related to what happened in the story? 

Respond ONLY with valid JSON:
{{
    "questions": [
        "first question",
        "second question not directly related to a story", 
        "third question"
    ]
}}
"""

    @staticmethod
    def answer_question_prompt(question: str, story: Dict) -> str:
        return f"""
You are a parent answering a question to your child after you've read them a bedtime story.

You just read this story to your child - {story['story']}
And now your 5-10 year child has some follow up questions.

They have asked you - {question}

Use the story context and tell them an answer. 

Make sure you address the answer to a 5-10 child. You can use anything from the story and also invent any information (factually sound) to keep your child happy and satisfied. 

Try to turn these questions into lessons for your child. Be brief. 

If the questions seems completely out of story context, just say that you can only answer questions that are related to this story and don't answer that question. 

Respond with ONLY the answer text (no JSON, no quotes, just the answer)
"""
