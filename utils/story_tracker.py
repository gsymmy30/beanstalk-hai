import json
import os
from datetime import datetime
from typing import Dict, List

class StoryTracker:
    """
    Tracks generated stories with new evaluation schema and user feedback.
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
    
    def add_story(self, story: Dict, evaluation: Dict, user_request: str = "", user_liked: bool = False):
        """
        Add a new story with evaluation and user feedback
        
        Args:
            story: {"title": str, "story": str, "moral": str}
            evaluation: Full judge evaluation results with new schema
            user_request: Original user request
            user_liked: Whether user liked the story (Y/N)
        """
        
        # Extract scores safely
        scores = evaluation.get("scores", {})
        
        # Create story record with new schema
        story_record = {
            "id": len(self.stories) + 1,
            "timestamp": datetime.now().isoformat(),
            "user_request": user_request,
            "user_liked": user_liked,
            "story": {
                "title": story.get("title", "Untitled"),
                "content": story.get("story", ""),
                "moral": story.get("moral", ""),
                "word_count": len(story.get("story", "").split())
            },
            "evaluation": {
                "pass": evaluation.get("pass", False),
                "safety_passed": evaluation.get("safety_passed", True),
                "reason": evaluation.get("reason", ""),
                "scores": {
                    "bedtime_readiness": scores.get("bedtime_readiness", 0),
                    "creative_spark": scores.get("creative_spark", 0),
                    "story_quality": scores.get("story_quality", 0),
                    "age_readability": scores.get("age_readability", 0)
                },
                "overall": evaluation.get("overall", 0),
                "feedback": evaluation.get("feedback", ""),
                "length_check": evaluation.get("length_check", {})
            }
        }
        
        self.stories.append(story_record)
        self._save_stories()
        print(f"\n📝 Story #{story_record['id']} saved to {self.storage_file}")
    
    def generate_html_report(self, output_file: str = "story_report.html"):
        """Generate HTML report with new schema"""
        
        if not self.stories:
            print("No stories to display in report")
            return
        
        # Calculate summary stats
        total_stories = len(self.stories)
        avg_score = sum(s["evaluation"]["overall"] for s in self.stories) / total_stories
        liked_count = sum(1 for s in self.stories if s.get("user_liked", False))
        liked_pct = (liked_count / total_stories) * 100
        passed_count = sum(1 for s in self.stories if s["evaluation"]["pass"])
        
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
        .user-feedback {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.3);
            font-weight: bold;
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
        .pass-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .pass-badge.passed {{
            background: #d4edda;
            color: #155724;
        }}
        .pass-badge.failed {{
            background: #f8d7da;
            color: #721c24;
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
        .feedback {{
            margin-top: 15px;
            padding: 15px;
            background: #fff3cd;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
        }}
        .safety-failed {{
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌱 Beanstalk AI Story Report</h1>
        <p>Generated bedtime stories with quality evaluation</p>
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
        <div class="stat-card">
            <div class="stat-number">{liked_pct:.0f}%</div>
            <div>User Liked</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{passed_count}/{total_stories}</div>
            <div>Stories Passed</div>
        </div>
    </div>
"""
        
        # Add each story
        for story in reversed(self.stories):  # Show newest first
            eval_data = story["evaluation"]
            scores = eval_data.get("scores", {})
            
            # Format timestamp
            timestamp = datetime.fromisoformat(story["timestamp"]).strftime("%Y-%m-%d %H:%M")
            
            # User feedback badge
            user_feedback = "👍 Liked" if story.get("user_liked", False) else "👎 Not Liked"
            
            # Pass/Fail badge
            pass_status = "passed" if eval_data["pass"] else "failed"
            pass_text = "✅ PASSED" if eval_data["pass"] else "❌ FAILED"
            
            html_content += f"""
    <div class="story-card">
        <div class="story-header">
            <div class="story-title">#{story["id"]}: {story["story"]["title"]}</div>
            <div class="story-meta">
                Generated: {timestamp} | Request: "{story["user_request"]}" | Words: {story["story"]["word_count"]}
                <span class="user-feedback">{user_feedback}</span>
            </div>
        </div>
"""
            
            # Safety check
            if not eval_data.get("safety_passed", True):
                html_content += f"""
        <div class="safety-failed">
            🛡️ SAFETY FAILED: {eval_data.get("reason", "Unknown safety issue")}
        </div>
"""
            else:
                # Show scores
                html_content += f"""
        <div class="scores">
            <div class="score-item">
                <div class="score-label">Bedtime Readiness</div>
                <div class="score-value">{scores.get("bedtime_readiness", 0)}/10</div>
            </div>
            <div class="score-item">
                <div class="score-label">Creative Spark</div>
                <div class="score-value">{scores.get("creative_spark", 0)}/10</div>
            </div>
            <div class="score-item">
                <div class="score-label">Story Quality</div>
                <div class="score-value">{scores.get("story_quality", 0)}/10</div>
            </div>
            <div class="score-item">
                <div class="score-label">Age Readability</div>
                <div class="score-value">{scores.get("age_readability", 0)}/10</div>
            </div>
            <div class="score-item">
                <div class="score-label">Overall Score</div>
                <div class="score-value">{eval_data.get("overall", 0)}/10</div>
            </div>
            <div class="score-item">
                <div class="score-label">Status</div>
                <div><span class="pass-badge {pass_status}">{pass_text}</span></div>
            </div>
        </div>
"""
            
            html_content += f"""
        <div class="story-content">
            <div class="story-text">{story["story"]["content"]}</div>
            <div class="moral"><strong>Moral:</strong> {story["story"]["moral"]}</div>
"""
            
            # Add feedback if available
            if eval_data.get("feedback"):
                html_content += f"""
            <div class="feedback">
                <strong>Judge Feedback:</strong> {eval_data["feedback"]}
            </div>
"""
            
            html_content += """
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
        """Get summary statistics with user feedback"""
        if not self.stories:
            return {"total": 0, "passed": 0, "average_score": 0, "pass_rate": 0, "liked_percentage": 0}
        
        total = len(self.stories)
        passed = sum(1 for s in self.stories if s["evaluation"]["pass"])
        avg_score = sum(s["evaluation"]["overall"] for s in self.stories) / total
        liked = sum(1 for s in self.stories if s.get("user_liked", False))
        
        return {
            "total": total,
            "passed": passed,
            "average_score": round(avg_score, 2),
            "pass_rate": round((passed / total) * 100, 1),
            "liked_percentage": round((liked / total) * 100, 0)
        }