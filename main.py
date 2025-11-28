from modules.scene_splitter import SceneSplitter
from modules.image_generator import ImageGenerator
from modules.storyboard_renderer import StoryboardRenderer
from modules.utils import ensure_dirs

def main():
    ensure_dirs()

    print("\n=== Neural Storyboard Generator ===\n")

    story = input("Enter story text: ").strip()
    if not story:
        print("No input given.")
        return

    print("\n[1] Splitting story into scenes...")
    splitter = SceneSplitter()
    captions = splitter.split_story(story)
    for i, c in enumerate(captions, 1):
        print(f"  Scene {i}: {c}")

    print("\n[2] Generating images...")
    gen = ImageGenerator()
    images = gen.generate_images(captions)

    print("\n[4] Rendering storyboard...")
    renderer = StoryboardRenderer()
    renderer.render(images)

    print("\n=== Done ===")

if __name__ == "__main__":
    main()
