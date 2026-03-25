import difflib

class DiffAnalyzer:
    def __init__(self, old_code, new_code):
        self.old_code = old_code
        self.new_code = new_code

    def analyze_semantic_diff(self):
        """Analyze the semantic differences between the old and new code."""
        old_lines = self.old_code.split('\
')
        new_lines = self.new_code.split('\
')

        diff = difflib.unified_diff(old_lines, new_lines, fromfile='old_code.py', tofile='new_code.py')

        semantic_diff = []
        for line in diff:
            if line.startswith('-') or line.startswith('+'):
                semantic_diff.append(line)

        return '\
'.join(semantic_diff)
