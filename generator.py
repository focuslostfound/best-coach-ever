"""
Generation Logic for Best Coach Ever Curriculum
Handles all API calls and curriculum generation following the methodology
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from anthropic import Anthropic


class CurriculumGenerator:
    """Handles curriculum generation using Claude API and methodology"""
    
    def __init__(self, api_client: Anthropic, methodology_path: Path):
        self.client = api_client
        self.methodology_path = methodology_path
        self.methodology_content = self._load_methodology()
    
    def _load_methodology(self) -> str:
        """Load the methodology document"""
        with open(self.methodology_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _call_claude(self, prompt: str, max_tokens: int = 4000) -> str:
        """Make a call to Claude API"""
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    
    def generate_phases(self, sport: str) -> Dict[str, Any]:
        """
        Generate game phases for a sport using the expert debate system
        
        Returns:
            Dict with 'phases' (list) and 'metadata' (dict)
        """
        
        # Extract the phase generation section from methodology
        phase_section = self._extract_section("STEP 1: GAME PHASE IDENTIFICATION")
        
        prompt = f"""You are generating game phases for {sport} following the Enhanced Methodology V3.

{phase_section}

YOUR TASK:
Generate 4-8 fundamental game phases for {sport} using the Expert Debate System with all 5 personas:
- Technical Specialist (The Engineer)
- Game Analyst (The Watcher)
- Development Expert (The Teacher)
- Biomechanics Specialist (The Scientist)
- Best Coach Ever (The Synthesizer)

REQUIREMENTS:
1. Follow the multi-round debate process (5 rounds minimum)
2. Each phase must have clear entry/exit conditions
3. No overlaps between phases
4. Cover all possible game situations
5. Based on situation, not tactical response
6. Teachable to youth players

OUTPUT FORMAT:
Return your response as a JSON object with this structure:

{{
  "debate_summary": "Brief summary of the expert debate process and key decisions",
  "phases": [
    {{
      "phase_id": "P1",
      "phase_name": "Phase Name",
      "location": "Where on playing surface",
      "possession_state": "Who has possession",
      "entry_condition": "What triggers entry",
      "exit_condition": "What triggers exit",
      "primary_objective": "What team is trying to accomplish",
      "validation_score": 0.95
    }}
  ],
  "quality_metrics": {{
    "overlap_score": 0.0,
    "coverage_score": 1.0,
    "clarity_score": 0.96,
    "consensus_achieved": true
  }},
  "expert_consensus": "Summary of why these phases are correct"
}}

CRITICAL: Output ONLY valid JSON. No other text before or after the JSON.
"""
        
        response = self._call_claude(prompt, max_tokens=8000)
        
        # Parse JSON from response
        try:
            # Try to extract JSON if there's extra text
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response)
            
            return result
        except json.JSONDecodeError as e:
            # If parsing fails, return error info
            return {
                "error": f"Failed to parse response: {str(e)}",
                "raw_response": response,
                "phases": []
            }
    
    def generate_plays(self, sport: str, phases: List[Dict]) -> Dict[str, Any]:
        """
        Generate plays for each phase
        
        Args:
            sport: The sport name
            phases: List of phase dictionaries
            
        Returns:
            Dict with 'plays' (list) and 'metadata' (dict)
        """
        
        # Extract the play generation section
        play_section = self._extract_section("STEP 2: PLAY GENERATION")
        
        # Build context about phases
        phase_context = "PHASES FOR THIS SPORT:\n"
        for phase in phases:
            phase_context += f"\n{phase['phase_id']}: {phase['phase_name']}\n"
            phase_context += f"  - Location: {phase['location']}\n"
            phase_context += f"  - Possession: {phase['possession_state']}\n"
            phase_context += f"  - Objective: {phase['primary_objective']}\n"
        
        prompt = f"""You are generating plays for {sport} following the Enhanced Methodology V3.

{phase_context}

{play_section}

YOUR TASK:
Generate 3-8 plays per phase using the Expert Debate System with all 5 personas.

CRITICAL REQUIREMENTS:
1. Each play has a SINGLE target_dl (not a range) - this is when a team can execute this play
2. Most frequently occurring plays only
3. Foundational plays (not trick plays)
4. Clear trigger conditions
5. Cross-phase validation (no conflicts)

OUTPUT FORMAT:
Return ONLY valid JSON:

{{
  "debate_summary": "Brief summary of expert debate",
  "plays": [
    {{
      "play_id": "PL1",
      "phase_id": "P1",
      "play_name": "Play Name",
      "description": "What happens in this play",
      "players_involved": 2,
      "target_dl": 3,
      "frequency": "High",
      "trigger": "When this situation occurs",
      "validation_score": 0.94
    }}
  ],
  "quality_metrics": {{
    "frequency_validation": 0.92,
    "dl_assignment_validity": 0.96,
    "trigger_clarity": 0.95,
    "distinctness": 0.91,
    "cross_phase_conflicts": 0
  }},
  "expert_consensus": "Why these plays are correct"
}}

Generate plays for ALL phases. CRITICAL: Output ONLY valid JSON.
"""
        
        response = self._call_claude(prompt, max_tokens=12000)
        
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response)
            
            return result
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse response: {str(e)}",
                "raw_response": response,
                "plays": []
            }
    
    def _extract_section(self, section_header: str) -> str:
        """Extract a section from the methodology document"""
        
        # Find the section
        lines = self.methodology_content.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if section_header in line:
                in_section = True
                continue
            
            # Stop at next major section (starts with ##)
            if in_section and line.startswith('## ') and section_header not in line:
                break
            
            if in_section:
                section_lines.append(line)
        
        return '\n'.join(section_lines)


def format_phases_for_display(phases: List[Dict]) -> List[Dict]:
    """Format phases for display in a table"""
    formatted = []
    for phase in phases:
        formatted.append({
            'Phase ID': phase.get('phase_id', ''),
            'Phase Name': phase.get('phase_name', ''),
            'Location': phase.get('location', ''),
            'Possession': phase.get('possession_state', ''),
            'Entry Condition': phase.get('entry_condition', ''),
            'Exit Condition': phase.get('exit_condition', ''),
            'Objective': phase.get('primary_objective', ''),
            'Score': f"{phase.get('validation_score', 0):.2f}"
        })
    return formatted


def format_plays_for_display(plays: List[Dict]) -> List[Dict]:
    """Format plays for display in a table"""
    formatted = []
    for play in plays:
        formatted.append({
            'Play ID': play.get('play_id', ''),
            'Phase': play.get('phase_id', ''),
            'Play Name': play.get('play_name', ''),
            'Description': play.get('description', ''),
            'Target DL': play.get('target_dl', ''),
            'Frequency': play.get('frequency', ''),
            'Trigger': play.get('trigger', ''),
            'Score': f"{play.get('validation_score', 0):.2f}"
        })
    return formatted
