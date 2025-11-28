from PIL import Image, ImageDraw, ImageFont
import math
import os
import textwrap

class StoryboardRenderer:
    def __init__(self):
        pass

    def render(self, images_with_captions, cols=3, rows_per_page=3, size=(512, 512), caption_height=120, out_dir=None):
        """
        Renders multiple storyboard pages.
        Now dynamically adjusts page height to fit content (no huge white spaces).
        """
        
        # 1. Calculate panels per page
        panels_per_page = cols * rows_per_page
        total_images = len(images_with_captions)
        total_pages = math.ceil(total_images / panels_per_page)
        
        generated_pages = []

        # Font setup
        try:
            font = ImageFont.truetype("arial.ttf", 20)
            chars_per_line = 50 
            line_height = 24
        except OSError:
            font = ImageFont.load_default()
            chars_per_line = 70
            line_height = 15
        
        # 2. Loop through chunks (pages)
        for page_num in range(total_pages):
            start_idx = page_num * panels_per_page
            end_idx = start_idx + panels_per_page
            page_batch = images_with_captions[start_idx:end_idx]
            
            # Create Page Canvas
            w, h = size
            
            # --- CHANGE: Calculate Dynamic Height ---
            # Instead of always using rows_per_page, we count how many rows 
            # we ACTUALLY need for this batch of images.
            current_rows = math.ceil(len(page_batch) / cols)
            
            # Height is now based on current_rows, not rows_per_page
            page_h = current_rows * (h + caption_height)
            
            board = Image.new("RGB", (cols * w, page_h), "white")
            draw = ImageDraw.Draw(board)

            # Draw Panels
            for idx, (caption, img) in enumerate(page_batch):
                r, c = divmod(idx, cols)
                x = c * w
                y = r * (h + caption_height)

                # Paste Image
                img = img.resize(size)
                board.paste(img, (x, y))

                # Draw Text
                text_y = y + h + 10
                lines = textwrap.wrap(caption, width=chars_per_line)
                for line in lines[:4]: # Limit to 4 lines
                    draw.text((x + 10, text_y), line, fill="black", font=font)
                    text_y += line_height

            # Save Page
            if out_dir is None:
                out_dir = "outputs/storyboards"
            
            os.makedirs(out_dir, exist_ok=True)
            filename = f"storyboard_page_{page_num+1:02d}.png"
            full_path = os.path.join(out_dir, filename)
            
            board.save(full_path)
            generated_pages.append(full_path)
            print(f"[Saved] {full_path}")

        return generated_pages

    def convert_to_pdf(self, page_paths, out_path):
        """
        Converts a list of image paths into a single PDF.
        """
        if not page_paths:
            return None

        # Open all images
        images = [Image.open(p).convert("RGB") for p in page_paths]
        
        # Save as PDF
        base_image = images[0]
        other_images = images[1:]
        
        base_image.save(out_path, save_all=True, append_images=other_images)
        return out_path