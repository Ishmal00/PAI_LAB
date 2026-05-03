from transformers import pipeline

class TransformerProcessor:
    def __init__(self):
        # Summarization model load ho raha hai
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        # Named Entity Recognition (NER) for Participants
        self.ner = pipeline("ner", grouped_entities=True, model="dbmdz/bert-large-cased-finetuned-conll03-english")

    def get_summary(self, text):
        try:
            # Text agar bohot chota ho toh summarizer error deta hai
            if len(text.split()) < 30:
                return text
            summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except:
            return "Summary generation failed."

    def extract_people(self, text):
        try:
            entities = self.ner(text)
            names = set([entity['word'] for entity in entities if entity['entity_group'] == 'PER'])
            return list(names)
        except:
            return []