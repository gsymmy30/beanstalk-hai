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
    """Prompts for story generation"""
    
    @staticmethod
    def complete_story_prompt(story_request: str) -> str:
        return f"""
You are a master storyteller creating bedtime stories for children aged 5-10. 

Create a complete bedtime story based on: "{story_request}"

STORY REQUIREMENTS (Research-Backed):
- Length: 900-1000 words (perfect for 10-15 minutes reading)
- Child protagonist (age 5-10) who solves problems independently
- Gentle, positive themes (friendship, kindness, exploration, overcoming small fears)
- Simple plot: clear beginning, middle, peaceful resolution
- Magical/imaginative elements balanced with familiar settings
- Soothing language that gradually winds down toward the end
- Light humor and playfulness without overstimulation
- Happy, reassuring ending that makes child feel safe and sleepy

AVOID:
- Adults solving the main problem
- Scary or intense conflicts
- Cliffhangers or unresolved endings
- Overly complex plots
- High-stakes danger

STORY STRUCTURE:
- Start engaging to hook attention
- Build gentle adventure/challenge
- Child character shows growth/learning
- Peaceful resolution with characters safe/cozy
- End with sleepy, comforting imagery

Make this story feel UNIQUE and engaging - not generic AI content. Use specific details, vivid imagery, and creative plot elements that avoid common fairy tale clichés.

Respond ONLY with valid JSON:
{{
    "title": "Compelling story title",
    "story": "Complete 900-1000 word narrative that follows all requirements",
    "moral": "Simple life lesson naturally embedded in the story"
}}
"""
    
    @staticmethod
    def refinement_prompt(original_story: Dict, refinement_instructions: str) -> str:
        return f"""
You are refining a bedtime story based on specific feedback.

ORIGINAL STORY:
Title: {original_story['title']}
Story: {original_story['story']}
Moral: {original_story['moral']}

IMPROVEMENT NEEDED:
{refinement_instructions}

Please improve the story while maintaining its core elements and staying true to bedtime story requirements:
- Child protagonist solving problems
- Gentle, positive themes
- Peaceful resolution
- Age-appropriate for 5-10 year olds
- 900-1000 words
- Gradually calming toward the end

Make targeted improvements based on the feedback while keeping what works well.

Respond ONLY with valid JSON:
{{
    "title": "Improved title (if needed)",
    "story": "Improved story addressing the feedback",
    "moral": "Improved moral (if needed)"
}}
"""

class JudgePrompts:
    """Research-backed prompts for story evaluation system"""
    
    @staticmethod
    def safety_gate_prompt(story: Dict) -> str:
        return f"""
You are evaluating if this bedtime story is SAFE for children aged 5-10.

STORY TO CHECK:
Title: {story['title']}
Story: {story['story']}
Moral: {story['moral']}

SAFETY REQUIREMENTS (MUST ALL BE MET):
- No profanity or inappropriate language
- No violence, death, serious injury, or trauma
- No genuinely scary, frightening, or nightmarish content
- No harmful stereotypes or negative messaging
- Content should be "never scary and always [appropriate]" per research

Respond ONLY with valid JSON:
{{
    "passed": true/false,
    "issues": "specific safety concerns if failed, empty if passed"
}}
"""
    
    @staticmethod
    def quality_evaluation_prompt(story: Dict) -> str:
        return f"""
You are an expert judge evaluating bedtime stories using research-backed criteria for "amazing stories that happen to be for bedtime."

STORY TO EVALUATE:
Title: {story['title']}
Story: {story['story']}
Moral: {story['moral']}

Rate on 5-point scale (1=Poor, 3=Adequate, 5=Excellent):

1. NARRATIVE EXCELLENCE (35% weight):
- Engaging plot with clear beginning/middle/satisfying end
- Child protagonist (5-10) driving action, solving problems independently
- "Real stakes" but manageable for children (lost toy vs life danger)
- Emotional engagement - makes kids care about characters
- Humor and playfulness - research shows "never scary and always funny"
- "Goodness wins" - optimistic, empowering resolution

2. STORY AUTHENTICITY (25% weight):
- Specific, vivid details vs generic AI descriptions
- Natural dialogue and realistic character interactions
- Creative, unexpected elements that avoid fairy tale clichés
- Rich sensory descriptions that help visualization
- Unique plot elements that feel fresh and engaging
- Avoids common AI story patterns (helpful animal guide, magic object solving everything)

3. BEDTIME FLOW & PACING (25% weight):
- "Active engagement → passive listening" progression per research
- Starts with hook to capture attention quickly
- Gradually winds down toward peaceful resolution
- Calm, cozy ending - characters safe, often going to sleep
- No unresolved tensions that could keep minds racing
- "Help children transition from busy days and wind down for sleep"

4. AGE-APPROPRIATE WONDER (15% weight):
- Fantasy balanced with familiarity - magical but grounded in familiar contexts
- Imaginative elements kids can accept without lengthy explanation
- Relatable challenges for 5-10 year olds (school, friends, small fears)
- Empowering themes - kids feel "big and capable"
- Rich vocabulary appropriate for developmental stage
- Content that "stimulates imagination without overwhelming"

Respond ONLY with valid JSON:
{{
    "narrative_excellence": 1-5 rating,
    "story_authenticity": 1-5 rating,
    "bedtime_flow": 1-5 rating,
    "age_appropriate_wonder": 1-5 rating,
    "feedback": {{
        "narrative_excellence": "specific feedback on plot, character agency, humor",
        "story_authenticity": "specific feedback on uniqueness, details, creativity",
        "bedtime_flow": "specific feedback on pacing and wind-down progression", 
        "age_appropriate_wonder": "specific feedback on age-appropriateness and wonder balance"
    }}
}}
"""
    
    @staticmethod
    def refinement_instructions_prompt(scores: Dict) -> str:
        feedback = scores.get("feedback", {})
        
        # Identify lowest scoring dimensions
        score_items = [(k, v) for k, v in scores.items() 
                      if isinstance(v, (int, float)) and k != "overall_score"]
        sorted_scores = sorted(score_items, key=lambda x: x[1])
        
        low_dimensions = [dim for dim, score in sorted_scores[:2] if score < 4.0]
        
        return f"""
Based on this story evaluation, provide specific improvement instructions focusing on the lowest-scoring areas.

DIMENSIONS NEEDING IMPROVEMENT:
{chr(10).join([f"- {dim}: {scores.get(dim, 'N/A')}/5 - {feedback.get(dim, '')}" for dim in low_dimensions])}

BEDTIME FLOW SCORE: {scores.get('bedtime_flow', 'N/A')}/5 (Must be ≥3.5)

Provide 2-3 specific, actionable instructions based on research findings:

If NARRATIVE EXCELLENCE is low:
- Add more engaging plot events with child protagonist solving problems
- Include gentle humor and playfulness ("never scary and always funny")
- Ensure "goodness wins" with empowering resolution

If STORY AUTHENTICITY is low:
- Replace generic descriptions with specific, vivid details
- Add unexpected but logical plot developments
- Create unique story elements that avoid common patterns

If BEDTIME FLOW is low:
- Start engaging then gradually wind down ("active → passive listening")
- End with cozy, peaceful imagery (characters safe/sleeping)
- Remove any unresolved tensions or cliffhangers

If AGE-APPROPRIATE WONDER is low:
- Balance fantasy with familiar settings kids know
- Focus on relatable 5-10 year old challenges
- Make child characters feel empowered and capable

Be specific about WHAT to change and HOW to change it.
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