import os

def ensure_dirs():
    for d in ["outputs/images", "outputs/storyboards", "outputs/embeddings"]:
        os.makedirs(d, exist_ok=True)
