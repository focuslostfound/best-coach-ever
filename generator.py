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
        
        prompt = f"""You are generating GAME PHASES for {sport} using the Enhanced Methodology V3.

CRITICAL UNDERSTANDING:

**Phase = Game SITUATION (not a tactical response)**
- Defined ONLY by: possession state + location
- Example: "Offensive Zone Attack" = We have puck + We're in offensive zone
- NOT a play or tactic - just the situation

**What Phases Are NOT:**
❌ NOT tactical actions (those are "plays")
❌ NOT specific plays ("Drive to Net" is a play, not a phase)
❌ NOT movements ("Skating" is not a phase)
❌ NOT general concepts ("Transition" alone is too vague)

**What Phases ARE:**
✅ Game situations where possession + location define the context
✅ Clear entry/exit based on puck/ball movement
✅ Cover ALL possible game situations (no gaps)
✅ No overlaps (can't be in two phases at once)

**EXAMPLE - ICE HOCKEY PHASES (Your Reference):**

Phase 1: "Offensive Zone Attack"
- Location: Offensive zone (opponent's end)
- Possession: Team has puck
- Entry: Puck crosses blue line with possession OR gain possession in zone
- Exit: Puck leaves zone OR lose possession
- Objective: Score or create scoring chances

Phase 2: "Defensive Zone Coverage"  
- Location: Defensive zone (our end)
- Possession: Opponent has puck
- Entry: Opponent enters zone with puck OR turnover in zone
- Exit: Puck cleared OR regain possession
- Objective: Prevent goals, regain possession

Phase 3: "Neutral Zone - Team Possession"
- Location: Neutral zone (middle ice)
- Possession: Team has puck
- Entry: Team gains possession in neutral zone OR exits defensive zone
- Exit: Enter offensive zone OR lose possession
- Objective: Advance puck to offense

Phase 4: "Neutral Zone - Opponent Possession"
- Location: Neutral zone (middle ice)
- Possession: Opponent has puck
- Entry: Opponent has puck in neutral zone
- Exit: Opponent enters our zone OR we regain possession
- Objective: Prevent zone entry, force turnover

(You would add 2-4 more phases to cover faceoffs, special teams, etc.)

**KEY RULE:** Phases are SITUATIONS. Plays are TACTICAL RESPONSES to those situations.

---

YOUR TASK:

Generate 4-8 game phases for {sport} following this understanding.

Use Expert Debate System (5 personas):
1. Technical Specialist - "Is this structurally sound?"
2. Game Analyst - "Does this cover real game situations?"
3. Development Expert - "Can youth players understand this?"
4. Biomechanics Specialist - "Is this physically sensible?"
5. Best Coach Ever - "Will coaches understand and use this?"

REQUIREMENTS:
- Each phase = possession state + location (nothing more)
- Clear entry/exit conditions
- Zero overlaps between phases
- 100% coverage (all game situations included)
- Objective describes what team is trying to do IN THAT SITUATION

OUTPUT FORMAT (JSON only, no other text):

{{
  "debate_summary": "Summary of expert debate: What phases were chosen and why",
  "phases": [
    {{
      "phase_id": "P1",
      "phase_name": "Name of situation (not a tactic)",
      "location": "Where on playing surface",
      "possession_state": "Who has possession of ball/puck",
      "entry_condition": "What triggers entry into this phase",
      "exit_condition": "What triggers exit from this phase",
      "primary_objective": "What team is trying to accomplish in this situation",
      "validation_score": 0.95
    }}
  ],
  "quality_metrics": {{
    "overlap_score": 0.0,
    "coverage_score": 1.0,
    "clarity_score": 0.96,
    "consensus_achieved": true
  }},
  "expert_consensus": "Why these phases correctly define all game situations for {sport}"
}}

Think step by step. Generate phases that are SITUATIONS, not tactics.
Output ONLY valid JSON.
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
        
        # Build context about phases
        phase_context = f"**GAME PHASES FOR {sport.upper()}:**\n\n"
        for phase in phases:
            phase_context += f"**{phase['phase_id']}: {phase['phase_name']}**\n"
            phase_context += f"- Location: {phase['location']}\n"
            phase_context += f"- Possession: {phase['possession_state']}\n"
            phase_context += f"- Objective: {phase['primary_objective']}\n\n"
        
        prompt = f"""You are generating PLAYS for {sport} using the Enhanced Methodology V3.

{phase_context}

---

CRITICAL UNDERSTANDING:

**Play = Tactical RESPONSE to a phase situation**
- A specific coordinated action players execute
- Has a clear trigger condition
- Involves specific player movements
- Has a SINGLE target DL (the level when teams can execute this in games)

**What Plays Are:**
✅ Specific tactical actions ("Drive to Net", "Give-and-Go", "Pick and Roll")
✅ Coordinated movements with clear sequences
✅ Things you would draw on a whiteboard
✅ Most frequent/foundational actions in that phase
✅ NOT trick plays or specialty moves

**What Plays Are NOT:**
❌ NOT just movements ("skating fast" is not a play)
❌ NOT general concepts ("offense" is not a play)
❌ NOT the same as the phase itself

**EXAMPLE - ICE HOCKEY PLAYS FOR "OFFENSIVE ZONE ATTACK" PHASE:**

Play 1: "Drive to Net"
- Description: Puck carrier skates directly toward net with speed, attempts to score or create rebound
- Players: 1-2 (carrier + optional support)
- Target DL: 3 (DL 3 teams can execute this)
- Frequency: Very High (happens multiple times per game)
- Trigger: Clear lane to net available, puck carrier has speed

Play 2: "Give-and-Go"
- Description: Quick pass to teammate, immediate return pass while moving to create space
- Players: 2 (passer + receiver)
- Target DL: 4 (requires coordination, DL 4 teams can do this)
- Frequency: High
- Trigger: Defender pressuring puck carrier, teammate in support position

Play 3: "Basic Cycle"  
- Description: Maintain possession below goal line, rotate puck between 2-3 players
- Players: 3
- Target DL: 4 (requires sustained coordination)
- Frequency: High
- Trigger: Pressure high in slot, need to maintain possession and reset

Play 4: "Point Shot with Screen"
- Description: Defenseman shoots from blue line while forward screens goalie
- Players: 2+ (shooter + screener + others)
- Target DL: 5 (requires positioning and timing)
- Frequency: Medium
- Trigger: Puck at point, traffic in front of net

**KEY RULES:**
1. Each play has SINGLE target_dl (not a range) - when teams can execute in games
2. Generate 3-8 plays per phase
3. Most frequent and foundational only (not trick plays)
4. Clear trigger conditions
5. Distinct from each other (different situations, different actions)

---

YOUR TASK:

Generate 3-8 plays PER PHASE for the phases above.

Use Expert Debate System (5 personas):
1. Game Analyst - "Does this actually happen in games? How often?"
2. Development Expert - "What DL can execute this? What's realistic?"
3. Technical Specialist - "Is this teachable? Clear trigger?"
4. Biomechanics Specialist - "Is this physically sound for youth?"
5. Best Coach Ever - "Will this work in practice? Makes sense?"

DL Assignment Guidelines:
- DL 1-2: Very basic, individual skills
- DL 3-4: Simple coordinated actions (2-3 players)
- DL 5-6: More complex coordination and timing
- DL 7-10: Advanced plays (if full scale requested)

OUTPUT FORMAT (JSON only):

{{
  "debate_summary": "Summary of expert debate and play selection rationale",
  "plays": [
    {{
      "play_id": "PL1",
      "phase_id": "P1",
      "play_name": "Specific Play Name",
      "description": "What players actually do in this play",
      "players_involved": 2,
      "target_dl": 3,
      "frequency": "Very High",
      "trigger": "Specific situation that makes this play appropriate",
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
  "expert_consensus": "Why these plays are the most frequent and foundational for {sport}"
}}

Generate plays for ALL phases listed above.
Think: What are the MOST COMMON tactical actions in each phase?
Output ONLY valid JSON.
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
