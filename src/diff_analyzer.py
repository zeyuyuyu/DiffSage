import spacy

class DiffAnalyzer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def analyze_diff(self, old_text, new_text):
        """Analyze the semantic differences between two text inputs."""
        old_doc = self.nlp(old_text)
        new_doc = self.nlp(new_text)

        changes = []
        for token_old, token_new in zip(old_doc, new_doc):
            if token_old.text != token_new.text:
                changes.append({
                    'old': token_old.text,
                    'new': token_new.text,
                    'pos': token_new.pos_,
                    'dep': token_new.dep_,
                    'lemma': token_new.lemma_
                })

        return changes
