import os
import difflib

class DiffAnalyzer:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def analyze_diff(self):
        """Analyzes the difference between two files and returns a detailed report."""
        with open(self.file1, 'r') as f1, open(self.file2, 'r') as f2:
            file1_lines = f1.readlines()
            file2_lines = f2.readlines()

        diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=self.file1, tofile=self.file2)
        diff_report = ''.join(diff)

        return diff_report

    def detect_changes(self):
        """Detects the types of changes between the two files and returns a summary."""
        with open(self.file1, 'r') as f1, open(self.file2, 'r') as f2:
            file1_lines = f1.readlines()
            file2_lines = f2.readlines()

        diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=self.file1, tofile=self.file2)
        diff_lines = list(diff)

        changes = {
            'additions': 0,
            'deletions': 0,
            'modifications': 0
        }

        for line in diff_lines:
            if line.startswith('+'):
                changes['additions'] += 1
            elif line.startswith('-'):
                changes['deletions'] += 1
            elif line.startswith(' '):
                changes['modifications'] += 1

        return changes

    def generate_html_report(self):
        """Generates an HTML report comparing the two files."""
        diff_report = self.analyze_diff()
        changes = self.detect_changes()

        html_report = f"""
        <html>
        <head>
            <title>Diff Report</title>
        </head>
        <body>
            <h1>Diff Report</h1>
            <h2>Changes Summary</h2>
            <p>Additions: {changes['additions']}</p>
            <p>Deletions: {changes['deletions']}</p>
            <p>Modifications: {changes['modifications']}</p>
            <h2>Diff Details</h2>
            <pre>{diff_report}</pre>
        </body>
        </html>
        """

        return html_report
