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

from typing import Dict

class StoryGenerationPrompts:
    """Prompts for story generation"""
    
    @staticmethod
    def complete_story_prompt(story_request: str) -> str:
        return f"""
Create an exceptional bedtime story for children aged 5-10. This will be judged against professional children's literature standards with a detailed 10-point rubric.

STORY REQUEST: "{story_request}"

MANDATORY WORD COUNT: 900-1000 words. Stories under 850 words will be REJECTED.

STRUCTURE REQUIREMENTS:
Format with clear paragraph breaks (\\n\\n). Target 8-12 paragraphs of 80-120 words each.

CHARACTER DEVELOPMENT ARCHITECTURE

CHARACTER PERSONALITY INTEGRATION:
- Choose ONE specific trait that drives the plot (e.g., "always counts things in threes," "asks exactly two questions about everything," "collects smooth stones")
- Show this trait in action at least 3 times throughout the story
- Make the trait both help AND hinder the character realistically
- Use the trait to create authentic dialogue: "One... two... three deep breaths, just like Mom taught me"

EMOTIONAL LAYERING REQUIREMENTS:
For each major story beat, include ALL four elements:
- Physical sensation the child feels ("stomach fluttered," "hands got sweaty," "shoulders relaxed")
- Internal thought in kid language ("This is scary but I can do it," "Maybe I'm not too little after all")
- External emotional expression (face scrunched up, bounced on toes, bit lip nervously)
- Emotional growth moment (from worried to determined to proud, shown through actions)

FORBIDDEN EMOTIONAL SHORTCUTS:
NEVER USE: "felt brave" "was happy" "felt proud" "heart filled with"
INSTEAD USE: "stood taller" "grinned so wide her cheeks hurt" "chest puffed out" "walked with bigger steps"

AUTHENTIC CHILD DIALOGUE PATTERNS:
- Incomplete sentences when excited: "But what if we— oh! I know!"
- Repetition for emphasis: "Really, really, really big"
- Questions that reveal thinking: "Why do you think it's purple? Purple's not scary, right?"
- Self-talk during problem-solving: "Okay, okay, think Maya, think..."
- Age-appropriate vocabulary with occasional "big words" they're proud of
- Natural interruptions and topic shifts
- Show personality through speech patterns (cautious kid asks more questions, bold kid makes more statements)

ENERGY CURVE PRECISION MAP

PARAGRAPH-BY-PARAGRAPH ENERGY CONTROL:
Paragraphs 1-3: HIGH energy (action verbs: dashed, leaped, discovered, gasped)
Paragraphs 4-6: MEDIUM energy (steady verbs: walked, searched, tried, considered)
Paragraphs 7-9: SETTLING energy (gentle verbs: settled, arranged, whispered, noticed)
Paragraphs 10-12: LOW energy (sleepy verbs: nestled, dozed, curled, drifted)

LANGUAGE RHYTHM SHIFTS:
Early: Short, punchy sentences. Quick dialogue exchanges. Exclamation points.
Middle: Balanced sentence variety with longer descriptive passages. Mixed punctuation.
Late: Longer, flowing sentences with soft consonants and soothing sounds. Periods and gentle commas.

SENSORY PROGRESSION FOR BEDTIME:
Opening (alerting senses): Bright colors, clear sounds, varied textures
- "Sunlight sparkled," "leaves crunched," "bark was rough under her fingers"
Middle (engaging senses): Rich visual details, varied sounds, active touch
- "Moss covered the rocks like green velvet," "water gurgled over stones"
Ending (calming senses): Soft colors, gentle sounds, warm/smooth textures
- "Golden light filtered through," "breeze whispered," "grass was soft as a pillow"

MANDATORY ENDING SENSORY ELEMENTS (include at least 2):
- Soft texture: "moss like velvet," "feathers that tickled," "sand smooth as silk"
- Gentle sound: "creek babbled softly," "leaves whispered," "birds hummed quietly"
- Warm/cool comfort: "sun-warmed stone," "cool grass on bare feet," "gentle breeze"
- Soothing visual: "stars like tiny nightlights," "golden glow," "soft shadows"

CONFLICT ARCHITECTURE

PROBLEM-SOLVING PROGRESSION TEMPLATE (MANDATORY):
Attempt 1: Obvious solution (fails because too simple)
- Character learns: "That was harder than I thought" or equivalent
- Show specific failure: what went wrong and why
Attempt 2: Clever solution (fails because missing key element)
- Character learns: "I need to think differently" or equivalent
- Show character adapting approach based on first failure
Attempt 3: Creative solution (succeeds because combines learning)
- Character realizes: "I had to try both ways together" or equivalent
- Success comes from applying both previous lessons

CONFLICT EXPANSION RULES:
Your main conflict CANNOT be resolved in one paragraph. It must:
- Take at least 250 words to fully resolve
- Include setbacks and complications that feel authentic
- Show the protagonist trying different approaches with specific details
- Have moments where things get worse before getting better
- Require genuine cleverness or bravery AND persistence, never luck

CONCRETE ACTION REQUIREMENTS:
NEVER write vague action like "they solved the problem" or "worked together to save everyone." Instead:
- Show exactly what the character does: "Maya grabbed three thick branches, wedged them against the boulder, and pushed with her legs while pulling the rope"
- Include specific obstacles: "The rope frayed, the branch snapped, mud made everything slippery"
- Add sensory details during action: "Her hands burned from the rough rope, rain stung her eyes"
- Show physical consequences: "She stumbled backward, breathing hard, dirt under her fingernails"

SETTING AS CHARACTER

SETTING PERSONALITY REQUIREMENTS:
Give the setting mood that matches energy curve:
- Opening setting: Dynamic, full of potential (rustling leaves, dancing shadows, morning light)
- Conflict setting: Challenging but not threatening (steep hill, tangled roots, rushing water)
- Resolution setting: Protective and nurturing (sheltered grove, gentle clearing, cozy nook)

SETTING MUST ACTIVELY HELP CHARACTER:
Don't just describe - show how setting provides what character needs
GOOD: "The old oak's hollow was just the right size for two tired adventurers"
GOOD: "The smooth rocks made perfect stepping stones across the creek"
BAD: "They found a beautiful clearing with an old oak tree"
BAD: "There was a creek with rocks in it"

BEDTIME STORY AI PATTERN KILLERS

FORBIDDEN PHRASES (will result in lower craft scores):
- "magical bond," "heart filled with," "learned valuable lesson"
- "courage deep inside," "friendship would last forever"
- "as they drifted off to sleep" (too meta for bedtime stories)
- "once upon a time" (overused opening)
- "happily ever after" (too abrupt for bedtime)

REQUIRED ALTERNATIVES:
- Show bonds through actions: "shared the last piece of bread," "helped without being asked"
- Show lessons through changed behavior: "next time, asked for help first," "remembered to look up AND down"
- End with characters in sleep-ready position, not talking about sleep
- Open with character in action, not exposition
- End with peaceful scene, not declaration of happiness

AUTHENTIC VOICE MARKERS:
- Use contractions naturally: "didn't," "couldn't," "wasn't"
- Include imperfect kid logic: "Maybe if I close my eyes, it'll work better"
- Show thought processes: "First this, then that, then... wait, what if..."
- Natural speech interruptions: "I think we should— oh look, a butterfly!"

THEME INTEGRATION SOPHISTICATION

THEME WEAVING TECHNIQUE:
Instead of stating the theme, demonstrate it through:
- Character's specific actions (shows kindness by sharing only cookie)
- Natural consequences (kindness leads to unexpected friendship)
- Character's realization through dialogue: "I'm glad I shared... now I have someone to explore with"
- Callback in ending: Character does the same kind thing again, but bigger

THEME MUST EMERGE FROM PLOT, NOT BE ADDED TO IT
The moral should feel inevitable based on character's journey, not tacked on.

OPENING HOOK REQUIREMENTS (Paragraphs 1-2, ~150-200 words)

START WITH CHARACTER DOING SOMETHING SPECIFIC:
GOOD: "Seven-year-old Sam was counting the cracks in the sidewalk—one, two, three—when something purple caught his eye"
GOOD: "Mia had asked her two questions for the day already, but the glowing mushroom made her forget all about her rule"
BAD: "There once was a little girl who loved adventures"
BAD: "Sam was a curious boy who lived near the woods"

HOOK REQUIREMENTS:
- Establish character age and defining trait immediately
- Put character in motion, not description
- Include sensory detail that draws reader in
- Hint at the adventure to come
- Use character's personality trait in the very first action

RESOLUTION & WIND-DOWN (Paragraphs 9-12, ~250-300 words)

CONCRETE WIND-DOWN ACTIONS (choose 2-3):
- Building something cozy (fort, nest, shelter) with specific details
- Sharing food or warm drinks with sensory descriptions
- Caring for each other (bandaging scrapes, brushing dirt off) gently
- Quiet conversation about what they learned (not preachy)
- Preparing for sleep (finding soft spots, arranging blankets) naturally
- Gentle activities (star-gazing, listening to night sounds) peacefully

ENDING REQUIREMENTS - SHOW THROUGH ACTIONS:
GOOD: "Mira spread her jacket on the soft moss and Leo curled up beside her, his counting finally quiet"
GOOD: "They listened to the gentle splash of water and the soft hoot of owls overhead"
GOOD: "Tomorrow we'll explore the crystal cave,' Leo whispered, already yawning"
BAD: "Their hearts were full of love and friendship"
BAD: "They felt peaceful and content"
BAD: "The magical bond between them would last forever"

FINAL QUALITY CHECKLIST

Before finishing, verify:
- Character trait appears 3+ times and drives plot
- Energy curve flows: engaging to exciting to settling to peaceful
- All emotions shown through actions/sensations, not told
- Dialogue sounds like real kids talking
- Setting actively helps character solve problems
- Theme emerges naturally from character's choices
- No AI pattern phrases detected
- Ending shows sleepy-ready actions, not statements about sleep
- Word count 900-1000 with proper paragraph breaks

Respond with JSON:
{{
    "title": "Specific, intriguing title that hints at the real adventure and character trait",
    "story": "Your complete 900-1000 word story with proper \\n\\n paragraph breaks following ALL requirements above",
    "moral": "Life lesson that emerges naturally from the character's actions and choices"
}}
"""
    
    @staticmethod
    def refinement_prompt(original_story: Dict, refinement_instructions: str) -> str:
        return f"""
You are refining a bedtime story based on specific feedback from expert evaluation.

ORIGINAL STORY:
Title: {original_story['title']}
Story: {original_story['story']} 
({len(original_story['story'].split())} words)
Moral: {original_story['moral']}

SPECIFIC IMPROVEMENTS NEEDED:
{refinement_instructions}

CRITICAL REQUIREMENTS:
- Story MUST be 900-1000 words after refinement
- Use proper paragraph structure with clear breaks (\\n\\n)
- Address ALL feedback points specifically
- Preserve what works well from original story
- Enhance weak areas without losing story's core appeal

If story is too short, expand by:
- Adding more paragraphs with specific scenes and details
- Developing character's internal thoughts and emotions more deeply
- Including additional dialogue and character interactions
- Enriching sensory descriptions and world-building
- Expanding the wind-down section with more cozy imagery
- Adding more specific, vivid details throughout

If story needs better paragraph structure:
- Break long blocks of text into readable paragraphs
- Each paragraph should be 80-120 words
- Use clear transitions between paragraphs
- Group related thoughts and actions together

BEDTIME STORY ESSENTIALS TO MAINTAIN:
- Child protagonist (5-10) solving problems independently
- Gradual energy curve: engaging start → peaceful, sleepy ending
- Specific, vivid details (not generic descriptions)
- Perfect complexity for 5-10 year cognitive development
- Universal themes woven naturally into adventure
- No cliffhangers or unresolved tensions

Respond ONLY with valid JSON:
{{
    "title": "Refined title (if needed)",
    "story": "Improved story with proper paragraphs addressing all feedback points",
    "moral": "Refined moral (if needed)"
}}
"""

class JudgePrompts:
    """Research-backed prompts for bedtime story evaluation system"""
    
    @staticmethod
    def safety_evaluation_prompt(story: Dict) -> str:
        return f"""
You are evaluating if this bedtime story is SAFE for children aged 5-10.

STORY TO CHECK:
Title: {story['title']}
Story: {story['story']}
Moral: {story['moral']}

SAFETY REQUIREMENTS (MUST ALL BE MET):
- No profanity, violence, death, serious injury, or trauma
- No genuinely scary, frightening, or nightmarish content
- No harmful stereotypes or negative messaging
- Content should be comforting and reassuring for bedtime
- Research shows best bedtime stories are "never scary and always positive"

Respond ONLY with valid JSON:
{{
    "passed": true/false,
    "issues": "specific safety concerns if failed, empty if passed"
}}
"""
    
    @staticmethod
    def detailed_evaluation_prompt(story: Dict, length_analysis: Dict) -> str:
        return f"""
You are an EXPERT JUDGE using a detailed 10-point rubric to evaluate bedtime stories.

STORY TO EVALUATE:
Title: {story['title']}
Story: {story['story']}
Moral: {story['moral']}

LENGTH ANALYSIS: {length_analysis['feedback']}

Rate each dimension 1-10 with ONE DECIMAL PRECISION (e.g., 7.3, 8.7):

=== 1. CHARACTER CONNECTION (30% weight) ===

9-10 EXCEPTIONAL:
- Child protagonist (5-10) with crystal-clear goals kids instantly relate to
- Rich internal life with fears/hopes kids recognize
- Protagonist drives ALL major plot points (zero adult intervention)
- Meaningful character growth throughout story
- Authentic child dialogue that sounds natural

7-8 STRONG:
- Clear relatable child protagonist with good emotional authenticity
- Character makes most important decisions independently
- Some character development visible
- Mostly natural dialogue for age group

5-6 ADEQUATE:
- Child protagonist present but may lack clear motivations
- Surface-level emotional connection
- Mix of child agency and adult problem-solving
- Limited character growth

3-4 WEAK:
- Unclear protagonist or poor age-appropriateness
- Little emotional authenticity
- Adults solve major problems instead of child
- Minimal development

1-2 POOR:
- No clear protagonist or completely inappropriate
- Zero emotional resonance
- Story happens TO character rather than character driving it
- No character growth

=== 2. BEDTIME APPROPRIATE (25% weight) ===

9-10 EXCEPTIONAL:
- Perfect energy curve: compelling hook -> engaging middle -> gradual calm -> peaceful sleep-ready ending
- Masterful pacing that naturally lulls toward drowsiness
- Characters explicitly in cozy, safe state at end
- Zero unresolved tensions or "what happens next" questions
- Language becomes increasingly soothing toward conclusion

7-8 STRONG:
- Clear energy progression from active to calm
- Good wind-down in final third of story
- Peaceful, reassuring ending
- Most conflicts resolved satisfactorily

5-6 ADEQUATE:
- Some energy management but inconsistent
- Peaceful ending but transition could be smoother
- Most major conflicts resolved

3-4 WEAK:
- Poor energy management (high excitement throughout OR too boring)
- Abrupt ending without proper wind-down
- Some unresolved tensions remain

1-2 POOR:
- No energy management whatsoever
- Cliffhanger or anxiety-inducing ending
- Would actively prevent sleep

=== 3. STORYTELLING CRAFT (25% weight) ===

9-10 EXCEPTIONAL:
- Irresistible opening hook establishing character/conflict/stakes immediately
- Flawless narrative structure where every scene propels story forward
- Completely authentic voice (feels human, not AI-generated)
- Vivid, immersive setting with perfect amount of detail
- Unique story elements that surprise while feeling natural
- Professional prose that flows beautifully when read aloud
- Zero detectable AI patterns or generic elements

7-8 STRONG:
- Good engaging opening that draws reader in
- Solid story structure with clear progression
- Mostly authentic voice with few artificial moments
- Well-described setting that enhances story
- Some creative elements that feel fresh

5-6 ADEQUATE:
- Decent opening but may lack immediate hook
- Basic structure with some pacing issues
- Somewhat artificial voice but not distractingly so
- Generic setting elements

3-4 WEAK:
- Weak opening that fails to engage
- Poor structure where scenes don't build effectively
- Obviously artificial voice with many awkward moments
- Heavy reliance on cliches and predictable patterns

1-2 POOR:
- No hook - story starts with exposition or confusion
- Incoherent structure or missing narrative elements
- Completely AI-generated feel throughout
- Entirely predictable with heavy AI patterns

=== 4. AGE APPROPRIATE (20% weight) ===

9-10 EXCEPTIONAL:
- Perfect complexity for 5-10 years (sophisticated enough to engage, simple enough to follow)
- Brilliant balance of fantasy elements with familiar, comforting contexts
- Rich vocabulary that expands language naturally without being incomprehensible
- Universal themes (friendship, courage, kindness) woven seamlessly into adventure
- Story empowers children and reinforces their capability and worth
- Natural moral lessons that don't feel preachy

7-8 STRONG:
- Good complexity level for target age
- Nice fantasy/familiar balance with creative elements
- Appropriate vocabulary with some challenging but accessible words
- Clear positive themes present
- Generally empowering message for children

5-6 ADEQUATE:
- Mostly age-appropriate but may be slightly too simple or complex
- Some imaginative elements but balance could be better
- Basic vocabulary without particular enrichment
- Some positive themes present

3-4 WEAK:
- Wrong complexity level (either too babyish or too advanced)
- Poor fantasy/reality balance
- Limited vocabulary or inappropriately complex language
- Weak or unclear themes

1-2 POOR:
- Completely inappropriate complexity for age group
- No imaginative elements OR completely incomprehensible fantasy
- Vocabulary entirely wrong for age level
- No discernible positive themes

SCORING REQUIREMENTS:
- Use decimal precision (e.g., 7.3, 8.7)
- Compare against specific criteria above, not other stories
- Be critical - reserve 9-10 for truly exceptional elements
- Most stories should score in 5-8 range
- Provide detailed, actionable feedback for each dimension

Respond ONLY with valid JSON:
{{
    "character_connection": X.X,
    "bedtime_appropriate": X.X,
    "storytelling_craft": X.X,
    "age_appropriate": X.X,
    "feedback": {{
        "character_connection": "Detailed analysis against rubric - what level achieved and why. What can be done to improve the score?",
        "bedtime_appropriate": "Assessment of pacing and sleep preparation effectiveness. What can be done to improve the score?",
        "storytelling_craft": "Evaluation of hook, structure, voice authenticity, AI patterns. What can be done to improve the score?",
        "age_appropriate": "Analysis of complexity, themes, and developmental fit. What can be done to improve the score?"
    }}
}}
"""
    
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