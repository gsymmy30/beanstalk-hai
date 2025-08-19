# 🌱✨ Beanstalk AI ✨🌱

**Magical Bedtime Stories for Kids 5-10**

Beanstalk AI is an intelligent bedtime story generator that creates engaging stories for children. Each story is carefully crafted, evaluated, and refined to ensure it's perfect for bedtime.

## 🚀 Setup

### Prerequisites
- Python 3.7+
- OpenAI API key

### Installation

1. **Clone and install**
   ```bash
   git clone https://github.com/gsymmy30/beanstalk-hai.git
   cd beanstalk-hai
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API key**
   
   Create a `.env` file:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the app**
   ```bash
   python main.py
   ```

## 🎯 How to Use

1. Choose option `1` to create a new story
2. Enter any story idea (e.g., "dragon who loves books", "brave mouse", or even just "adventure")
3. Watch as AI creates, evaluates, and refines your story
4. Enjoy the final story and ask questions about it
5. View your story collection with option `2`

## 📖 Example Usage

```
🌱✨ BEANSTALK AI ✨🌱
Magical Bedtime Stories for Kids 5-10

 📖  1. Create a new story
 📊  2. View story report  
 🌙  3. Exit

➤ Choose: 1

📖 What story shall we create tonight?
➤ Your idea: a mouse who lives in a library

✨ Creating your story...
Improving story...

📚 The Brave Library Mouse
[... story content ...]
💫 Even the smallest among us can be the bravest heroes.

✅ Story Quality: 8.5/10

💭 Did you enjoy this story? (Y/N)
➤ Y

💬 Got questions about the story?
 1. What was Pip's favorite book to read?
 2. How did the other mice feel about Pip?
 3. What happened to the library cat?

❓ What was Pip's favorite book to read?

💡 I think Pip loved adventure stories the most...

Press Enter to continue...

📚 1 stories created

➤ Choose: 3

🌙 Sweet dreams!
```

## 🏗️ System Workflow

![Beanstalk AI Flow](flow-diagram.png)

## 🏗️ System Architecture

```mermaid
graph TB
    %% User Interface
    User[User]
    CLI[CLI Menu<br/>main.py]
    
    %% Core Story Pipeline
    InputHandler[Input Handler<br/>Validates input<br/>Filters inappropriate<br/>Enhances ideas]
    
    StoryGen[Story Generator<br/>Two-phase generation:<br/>1. Outline creation<br/>2. Story writing]
    
    Judge[Judge System<br/>Safety gatekeeper<br/>4-dimension scoring:<br/>• Bedtime readiness<br/>• Creative spark<br/>• Story quality<br/>• Age readability]
    
    QA[Story Q&A<br/>Generates questions<br/>Answers contextually]
    
    %% Data & Analytics
    Tracker[Story Tracker<br/>Saves stories<br/>User feedback<br/>Metrics]
    
    Report[HTML Dashboard<br/>story_report.html<br/>Analytics & scores]
    
    JSONData[(story_metrics.json<br/>Persistent storage)]
    
    %% External Service
    OpenAI[OpenAI GPT-3.5<br/>LLM Service]
    
    %% Prompt Management
    Prompts[Prompt Library<br/>utils/prompts.py<br/>Centralized templates:<br/>• Input validation<br/>• Story generation<br/>• Judge evaluation<br/>• Q&A responses]
    
    %% Main Flow
    User -->|Story idea| CLI
    CLI --> InputHandler
    InputHandler -->|Valid input| StoryGen
    StoryGen -->|Generated story| Judge
    
    %% Refinement Loop
    Judge -->|Pass| QA
    Judge -->|Needs improvement| StoryGen
    
    %% Post-Story Flow
    QA --> CLI
    CLI -->|Display story| User
    User -->|Like/Dislike| CLI
    
    %% Data Flow
    CLI -->|Save| Tracker
    Tracker --> JSONData
    Tracker -->|Generate| Report
    
    %% LLM Integration
    InputHandler -.->|uses| Prompts
    StoryGen -.->|uses| Prompts
    Judge -.->|uses| Prompts
    QA -.->|uses| Prompts
    
    InputHandler -->|API call| OpenAI
    StoryGen -->|API call| OpenAI
    Judge -->|API call| OpenAI
    QA -->|API call| OpenAI
    
    %% Styling with darker backgrounds
    classDef interface fill:#1565c0,stroke:#0d47a1,stroke-width:2px,color:#fff
    classDef pipeline fill:#6a1b9a,stroke:#4a148c,stroke-width:2px,color:#fff
    classDef storage fill:#e65100,stroke:#bf360c,stroke-width:2px,color:#fff
    classDef external fill:#2e7d32,stroke:#1b5e20,stroke-width:2px,color:#fff
    classDef utility fill:#f57c00,stroke:#e65100,stroke-width:2px,color:#fff
    
    class User,CLI interface
    class InputHandler,StoryGen,Judge,QA pipeline
    class Tracker,Report,JSONData storage
    class OpenAI external
    class Prompts utility
```

### Key Components

🛡️ **Input Handler** - Handles ANY input, filters inappropriate content, provides suggestions  
✍️ **Story Generator & Refiner** - Creates complete stories, optimized for bedtime, improves based on feedback  
⚖️ **Judge** - Age-appropriate safety gatekeeper, 4-dimension scoring rubric  
🤔 **Story Q&A** - Suggests and answers context-related questions  
📊 **Metrics** - Dashboard tracking story scores and improvements over time

---

**Sweet dreams! 🌙✨**
