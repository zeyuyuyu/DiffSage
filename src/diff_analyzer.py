from typing import Dict, List, Tuple
import re
from dataclasses import dataclass

@dataclass
class DiffChange:
    type: str  # 'add', 'remove', or 'modify'
    content: str
    line_number: int
    impact_score: float

class DiffAnalyzer:
    def __init__(self):
        self.change_patterns = {
            'function': r'\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'class': r'\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'import': r'\s*(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_.*]*)',
        }
        
    def analyze_diff(self, diff_content: str) -> Dict:
        changes = self._parse_diff(diff_content)
        summary = self._generate_summary(changes)
        impact_score = self._calculate_impact(changes)
        
        return {
            'changes': changes,
            'summary': summary,
            'impact_score': impact_score,
            'recommendations': self._generate_recommendations(changes, impact_score)
        }
    
    def _parse_diff(self, diff_content: str) -> List[DiffChange]:
        changes = []
        current_line = 0
        
        for line in diff_content.split('\n'):
            if line.startswith('+'):
                change_type = 'add'
                content = line[1:]
            elif line.startswith('-'):
                change_type = 'remove'
                content = line[1:]
            else:
                current_line += 1
                continue
                
            impact = self._calculate_line_impact(content)
            changes.append(DiffChange(
                type=change_type,
                content=content,
                line_number=current_line,
                impact_score=impact
            ))
            current_line += 1
            
        return changes
    
    def _calculate_line_impact(self, line: str) -> float:
        impact = 1.0
        
        # Check for high-impact changes
        if any(re.match(pattern, line) for pattern in self.change_patterns.values()):
            impact *= 2.0
        
        # Additional impact factors
        if 'api' in line.lower():
            impact *= 1.5
        if 'security' in line.lower():
            impact *= 2.0
        if 'database' in line.lower() or 'db' in line.lower():
            impact *= 1.8
            
        return impact
    
    def _calculate_impact(self, changes: List[DiffChange]) -> float:
        if not changes:
            return 0.0
            
        total_impact = sum(change.impact_score for change in changes)
        return round(total_impact / len(changes), 2)
    
    def _generate_summary(self, changes: List[DiffChange]) -> str:
        added = len([c for c in changes if c.type == 'add'])
        removed = len([c for c in changes if c.type == 'remove'])
        
        high_impact_changes = [c for c in changes if c.impact_score > 1.5]
        
        summary = f'Changes: {added} additions, {removed} deletions\n'
        if high_impact_changes:
            summary += '\nHigh impact changes:\n'
            for change in high_impact_changes:
                summary += f'- Line {change.line_number}: {change.content[:60]}...\n'
                
        return summary
    
    def _generate_recommendations(self, changes: List[DiffChange], impact_score: float) -> List[str]:
        recommendations = []
        
        if impact_score > 2.0:
            recommendations.append('Consider breaking changes into smaller commits')
            recommendations.append('Thorough testing recommended due to high impact score')
            
        api_changes = any('api' in c.content.lower() for c in changes)
        if api_changes:
            recommendations.append('Update API documentation')
            recommendations.append('Consider version bump if API changes are breaking')
            
        security_changes = any('security' in c.content.lower() for c in changes)
        if security_changes:
            recommendations.append('Conduct security review')
            recommendations.append('Update security documentation')
            
        return recommendations