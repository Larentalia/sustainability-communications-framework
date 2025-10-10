"""
Sustainability Communications Framework - Content Analyser Module

This module analyses regulatory text complexity and extracts key concepts 
for an effective seller communication strategy.

Author: Begoña Penón
"""

import re
import json
from typing import Dict, List, Tuple
from collections import Counter
import statistics


class ContentAnalyzer:
    """
    Analyses sustainability compliance documents to support strategic communication decisions.
    
    Key capabilities:
    - Complexity scoring for different audience segments
    - Key concept extraction for priority messaging
    - Translation readiness assessment for multilingual campaigns
    """
    
    def __init__(self, content_segments):
        # Save segments received from class instantiation
        self.content_segments = content_segments
        self.sustainability_elements = []

        # Common sustainability/EPR terminology for enhanced analysis
        self.epr_keywords = {
            'high_priority': [
                'extended producer responsibility', 'epr', 'compliance', 'liability',
                'packaging waste', 'recycling targets', 'producer obligations',
                'registration requirements', 'reporting deadlines', 'penalties'
            ],
            'medium_priority': [
                'circular economy', 'waste prevention', 'environmental impact',
                'product lifecycle', 'take-back programs', 'eco-design',
                'material recovery', 'producer register'
            ],
            'process_terms': [
                'register', 'report', 'submit', 'comply', 'deadline', 'requirement',
                'obligation', 'documentation', 'evidence', 'certification'
            ]
        }
        
        # Complexity indicators that may confuse sellers
        self.complexity_indicators = [
            'notwithstanding', 'pursuant to', 'aforementioned', 'whereas',
            'hereinafter', 'thereof', 'whereby', 'insofar as', 'provided that'
        ]
    
    
    def detect_keywords(self):
        """
        Search keywords inside the segments and adds them to sustainability_elements.
        """
        for segment in self.content_segments:
            lower_segment = segment.lower()
            for category, keywords in self.epr_keywords.items():
                for kw in keywords:
                    if kw in lower_segment:
                        self.sustainability_elements.append((kw, category))
        return self.sustainability_elements



    def analyze_text_complexity(self, text: str) -> Dict:
        """
        Comprehensive text complexity analysis for communication strategy planning.
        
        Returns complexity metrics essential for stakeholder-appropriate messaging.
        """
        words = text.lower().split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Basic readability metrics
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        
        # Syllable estimation (simplified)
        syllables = sum([self._count_syllables(word) for word in words])
        avg_syllables_per_word = syllables / len(words) if words else 0
        
        # Flesch Reading Ease Score (adapted for regulatory content)
        flesch_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        
        # Legal/regulatory complexity indicators
        legal_complexity = len([word for word in words if word in self.complexity_indicators])
        legal_complexity_ratio = legal_complexity / len(words) if words else 0
        
        # EPR-specific terminology density
        epr_density = self._calculate_epr_density(text.lower())
        
        return {
            'total_words': len(words),
            'total_sentences': len(sentences),
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'avg_syllables_per_word': round(avg_syllables_per_word, 2),
            'flesch_reading_ease': round(flesch_score, 2),
            'readability_level': self._interpret_flesch_score(flesch_score),
            'legal_complexity_ratio': round(legal_complexity_ratio, 4),
            'epr_terminology_density': epr_density,
            'recommended_audience': self._recommend_audience_segment(flesch_score, legal_complexity_ratio),
            'adaptation_priority': self._assess_adaptation_priority(flesch_score, legal_complexity_ratio, epr_density)
        }
    
    def extract_key_concepts(self, text: str, top_n: int = 10) -> Dict:
        """
        Extract priority concepts for strategic message development.
        
        Essential for creating targeted seller communications and training materials.
        """
        text_lower = text.lower()
        
        # Find EPR-specific concepts
        found_concepts = {
            'high_priority': [],
            'medium_priority': [],
            'process_terms': []
        }
        
        for priority_level, keywords in self.epr_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Count occurrences for importance weighting
                    count = text_lower.count(keyword)
                    found_concepts[priority_level].append({
                        'term': keyword,
                        'frequency': count,
                        'importance_score': count * self._get_priority_weight(priority_level)
                    })
        
        # Extract general important phrases (2-4 words)
        phrases = self._extract_important_phrases(text, top_n)
        
        # Identify action items and deadlines
        action_items = self._identify_action_items(text)
        deadlines = self._identify_deadlines(text)
        
        return {
            'epr_concepts': found_concepts,
            'key_phrases': phrases,
            'action_items': action_items,
            'critical_deadlines': deadlines,
            'communication_priorities': self._rank_communication_priorities(found_concepts, action_items)
        }
    
    def assess_translation_readiness(self, text: str) -> Dict:
        """
        Evaluate text suitability for multilingual seller communications.
        
        Critical for EU marketplace communication strategy.
        """
        # Cultural-specific terms that may not translate well
        cultural_terms = [
            'due diligence', 'good faith', 'reasonable care', 'best efforts',
            'state of the art', 'common practice', 'industry standard'
        ]
        
        # Technical terms requiring glossary
        technical_density = len(re.findall(r'\b[A-Z]{2,}\b', text))  # Acronyms
        
        cultural_issues = [term for term in cultural_terms if term.lower() in text.lower()]
        
        # Sentence complexity for translation
        sentences = re.split(r'[.!?]+', text)
        sentence_lengths = [len(sentence.split()) for sentence in sentences if sentence.strip()]
        avg_sentence_length = statistics.mean(sentence_lengths) if sentence_lengths else 0
        
        return {
            'cultural_adaptation_needed': len(cultural_issues) > 0,
            'cultural_terms_found': cultural_issues,
            'technical_density_score': technical_density,
            'avg_sentence_length': round(avg_sentence_length, 2),
            'translation_difficulty': self._assess_translation_difficulty(
                len(cultural_issues), technical_density, avg_sentence_length
            ),
            'recommended_localization_strategy': self._recommend_localization_strategy(
                len(cultural_issues), technical_density
            )
        }
    
    def generate_communication_recommendations(self, text: str) -> Dict:
        """
        Strategic recommendations for seller communication campaigns.
        
        Combines all analysis elements into an actionable communication strategy.
        """
        complexity = self.analyze_text_complexity(text)
        concepts = self.extract_key_concepts(text)
        translation = self.assess_translation_readiness(text)
        
        # Strategic recommendations based on analysis
        recommendations = {
            'primary_message_focus': self._determine_primary_focus(concepts),
            'audience_segmentation': self._recommend_segmentation(complexity),
            'channel_strategy': self._recommend_channels(complexity, concepts),
            'content_adaptation_needs': self._identify_adaptation_needs(complexity, translation),
            'crisis_communication_risk': self._assess_crisis_risk(concepts, complexity),
            'success_metrics_focus': self._recommend_success_metrics(concepts, complexity)
        }
        
        return {
            'analysis_summary': {
                'complexity_analysis': complexity,
                'key_concepts': concepts,
                'translation_readiness': translation
            },
            'strategic_recommendations': recommendations,
            'implementation_priority': self._calculate_implementation_priority(
                complexity, concepts, translation
            )
        }
    
    # Helper methods
    def _count_syllables(self, word: str) -> int:
        """Simplified syllable counting for readability analysis."""
        word = word.lower()
        vowels = 'aeiouy'
        syllables = 0
        prev_was_vowel = False
        
        for char in word:
            if char in vowels:
                if not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = True
            else:
                prev_was_vowel = False
                
        if word.endswith('e'):
            syllables -= 1
        
        return max(1, syllables)
    
    def _calculate_epr_density(self, text: str) -> Dict:
        """Calculate density of EPR-related terminology."""
        total_words = len(text.split())
        densities = {}
        
        for priority, keywords in self.epr_keywords.items():
            count = sum(text.count(keyword) for keyword in keywords)
            densities[priority] = round(count / total_words * 100, 2) if total_words > 0 else 0
        
        return densities
    
    def _interpret_flesch_score(self, score: float) -> str:
        """Interpret Flesch Reading Ease score for business context."""
        if score >= 90:
            return "Very Easy (5th grade level)"
        elif score >= 80:
            return "Easy (6th grade level)"
        elif score >= 70:
            return "Fairly Easy (7th grade level)"
        elif score >= 60:
            return "Standard (8th-9th grade level)"
        elif score >= 50:
            return "Fairly Difficult (10th-12th grade level)"
        elif score >= 30:
            return "Difficult (College level)"
        else:
            return "Very Difficult (Graduate level)"
    
    def _recommend_audience_segment(self, flesch_score: float, legal_complexity: float) -> str:
        """Recommend target audience based on complexity analysis."""
        if flesch_score >= 60 and legal_complexity < 0.02:
            return "All seller segments"
        elif flesch_score >= 50 and legal_complexity < 0.05:
            return "Experienced sellers and enterprise accounts"
        else:
            return "Legal/compliance teams and enterprise sellers only"
    
    def _assess_adaptation_priority(self, flesch_score: float, legal_complexity: float, epr_density: Dict) -> str:
        """Assess priority level for content adaptation."""
        total_epr_density = sum(epr_density.values())
        
        if flesch_score < 50 or legal_complexity > 0.05 or total_epr_density > 5:
            return "HIGH - Requires significant simplification"
        elif flesch_score < 60 or legal_complexity > 0.02 or total_epr_density > 3:
            return "MEDIUM - Moderate adaptation needed"
        else:
            return "LOW - Minor adjustments sufficient"
    
    def _get_priority_weight(self, priority_level: str) -> int:
        """Weight concepts by strategic priority."""
        weights = {'high_priority': 3, 'medium_priority': 2, 'process_terms': 2}
        return weights.get(priority_level, 1)
    
    def _extract_important_phrases(self, text: str, top_n: int) -> List[Dict]:
        """Extract multi-word phrases likely to be important for sellers."""
        # Simple n-gram extraction for important phrases
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Generate 2-3 word phrases
        phrases = []
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            phrases.append(phrase)
        
        # Count frequency and return top phrases
        phrase_counts = Counter(phrases)
        top_phrases = phrase_counts.most_common(top_n)
        
        return [{'phrase': phrase, 'frequency': count} for phrase, count in top_phrases]
    
    def _identify_action_items(self, text: str) -> List[str]:
        """Identify actionable items sellers need to complete."""
        action_patterns = [
            r'must\s+\w+',
            r'shall\s+\w+',
            r'required\s+to\s+\w+',
            r'obligation\s+to\s+\w+',
            r'need\s+to\s+\w+'
        ]
        
        actions = []
        for pattern in action_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            actions.extend(matches)
        
        return list(set(actions))  # Remove duplicates
    
    def _identify_deadlines(self, text: str) -> List[str]:
        """Identify time-sensitive information."""
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{1,2}\s+\w+\s+\d{4}',
            r'by\s+\w+\s+\d{1,2}',
            r'before\s+\w+\s+\d{1,2}'
        ]
        
        deadlines = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            deadlines.extend(matches)
        
        return deadlines
    
    def _rank_communication_priorities(self, concepts: Dict, actions: List) -> List[str]:
        """Rank what should be communicated first."""
        priorities = []
        
        # High priority concepts come first
        if concepts['high_priority']:
            priorities.append("Compliance obligations and liability")
        
        # Action items are urgent
        if actions:
            priorities.append("Required seller actions")
        
        # Process terms indicate procedural information
        if concepts['process_terms']:
            priorities.append("How-to procedures and documentation")
        
        # Medium priority for context
        if concepts['medium_priority']:
            priorities.append("Background context and benefits")
        
        return priorities
    
    def _assess_translation_difficulty(self, cultural_terms: int, technical_density: int, avg_sentence: float) -> str:
        """Assess overall translation difficulty."""
        score = cultural_terms * 2 + technical_density + (avg_sentence / 10)
        
        if score > 15:
            return "HIGH - Professional legal translation required"
        elif score > 8:
            return "MEDIUM - Specialized translation with review needed"
        else:
            return "LOW - Standard business translation sufficient"
    
    def _recommend_localization_strategy(self, cultural_terms: int, technical_density: int) -> List[str]:
        """Recommend specific localization approaches."""
        strategies = []
        
        if cultural_terms > 0:
            strategies.append("Create culture-specific explanatory content")
        
        if technical_density > 5:
            strategies.append("Develop multilingual glossary")
            strategies.append("Include visual aids and diagrams")
        
        strategies.append("Implement local review by native speakers")
        strategies.append("Test comprehension with local seller focus groups")
        
        return strategies
    
    def _determine_primary_focus(self, concepts: Dict) -> str:
        """Determine primary message focus based on content analysis."""
        high_priority_count = len(concepts['high_priority'])
        process_count = len(concepts['process_terms'])
        
        if high_priority_count > process_count:
            return "Compliance importance and consequences"
        elif process_count > 0:
            return "Step-by-step guidance and procedures"
        else:
            return "General awareness and education"
    
    def _recommend_segmentation(self, complexity: Dict) -> List[str]:
        """Recommend audience segmentation strategy."""
        segments = ["All sellers"]  # Base segment
        
        if complexity['flesch_reading_ease'] < 50:
            segments = ["New/Small sellers", "Experienced sellers", "Enterprise accounts"]
        elif complexity['legal_complexity_ratio'] > 0.02:
            segments = ["General sellers", "Sellers with legal support"]
        
        return segments
    
    def _recommend_channels(self, complexity: Dict, concepts: Dict) -> Dict[str, List[str]]:
        """Recommend communication channels based on content complexity."""
        if complexity['flesch_reading_ease'] < 40:
            return {
                "primary": ["Webinars", "One-on-one consultations"],
                "secondary": ["Detailed guides", "FAQ sections"],
                "avoid": ["Email", "Brief notifications"]
            }
        elif len(concepts['action_items']) > 5:
            return {
                "primary": ["Interactive tutorials", "Step-by-step guides"],
                "secondary": ["Email sequences", "Dashboard notifications"],
                "avoid": ["Single announcements"]
            }
        else:
            return {
                "primary": ["Email", "Dashboard notifications"],
                "secondary": ["Help center articles", "Video tutorials"],
                "avoid": ["Complex webinars"]
            }
    
    def _identify_adaptation_needs(self, complexity: Dict, translation: Dict) -> List[str]:
        """Identify specific content adaptation requirements."""
        needs = []
        
        if complexity['flesch_reading_ease'] < 50:
            needs.append("Simplify sentence structure and vocabulary")
        
        if complexity['legal_complexity_ratio'] > 0.02:
            needs.append("Add plain language explanations for legal terms")
        
        if translation['cultural_adaptation_needed']:
            needs.append("Develop region-specific examples and references")
        
        if translation['technical_density_score'] > 5:
            needs.append("Create visual aids and infographics")
        
        return needs
    
    def _assess_crisis_risk(self, concepts: Dict, complexity: Dict) -> str:
        """Assess likelihood of communication causing confusion or backlash."""
        risk_factors = 0
        
        # High complexity increases confusion risk
        if complexity['flesch_reading_ease'] < 40:
            risk_factors += 2
        
        # Many high-priority compliance items increase stress
        if len(concepts['high_priority']) > 5:
            risk_factors += 1
        
        # Many action items can overwhelm
        if len(concepts['action_items']) > 8:
            risk_factors += 1
        
        if risk_factors >= 3:
            return "HIGH - Implement crisis communication protocols"
        elif risk_factors >= 1:
            return "MEDIUM - Monitor sentiment closely"
        else:
            return "LOW - Standard monitoring sufficient"
    
    def _recommend_success_metrics(self, concepts: Dict, complexity: Dict) -> List[str]:
        """Recommend KPIs for measuring communication effectiveness."""
        metrics = ["Open rates", "Click-through rates"]  # Base metrics
        
        if len(concepts['action_items']) > 0:
            metrics.append("Action completion rates")
            metrics.append("Time to compliance")
        
        if complexity['flesch_reading_ease'] < 50:
            metrics.append("Comprehension survey scores")
            metrics.append("Follow-up question volume")
        
        metrics.extend([
            "Seller satisfaction scores",
            "Support ticket reduction",
            "Sentiment analysis scores"
        ])
        
        return metrics
    
    def _calculate_implementation_priority(self, complexity: Dict, concepts: Dict, translation: Dict) -> str:
        """Calculate overall implementation priority for communication strategy."""
        priority_score = 0
        
        # Complexity adds urgency
        if complexity['flesch_reading_ease'] < 40:
            priority_score += 3
        elif complexity['flesch_reading_ease'] < 60:
            priority_score += 1
        
        # High-priority concepts need immediate attention
        priority_score += len(concepts['high_priority'])
        
        # Translation challenges add complexity
        if translation['translation_difficulty'].startswith("HIGH"):
            priority_score += 2
        
        if priority_score >= 6:
            return "URGENT - Immediate strategic intervention required"
        elif priority_score >= 3:
            return "HIGH - Priority resource allocation needed"
        else:
            return "MEDIUM - Standard implementation timeline"


# Example usage and testing functionality
if __name__ == "__main__":
    # Example EPR regulation text for demonstration
    sample_epr_text = """
    Extended Producer Responsibility (EPR) requirements mandate that producers 
    who first place packaging on the market must register with the national 
    packaging authority and comply with recycling targets. Producers must 
    submit annual reports by March 31st detailing packaging quantities and 
    materials. Non-compliance may result in penalties up to €50,000. 
    Registration must be completed before first market placement.
    """
    
    analyzer = ContentAnalyzer()
    
    print("=== Sustainability Communications Framework Demo ===\n")
    
    # Run comprehensive analysis
    results = analyzer.generate_communication_recommendations(sample_epr_text)
    
    print("COMPLEXITY ANALYSIS:")
    complexity = results['analysis_summary']['complexity_analysis']
    print(f"  Reading Level: {complexity['readability_level']}")
    print(f"  Recommended Audience: {complexity['recommended_audience']}")
    print(f"  Adaptation Priority: {complexity['adaptation_priority']}\n")
    
    print("KEY CONCEPTS IDENTIFIED:")
    concepts = results['analysis_summary']['key_concepts']
    print(f"  Communication Priorities: {', '.join(concepts['communication_priorities'])}")
    print(f"  Critical Deadlines: {concepts['critical_deadlines']}\n")
    
    print("STRATEGIC RECOMMENDATIONS:")
    recommendations = results['strategic_recommendations']
    print(f"  Primary Focus: {recommendations['primary_message_focus']}")
    print(f"  Audience Segments: {', '.join(recommendations['audience_segmentation'])}")
    print(f"  Crisis Risk Level: {recommendations['crisis_communication_risk']}")
    print(f"  Implementation Priority: {results['implementation_priority']}")
    
    print("\n=== Framework Ready for Implementation ===")
