import re
from config import MAX_SCENES

class SceneSplitter:
    def __init__(self):
        pass

    def clean_text_file(self, text):
        """
        Removes tags and extra whitespace.
        """
        # Remove tags like <tag> </tag> <something>
        text = re.sub(r'<[^>]+>', '', text)

        # Remove multiple newlines
        text = re.sub(r'\n+', ' ', text)

        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def split_story(self, text, max_scenes=MAX_SCENES):
        """
        Splits story into visual chunks of ~20-40 words.
        """
        # 1. Clean input
        clean_text = self.clean_text_file(text)

        # 2. Sentence splitting using improved regex
        sentence_endings = r'(?<=[.!?])\s+(?=[A-Z"\'\n])'
        sentences = re.split(sentence_endings, clean_text)

        # 3. Smart chunking
        final_scenes = []
        current_chunk = ""

        MIN_WORDS_PER_PANEL = 5

        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue

            # Build chunk
            if current_chunk:
                current_chunk += " " + sent
            else:
                current_chunk = sent

            # Check size
            if len(current_chunk.split()) >= MIN_WORDS_PER_PANEL:
                final_scenes.append(current_chunk)
                current_chunk = ""

        # Add leftovers
        if current_chunk:
            final_scenes.append(current_chunk)

        # 4. Limit scenes
        return final_scenes[:max_scenes]
