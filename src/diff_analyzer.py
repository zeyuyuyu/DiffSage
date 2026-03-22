import os
import difflib

class DiffAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def analyze_diff(self, base_ref, compare_ref):
        """Analyze the difference between two Git references."""
        base_files = self._get_file_list(base_ref)
        compare_files = self._get_file_list(compare_ref)

        diff_report = []

        for file in base_files:
            if file in compare_files:
                base_content = self._get_file_content(base_ref, file)
                compare_content = self._get_file_content(compare_ref, file)
                file_diff = self._generate_diff(base_content, compare_content)
                if file_diff:
                    diff_report.append({
                        'file': file,
                        'diff': file_diff
                    })
            else:
                diff_report.append({
                    'file': file,
                    'diff': 'File deleted'
                })

        for file in compare_files:
            if file not in base_files:
                diff_report.append({
                    'file': file,
                    'diff': 'File added'
                })

        return diff_report

    def _get_file_list(self, ref):
        """Get the list of files for a given Git reference."""
        file_list = []
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(file_path.replace(self.repo_path + '/', ''))
        return file_list

    def _get_file_content(self, ref, file_path):
        """Get the content of a file for a given Git reference."""
        file_path = os.path.join(self.repo_path, file_path)
        with open(file_path, 'r') as file:
            return file.read()

    def _generate_diff(self, base_content, compare_content):
        """Generate a diff between two file contents."""
        diff = difflib.unified_diff(base_content.splitlines(), compare_content.splitlines())
        return '\n'.join(diff)
