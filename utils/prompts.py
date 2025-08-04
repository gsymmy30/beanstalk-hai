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
        return f"""
Create a bedtime story outline for ages 5-10 based on: "{story_request}"

Design a story with:
- The protagonist from "{story_request}" (age 5-10 or equivalent in their species)
- EXACTLY 2 helper characters (no more, no less)
- A problem that needs solving
- EXACTLY 3 key events
- Concrete actions leading to resolution
- Leading to peaceful sleep

Return this EXACT JSON structure with ALL fields filled:

{{
    "protagonist": {{
        "name": "character name",
        "age": "5-10 or young [species]",
        "personality": "key trait",
        "type": "human/dragon/mouse/etc"
    }},
    "helpers": [
        {{"name": "first helper", "type": "species", "role": "their role"}},
        {{"name": "second helper", "type": "species", "role": "their role"}}
    ],
    "setting": "location",
    "conflict": "problem",
    "key_events": [
        "first event",
        "second event",
        "third event"
    ],
    "journey": "what happens",
    "resolution": "how it ends peacefully",
    "theme": "lesson"
}}

Return ONLY the complete JSON above with your content filled in. No explanations.
"""

    @staticmethod
    def write_story_from_outline_prompt(outline: Dict) -> str:
        protagonist = outline.get('protagonist', {})
        helpers = ', '.join([f"{h['name']} the {h['type']}" for h in outline.get('helpers', [])])
        
        return f"""
Write a complete 800-word bedtime story based on this outline:

MAIN CHARACTER: {protagonist.get('name')}, age {protagonist.get('age')}, who is {protagonist.get('personality')}
FRIENDS: {helpers}
SETTING: {outline.get('setting')}
PROBLEM: {outline.get('conflict')}
KEY EVENTS: {outline.get('key_events', outline.get('magical_events', []))}
WHAT HAPPENS: {outline.get('journey')}
ENDING: {outline.get('resolution')}
THEME: {outline.get('theme')}

STORY REQUIREMENTS:
• Show SPECIFIC things happening with visual details
• Include the key events with concrete descriptions
• Keep the story ACTIVE - show characters doing things
• Natural dialogue between characters  
• Gradual calming: exciting events → gentler activities → peaceful sleep
• eventful story - innovative
• Final paragraphs: calm bedtime activities (not abstract feelings)
• Exactly 800 words

AVOID:
• Vague descriptions ("something wonderful happened")
• Too many feeling words ("heart swelled", "filled with joy")
• Abstract endings - show actual bedtime routines/activities
• Rushing through events - develop each one properly

Write an engaging story where interesting things actually happen. Show actions and consequences.

JSON response:
{{
    "title": "story title",
    "story": "complete 800-word story",
    "moral": "catchy moral of the story"
}}
REMINDER: Return ONLY valid JSON.
"""

    @staticmethod
    def story_refinement_prompt(original_story: Dict, judge_feedback: Dict, outline: Dict = None) -> str:
        feedback_lines = []
        feedback_dict = judge_feedback.get('feedback', {})
        for dim, feedback in feedback_dict.items():
            if feedback and isinstance(feedback, str):
                feedback_lines.append(f"• {feedback}")
        feedback_text = '\n'.join(feedback_lines) if feedback_lines else "• Enhance character personality\n• Add more sensory details"
        original_word_count = len(original_story['story'].split())
        return f"""
You are a master editor. Edit this bedtime story to address the feedback below.

ORIGINAL STORY: "{original_story['story']}"

FEEDBACK TO ADDRESS:
{feedback_text}

ADD DIALOGUE throughout the story - characters should talk to each other! Replace narration with conversation where possible

EXPANSION REQUIREMENTS:
1. ADD more details to existing scenes - don't remove anything
2. EXPAND character thoughts and feelings
3. EXTEND descriptions with sensory details (sights, sounds, smells)
4. DEVELOP dialogue - make conversations more natural and detailed (more back and forth)
5. ENHANCE transitions between scenes
6. ELABORATE on the setting and atmosphere

DO NOT: Summarize, condense, or remove any content. Only ADD and ENHANCE.

JSON response:
{{
    "title": "{original_story['title']}",
    "story": "[edited story with improvements]",
    "moral": "{original_story['moral']}",
    "improvements": "A brief summary of what was improved"
}}"""


class JudgePrompts:
    """Streamlined prompts for bedtime story evaluation"""
    
    @staticmethod
    def safety_evaluation_prompt(story: Dict) -> str:
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
    def detailed_evaluation_prompt(story: Dict, length_analysis: Dict) -> str:
        word_count = length_analysis.get('word_count', 0)
        
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
        for dim in ["character_connection", "bedtime_appropriate", "storytelling_craft", "age_appropriate"]:
            score = scores.get(dim, 0)
            if score < 7.0:
                low_dimensions.append(f"- {dim.upper()}: {score}/10 - {feedback.get(dim, 'Needs improvement')}")
        
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
You are generating example questions that curious 5-10 year old children might want to ask after hearing this bedtime story.

STORY CONTEXT:
Title: {story['title']}
Story: {story['story']}
Moral: {story['moral']}

Generate 3 engaging, story-specific questions that would spark a child's curiosity. Make them:

QUESTION TYPES TO INCLUDE:
1. A "what" question about story elements (characters, places, objects)
2. A "why" or "how" question about motivations or story mechanics  
3. A "what if" or imaginative question that extends the story world

REQUIREMENTS:
- Specific to THIS story (not generic questions that work for any story)
- Age-appropriate for 5-10 year olds
- Encourage imagination and wonder
- Not too complex or abstract
- Questions a curious child would actually want to ask

EXAMPLES OF GOOD QUESTIONS:
- "What do you think Luna the dragon's favorite color of book is?"
- "How do you think Maya felt when she first saw Luna?"
- "What other magical creatures might live in the library?"

AVOID:
- Generic questions that work for any story
- Questions with obvious answers already in the story
- Too complex or abstract questions
- Questions about scary or inappropriate topics

Respond ONLY with valid JSON:
{{
    "questions": [
        "First engaging question specific to this story",
        "Second question about different story aspect", 
        "Third imaginative question"
    ]
}}
"""
    
    @staticmethod
    def answer_question_prompt(question: str, story_context: Dict) -> str:
        return f"""
You are answering a child's question about a bedtime story. Be warm, engaging, and age-appropriate for kids 5-10.

STORY CONTEXT:
Title: {story_context['title']}
Story: {story_context['story']}
Moral: {story_context['moral']}

CHILD'S QUESTION: "{question}"

ANSWER GUIDELINES:
- Keep the magic and wonder of the story alive
- Be encouraging and positive
- Use age-appropriate language (5-10 years old)
- Draw from story details when possible
- If the answer isn't in the story, use imagination to extend the story world
- Keep answers concise (2-4 sentences)
- Maintain the gentle, bedtime-appropriate tone
- Sometimes turn it back to the child: "What do you think?"

EXAMPLES OF GOOD ANSWERS:
Question: "What's Luna's favorite color book?"
Answer: "Based on how Luna organized books by color, I think she might love the deep blue books about oceans and night skies - just like the color of peaceful dreams! What color books do you think would be your favorite?"

Question: "Are there other dragons in the library?"
Answer: "Maybe there are! Luna seemed like she had been hiding for a long time, so perhaps there are other shy magical creatures living quietly among the books, waiting for kind friends like Maya to discover them."

Respond with ONLY the answer text (no JSON, no quotes, just the answer).
"""