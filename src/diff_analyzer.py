import difflib

class DiffAnalyzer:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def analyze_diff(self):
        with open(self.file1, 'r') as f1, open(self.file2, 'r') as f2:
            file1_lines = f1.readlines()
            file2_lines = f2.readlines()

        diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=self.file1, tofile=self.file2)
        return list(diff)

    def find_changes(self):
        diff = self.analyze_diff()
        changes = []
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                changes.append(line[1:])
            elif line.startswith('-') and not line.startswith('---'):
                changes.append(line[1:])
        return changes

    def find_additions(self):
        diff = self.analyze_diff()
        additions = []
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                additions.append(line[1:])
        return additions

    def find_deletions(self):
        diff = self.analyze_diff()
        deletions = []
        for line in diff:
            if line.startswith('-') and not line.startswith('---'):
                deletions.append(line[1:])
        return deletions