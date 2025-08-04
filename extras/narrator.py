"""
Smart bedtime narrator that preprocesses text for natural narration
"""

import re
import json
import os
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs import generate, save, Voice, VoiceSettings

# Load environment variables
load_dotenv()


class SmartBedtimeNarrator:
    """
    Preprocesses stories to understand pacing, emotion, and tone changes
    """
    
    def __init__(self, api_key: Optional[str] = None, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
        # Get API key from parameter or .env file
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "No ElevenLabs API key found. "
                "Please set ELEVENLABS_API_KEY in your .env file or pass it as a parameter."
            )
        
        # Set API key for ElevenLabs
        os.environ["ELEVEN_API_KEY"] = self.api_key
        
        self.voice_id = voice_id
        
        # Output directory
        self.output_dir = Path("narrations")
        self.output_dir.mkdir(exist_ok=True)
        
        # Emotion indicators
        self.excitement_words = [
            'wow', 'amazing', 'incredible', 'fantastic', 'wonderful',
            'exclaimed', 'shouted', 'cheered', 'jumped', 'danced'
        ]
        
        self.calm_words = [
            'peaceful', 'quiet', 'gentle', 'soft', 'calm', 'serene',
            'whispered', 'sighed', 'yawned', 'drowsy', 'sleepy'
        ]
        
        self.tension_words = [
            'worried', 'nervous', 'scared', 'afraid', 'trembled',
            'problem', 'trouble', 'danger', 'oh no', 'help'
        ]
        
        self.resolution_words = [
            'solved', 'fixed', 'better', 'safe', 'together',
            'figured out', 'realized', 'understood', 'happy'
        ]
    
    def narrate_story(self, story_data: Dict) -> str:
        """
        Narrate with intelligent preprocessing
        """
        title = story_data.get('title', 'Story')
        text = story_data.get('story', '')
        
        print(f"\n🌙 Narrating: {title}")
        
        # Analyze story structure
        segments = self._analyze_story(text)
        
        # Process each segment with appropriate tone
        processed_segments = []
        for segment in segments:
            processed = self._process_segment(segment)
            processed_segments.append(processed)
        
        # Combine with appropriate transitions
        final_text = self._combine_segments(processed_segments)
        
        # Generate audio with dynamic settings
        print("✨ Generating narration with dynamic expression...")
        audio = self._generate_with_segments(processed_segments)
        
        # Save
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        output_path = self.output_dir / f"{safe_title}.mp3"
        save(audio, str(output_path))
        
        print(f"✅ Saved to: {output_path}")
        return str(output_path)
    
    def _analyze_story(self, text: str) -> List[Dict]:
        """
        Analyze story to identify different segments and their emotional tone
        """
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        segments = []
        for i, para in enumerate(paragraphs):
            # Detect emotional tone
            tone = self._detect_tone(para)
            
            # Detect if it's dialogue heavy
            has_dialogue = para.count('"') >= 2
            
            # Detect story position
            position = self._get_position(i, len(paragraphs))
            
            segments.append({
                'text': para,
                'tone': tone,
                'has_dialogue': has_dialogue,
                'position': position,
                'index': i
            })
        
        return segments
    
    def _detect_tone(self, text: str) -> str:
        """
        Detect emotional tone of a text segment
        """
        text_lower = text.lower()
        
        # Count emotion indicators
        excitement_count = sum(1 for word in self.excitement_words if word in text_lower)
        calm_count = sum(1 for word in self.calm_words if word in text_lower)
        tension_count = sum(1 for word in self.tension_words if word in text_lower)
        resolution_count = sum(1 for word in self.resolution_words if word in text_lower)
        
        # Determine dominant tone
        scores = {
            'exciting': excitement_count,
            'calm': calm_count,
            'tense': tension_count,
            'resolving': resolution_count,
            'neutral': 1  # Default
        }
        
        return max(scores, key=scores.get)
    
    def _get_position(self, index: int, total: int) -> str:
        """
        Determine story position (beginning, middle, end)
        """
        ratio = index / max(total - 1, 1)
        
        if ratio < 0.2:
            return 'beginning'
        elif ratio < 0.8:
            return 'middle'
        else:
            return 'ending'
    
    def _process_segment(self, segment: Dict) -> Dict:
        """
        Process a segment based on its characteristics
        """
        text = segment['text']
        tone = segment['tone']
        position = segment['position']
        
        # Apply tone-specific processing
        if tone == 'exciting':
            # Slightly faster, more animated
            text = self._add_excitement_markers(text)
            voice_settings = VoiceSettings(
                stability=0.7,
                similarity_boost=0.75,
                style=0.3,  # More expressive
                use_speaker_boost=True
            )
        
        elif tone == 'calm' or position == 'ending':
            # Slower, more soothing
            text = self._add_calm_markers(text)
            voice_settings = VoiceSettings(
                stability=0.9,
                similarity_boost=0.8,
                style=0.1,  # Very gentle
                use_speaker_boost=True
            )
        
        elif tone == 'tense':
            # Slightly dramatic but not scary
            text = self._add_tension_markers(text)
            voice_settings = VoiceSettings(
                stability=0.75,
                similarity_boost=0.75,
                style=0.25,
                use_speaker_boost=True
            )
        
        else:  # neutral/resolving
            # Balanced narration
            text = self._add_standard_markers(text)
            voice_settings = VoiceSettings(
                stability=0.85,
                similarity_boost=0.75,
                style=0.15,
                use_speaker_boost=True
            )
        
        # Add position-based processing
        if position == 'beginning':
            # Clear, engaging start
            text = "... " + text  # Small pause before starting
        elif position == 'ending':
            # Extra slow and soothing
            text = self._add_bedtime_ending(text)
        
        # Process dialogue
        if segment['has_dialogue']:
            text = self._process_dialogue(text)
        
        return {
            'original': segment['text'],
            'processed': text,
            'voice_settings': voice_settings,
            'tone': tone,
            'position': position
        }
    
    def _add_excitement_markers(self, text: str) -> str:
        """Add markers for exciting passages"""
        # Short pauses before exclamations for effect
        text = re.sub(r'(\w)\!', r'\1!', text)
        
        # Emphasize wow words
        for word in ['Wow', 'Amazing', 'Incredible']:
            text = text.replace(f' {word}', f' ...{word}')
        
        return text
    
    def _add_calm_markers(self, text: str) -> str:
        """Add markers for calm passages"""
        # Longer pauses between sentences
        text = text.replace('. ', '. ... ')
        
        # Extra pause before sleep-related words
        for word in ['yawned', 'sleepy', 'drowsy', 'tired']:
            text = re.sub(rf'\b{word}\b', f'... {word}', text, flags=re.IGNORECASE)
        
        return text
    
    def _add_tension_markers(self, text: str) -> str:
        """Add markers for tense passages (but keep child-friendly)"""
        # Quick pauses for suspense
        text = text.replace(', ', ', . ')
        
        # Pause before problem words
        text = re.sub(r'\b(Oh no|Help)\b', r'... \1', text, flags=re.IGNORECASE)
        
        return text
    
    def _add_standard_markers(self, text: str) -> str:
        """Standard processing for neutral passages"""
        # Natural pauses at commas and periods
        text = text.replace(', ', ', . ')
        text = text.replace('. ', '. .. ')
        
        return text
    
    def _add_bedtime_ending(self, text: str) -> str:
        """Special processing for story endings"""
        # Very slow and soothing
        text = text.replace('. ', '. ... ... ')
        text = text.replace(', ', ', ... ')
        
        # Extra pauses before final words
        if 'the end' in text.lower():
            text = re.sub(r'(the end\.?)', r'... ... \1', text, flags=re.IGNORECASE)
        
        # Add sleepy feeling
        sleep_words = ['dream', 'sleep', 'night', 'rest', 'cozy', 'warm']
        for word in sleep_words:
            text = re.sub(rf'\b{word}\b', f'... {word} ...', text, flags=re.IGNORECASE)
        
        return text
    
    def _process_dialogue(self, text: str) -> str:
        """Process dialogue for character distinction"""
        # Add brief pauses around dialogue
        text = re.sub(r'"([^"]+)"', r'"\1" .', text)
        
        # Different processing for different speakers
        # (In practice, ElevenLabs handles this well automatically)
        
        return text
    
    def _combine_segments(self, segments: List[Dict]) -> str:
        """Combine processed segments"""
        combined = []
        
        for i, segment in enumerate(segments):
            text = segment['processed']
            
            # Add transition pauses between segments
            if i > 0:
                # Longer pause between paragraphs
                combined.append("... ... ...")
            
            combined.append(text)
        
        return '\n\n'.join(combined)
    
    def _generate_with_segments(self, segments: List[Dict]) -> bytes:
        """
        Generate audio with different settings per segment
        
        Note: ElevenLabs doesn't support mid-text setting changes,
        so we use the overall best settings based on story analysis
        """
        # Determine overall story mood
        tones = [s['tone'] for s in segments]
        
        # If ending is calm (usually is), use calm settings
        if segments[-1]['tone'] in ['calm', 'neutral'] or segments[-1]['position'] == 'ending':
            final_settings = VoiceSettings(
                stability=0.85,
                similarity_boost=0.75,
                style=0.15,
                use_speaker_boost=True
            )
        else:
            # Use balanced settings
            final_settings = VoiceSettings(
                stability=0.8,
                similarity_boost=0.75,
                style=0.2,
                use_speaker_boost=True
            )
        
        # Combine all text
        full_text = self._combine_segments(segments)
        
        # Generate
        audio = generate(
            text=full_text,
            voice=Voice(voice_id=self.voice_id, settings=final_settings),
            model="eleven_multilingual_v2"
        )
        
        return audio
