from transformer_engine import TransformerProcessor

class MeetingAssistant:
    def __init__(self):
        # Naya transformer engine connect kar diya
        self.engine = TransformerProcessor()

    def analyze_meeting(self, text):
        # AI se summary aur names nikalna
        ai_summary = self.engine.get_summary(text)
        ai_participants = self.engine.extract_people(text)
        
        # Action items aur Decisions ke liye hum purana keyword logic 
        # filhal rehne dete hain kyunke wo theek kaam kar raha tha
        decisions = self.extract_decisions(text)
        tasks = self.extract_tasks(text)
        questions = self.extract_questions(text)

        # Mock object for return (jese pehle tha)
        class Insights:
            def __init__(self, s, p, d, t, q):
                self.summary = s
                self.participants = p
                self.decisions = d
                self.action_items = t
                self.questions = q
                self.sentiment = "Neutral"
                self.duration_estimate = "~5 minutes"

        return Insights(ai_summary, ai_participants, decisions, tasks, questions)

    # ... baaki purane extract_decisions methods niche waise hi rahenge
"""
AI Meeting Assistant with NLP Pipeline
Transcribes, analyzes, and extracts insights from meeting audio/text
"""

import json
import re
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from collections import Counter
import warnings
warnings.filterwarnings('ignore')


@dataclass
class MeetingInsights:
    """Container for meeting analysis results"""
    summary: str
    key_points: List[str]
    action_items: List[Dict[str, str]]
    decisions: List[str]
    participants: List[str]
    topics: List[str]
    sentiment: str
    duration_estimate: str
    questions: List[str]
    next_steps: List[str]


class NLPPipeline:
    """Natural Language Processing pipeline for meeting analysis"""
    
    def __init__(self):
        self.action_keywords = [
            'will', 'should', 'need to', 'must', 'have to', 'going to',
            'action item', 'todo', 'task', 'assign', 'responsible for'
        ]
        self.decision_keywords = [
            'decided', 'agreed', 'approved', 'confirmed', 'concluded',
            'determined', 'resolved', 'settled on', 'go with'
        ]
        self.question_patterns = [
            r'\?$',
            r'^(what|how|why|when|where|who|which|can|could|would|should|is|are|do|does)',
        ]
    
    def extract_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_participants(self, text: str) -> List[str]:
        """Extract participant names from transcript"""
        pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\s*[:\-]'
        participants = re.findall(pattern, text)
        counter = Counter(participants)
        return [name for name, count in counter.most_common() if count >= 2]
    
    def extract_action_items(self, text: str) -> List[Dict[str, str]]:
        """Extract action items and tasks"""
        sentences = self.extract_sentences(text)
        action_items = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for keyword in self.action_keywords:
                if keyword in sentence_lower:
                    assignee = self._extract_assignee(sentence)
                    action_items.append({
                        'task': sentence.strip(),
                        'assignee': assignee if assignee else 'Unassigned',
                        'priority': self._determine_priority(sentence_lower)
                    })
                    break
        return action_items
    
    def _extract_assignee(self, sentence: str) -> Optional[str]:
        """Extract person assigned to a task"""
        patterns = [
            r'([A-Z][a-z]+)\s+will',
            r'([A-Z][a-z]+)\s+should',
            r'assigned to ([A-Z][a-z]+)',
            r'([A-Z][a-z]+)\'s responsibility'
        ]
        for pattern in patterns:
            match = re.search(pattern, sentence)
            if match:
                return match.group(1)
        return None
    
    def _determine_priority(self, text: str) -> str:
        """Determine priority based on urgency keywords"""
        high_priority = ['urgent', 'critical', 'asap', 'immediately', 'today']
        medium_priority = ['soon', 'this week', 'important']
        text_lower = text.lower()
        if any(word in text_lower for word in high_priority):
            return 'High'
        elif any(word in text_lower for word in medium_priority):
            return 'Medium'
        else:
            return 'Normal'
    
    def extract_decisions(self, text: str) -> List[str]:
        """Extract decisions made during the meeting"""
        sentences = self.extract_sentences(text)
        decisions = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in self.decision_keywords):
                decisions.append(sentence.strip())
        return decisions
    
    def extract_questions(self, text: str) -> List[str]:
        """Extract questions asked during the meeting"""
        sentences = self.extract_sentences(text)
        questions = []
        for sentence in sentences:
            if sentence.strip().endswith('?'):
                questions.append(sentence.strip())
            else:
                for pattern in self.question_patterns:
                    if re.match(pattern, sentence.lower()):
                        questions.append(sentence.strip())
                        break
        return questions
    
    def extract_topics(self, text: str) -> List[str]:
        """Extract main topics discussed"""
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'is',
            'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'we',
            'they', 'i', 'you', 'he', 'she', 'it', 'this', 'that', 'these', 'those'
        }
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        filtered_words = [w for w in words if w not in stop_words]
        counter = Counter(filtered_words)
        return [word.title() for word, count in counter.most_common(8) if count >= 3]
    
    def analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'happy', 'pleased', 'success', 'agree']
        negative_words = ['bad', 'poor', 'issue', 'problem', 'concern', 'worried', 'disagree']
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        if pos_count > neg_count * 1.5: return 'Positive'
        elif neg_count > pos_count * 1.5: return 'Negative'
        else: return 'Neutral'
    
    def generate_summary(self, text: str, max_sentences: int = 5) -> str:
        """Generate summary while keeping chronological order"""
        sentences = self.extract_sentences(text)
        if len(sentences) <= max_sentences: 
          return ' '.join(sentences)
    
        scored_sentences = []
        importance_words = ['decided', 'agreed', 'important', 'key', 'critical', 'action']
    
        for i, sentence in enumerate(sentences):
        # We keep the original index (i) to sort back later
         score = sum(1 for word in importance_words if word in sentence.lower())
         word_count = len(sentence.split())
         if 10 <= word_count <= 30: score += 1
         scored_sentences.append({'score': score, 'text': sentence, 'index': i})
    
        # 1. Sort by importance to find top sentences
         scored_sentences.sort(reverse=True, key=lambda x: x['score'])
         top_sentences = scored_sentences[:max_sentences]
    
        # 2. Re-sort by original index to maintain meeting timeline
         top_sentences.sort(key=lambda x: x['index'])
    
        return ' '.join([s['text'] for s in top_sentences])
         

    def extract_key_points(self, text: str) -> List[str]:
        """Extract key discussion points"""
        sentences = self.extract_sentences(text)
        indicators = ['main point', 'key', 'important', 'critical', 'focus on']
        key_points = [s.strip() for s in sentences if any(ind in s.lower() for ind in indicators)]
        return key_points[:7]


class MeetingAssistant:
    """Main AI Meeting Assistant"""
    
    def __init__(self):
        self.nlp_pipeline = NLPPipeline()
    
    def analyze_meeting(self, transcript: str) -> MeetingInsights:
        print("🤖 Starting AI analysis...")
        print("📝 Extracting key information...")
        
        nlp = self.nlp_pipeline
        summary = nlp.generate_summary(transcript)
        key_points = nlp.extract_key_points(transcript)
        action_items = nlp.extract_action_items(transcript)
        decisions = nlp.extract_decisions(transcript)
        participants = nlp.extract_participants(transcript)
        topics = nlp.extract_topics(transcript)
        sentiment = nlp.analyze_sentiment(transcript)
        questions = nlp.extract_questions(transcript)
        next_steps = [item['task'] for item in action_items[:3]]
        
        word_count = len(transcript.split())
        duration_estimate = f"~{word_count // 150} minutes"
        
        print("✅ Analysis complete!")
        
        return MeetingInsights(
            summary=summary, key_points=key_points, action_items=action_items,
            decisions=decisions, participants=participants, topics=topics,
            sentiment=sentiment, duration_estimate=duration_estimate,
            questions=questions, next_steps=next_steps
        )
    
    def save_report(self, insights: MeetingInsights, filename: str = None):
        """Save analysis report to file (Fixed for Windows)"""
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_dir, f"meeting_report_{timestamp}.json")
        
        with open(filename, 'w') as f:
            json.dump(asdict(insights), f, indent=2)
        
        print(f"💾 JSON Report saved to: {filename}")
        return filename
    
    def generate_formatted_report(self, insights: MeetingInsights) -> str:
        """Generate human-readable formatted report"""
        report = ["=" * 80, "📊 MEETING ANALYSIS REPORT", "=" * 80]
        report.append(f"\n🕒 Estimated Duration: {insights.duration_estimate}")
        report.append(f"😊 Overall Sentiment: {insights.sentiment}")
        
        if insights.participants:
            report.append(f"\n👥 Participants ({len(insights.participants)}):")
            for p in insights.participants: report.append(f"   • {p}")
        
        report.append(f"\n📋 SUMMARY\n" + "-" * 80 + f"\n{insights.summary}")
        
        if insights.topics:
            report.append(f"\n🏷️  MAIN TOPICS\n" + "-" * 80 + f"\n   {', '.join(insights.topics)}")
        
        if insights.key_points:
            report.append(f"\n💡 KEY POINTS\n" + "-" * 80)
            for i, p in enumerate(insights.key_points, 1): report.append(f"   {i}. {p}")

        if insights.action_items:
            report.append(f"\n📌 ACTION ITEMS ({len(insights.action_items)})\n" + "-" * 80)
            for i, item in enumerate(insights.action_items, 1):
                emoji = "🔴" if item['priority'] == 'High' else "🟡" if item['priority'] == 'Medium' else "🟢"
                report.append(f"   {i}. {emoji} [{item['priority']}] {item['task']}\n      Assignee: {item['assignee']}")

        return "\n".join(report)


def demo():
    sample_transcript = """
    Sarah: Good morning everyone. Let's start our weekly product sync. 
    John: We've decided to focus on mobile optimization.
    Lisa: When can we expect the first release?
    John: targeting end of May. Lisa, you will be leading that.
    Mark: We've identified 15 critical bugs. Tom will fix that today.
    Sarah: Action item for everyone: review the Q2 roadmap by Friday.
    """
    
    assistant = MeetingAssistant()
    insights = assistant.analyze_meeting(sample_transcript)
    
    # 1. Show report on screen
    report = assistant.generate_formatted_report(insights)
    print(report)
    
    # 2. Save JSON
    assistant.save_report(insights)
    
    # 3. Save Text (Fixed for Windows)
    output_dir = "outputs"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    text_file = os.path.join(output_dir, "meeting_report.txt")
    
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 Text report saved to: {text_file}")

if __name__ == "__main__":
    print("🚀 AI Meeting Assistant - NLP Pipeline Demo\n")
    demo()