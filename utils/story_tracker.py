import json
import os
from datetime import datetime
from typing import Dict, List

class StoryTracker:
    """
    Tracks generated stories and their evaluation scores.
    Stores data in JSON and generates HTML reports.
    """
    
    def __init__(self, storage_file: str = "story_metrics.json"):
        self.storage_file = storage_file
        self.stories = self._load_stories()
    
    def _load_stories(self) -> List[Dict]:
        """Load existing stories from JSON file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def _save_stories(self):
        """Save stories to JSON file"""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.stories, f, indent=2, ensure_ascii=False)
    
    def add_story(self, story: Dict, evaluation: Dict, user_request: str = ""):
        """
        Add a new story and its evaluation to tracking
        
        Args:
            story: {"title": str, "story": str, "moral": str}
            evaluation: Full judge evaluation results
            user_request: Original user request that generated this story
        """
        
        # Create story record
        story_record = {
            "id": len(self.stories) + 1,
            "timestamp": datetime.now().isoformat(),
            "user_request": user_request,
            "story": {
                "title": story.get("title", "Untitled"),
                "content": story.get("story", ""),
                "moral": story.get("moral", ""),
                "word_count": len(story.get("story", "").split())
            },
            "evaluation": {
                "safety_passed": evaluation.get("safety_passed", True),
                "character_connection": evaluation.get("character_connection", 0),
                "bedtime_appropriate": evaluation.get("bedtime_appropriate", 0),
                "storytelling_craft": evaluation.get("storytelling_craft", 0),
                "age_appropriate": evaluation.get("age_appropriate", 0),
                "overall_score": evaluation.get("overall_score", 0),
                "passed": evaluation.get("passed", False),
                "length_check": evaluation.get("length_check", {}),
                "feedback": evaluation.get("feedback", {})
            }
        }
        
        self.stories.append(story_record)
        self._save_stories()
        print(f"Story #{story_record['id']} saved to {self.storage_file}")
    
    def generate_html_report(self, output_file: str = "story_report.html"):
        """Generate HTML report of all tracked stories"""
        
        if not self.stories:
            print("No stories to display in report")
            return
        
        # Calculate summary stats
        total_stories = len(self.stories)
        avg_score = sum(s["evaluation"]["overall_score"] for s in self.stories) / total_stories
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Beanstalk AI Story Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f7fa;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .story-card {{
            background: white;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .story-header {{
            padding: 20px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}
        .story-title {{
            font-size: 1.5em;
            margin: 0 0 10px 0;
        }}
        .story-meta {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .scores {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            padding: 20px;
            background: #f8f9fa;
        }}
        .score-item {{
            text-align: center;
        }}
        .score-label {{
            font-size: 0.8em;
            color: #666;
            margin-bottom: 5px;
        }}
        .score-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .story-content {{
            padding: 20px;
        }}
        .story-text {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
            white-space: pre-wrap;
            line-height: 1.8;
        }}
        .moral {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #2196f3;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌱 Beanstalk AI Story Report</h1>
        <p>Generated bedtime stories and their quality scores</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{total_stories}</div>
            <div>Total Stories</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{avg_score:.1f}/10</div>
            <div>Average Score</div>
        </div>
    </div>
"""
        
        # Add each story
        for story in reversed(self.stories):  # Show newest first
            eval_data = story["evaluation"]
            
            # Format timestamp
            timestamp = datetime.fromisoformat(story["timestamp"]).strftime("%Y-%m-%d %H:%M")
            
            html_content += f"""
    <div class="story-card">
        <div class="story-header">
            <div class="story-title">#{story["id"]}: {story["story"]["title"]}</div>
            <div class="story-meta">
                Generated: {timestamp} | Request: "{story["user_request"]}" | Words: {story["story"]["word_count"]}
            </div>
        </div>
        
        <div class="scores">
            <div class="score-item">
                <div class="score-label">Character Connection</div>
                <div class="score-value">{eval_data["character_connection"]}/10</div>
            </div>
            <div class="score-item">
                <div class="score-label">Bedtime Appropriate</div>
                <div class="score-value">{eval_data["bedtime_appropriate"]}/10</div>
            </div>
            <div class="score-item">
                <div class="score-label">Storytelling Craft</div>
                <div class="score-value">{eval_data["storytelling_craft"]}/10</div>
            </div>
            <div class="score-item">
                <div class="score-label">Age Appropriate</div>
                <div class="score-value">{eval_data["age_appropriate"]}/10</div>
            </div>
            <div class="score-item">
                <div class="score-label">Overall Score</div>
                <div class="score-value">{eval_data["overall_score"]}/10</div>
            </div>
        </div>
        
        <div class="story-content">
            <div class="story-text">{story["story"]["content"]}</div>
            <div class="moral"><strong>Moral:</strong> {story["story"]["moral"]}</div>
        </div>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        # Write HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML report generated: {output_file}")
    
    def get_stats(self) -> Dict:
        """Get summary statistics"""
        if not self.stories:
            return {"total": 0, "passed": 0, "average_score": 0, "pass_rate": 0}
        
        total = len(self.stories)
        passed = sum(1 for s in self.stories if s["evaluation"]["passed"])
        avg_score = sum(s["evaluation"]["overall_score"] for s in self.stories) / total
        
        return {
            "total": total,
            "passed": passed,
            "average_score": round(avg_score, 2),
            "pass_rate": round((passed / total) * 100, 1)
        }