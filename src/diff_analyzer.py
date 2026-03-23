import re
from typing import Dict, List, Tuple

class DiffAnalyzer:
    def __init__(self):
        self.change_patterns = {
            'api_change': r'(API|api|endpoint|route)',
            'security': r'(password|token|secret|auth|crypt)',
            'database': r'(SELECT|INSERT|UPDATE|DELETE|CREATE TABLE)',
            'dependency': r'(requirements.txt|package.json|Gemfile|\bdep\b)',
            'config': r'(config|settings|env|yaml|yml)'
        }

    def parse_diff(self, diff_content: str) -> Dict[str, List[str]]:
        """Parse git diff content and categorize changes."""
        lines = diff_content.split('\n')
        changes = {
            'files_changed': [],
            'additions': [],
            'deletions': [],
            'critical_changes': []
        }
        
        current_file = ''
        
        for line in lines:
            if line.startswith('diff --git'):
                current_file = line.split()[-1][2:]
                changes['files_changed'].append(current_file)
            elif line.startswith('+') and not line.startswith('+++'):
                changes['additions'].append(line[1:])
                self._analyze_critical_change(line[1:], current_file, changes)
            elif line.startswith('-') and not line.startswith('---'):
                changes['deletions'].append(line[1:])
                self._analyze_critical_change(line[1:], current_file, changes)
                
        return changes

    def _analyze_critical_change(self, line: str, filename: str, changes: Dict[str, List[str]]):
        """Analyze if a change is critical based on predefined patterns."""
        for change_type, pattern in self.change_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                message = f'{change_type.upper()} change detected in {filename}: {line.strip()}'
                changes['critical_changes'].append(message)

    def generate_summary(self, changes: Dict[str, List[str]]) -> Tuple[str, List[str]]:
        """Generate a human-readable summary of the changes."""
        summary = []
        warnings = []
        
        summary.append(f"Files modified: {len(changes['files_changed'])}\n")
        summary.append(f"Total additions: {len(changes['additions'])}\n")
        summary.append(f"Total deletions: {len(changes['deletions'])}\n")
        
        if changes['critical_changes']:
            warnings = changes['critical_changes']
            summary.append("\nCritical changes detected:\n")
            for warning in warnings:
                summary.append(f"- {warning}\n")
                
        return ''.join(summary), warnings

    def analyze_impact(self, changes: Dict[str, List[str]]) -> str:
        """Analyze the potential impact of changes."""
        impact_level = 'LOW'
        
        if any('security' in change.lower() for change in changes['critical_changes']):
            impact_level = 'HIGH'
        elif len(changes['critical_changes']) > 3:
            impact_level = 'MEDIUM'
        elif len(changes['files_changed']) > 10:
            impact_level = 'MEDIUM'
            
        return impact_level

    def get_file_statistics(self, changes: Dict[str, List[str]]) -> Dict[str, int]:
        """Get detailed statistics for changed files."""
        stats = {}
        
        for file in changes['files_changed']:
            stats[file] = {
                'additions': len([l for l in changes['additions'] if file in l]),
                'deletions': len([l for l in changes['deletions'] if file in l])
            }
            
        return stats