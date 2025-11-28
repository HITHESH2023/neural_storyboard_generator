# 🎬 Neural Storyboard Generator

Turn any written story into a complete visual storyboard using AI-powered scene extraction and image generation.

---

## 🚀 Overview

**Neural Storyboard Generator** is an end-to-end pipeline that transforms a story into **scene captions**, generates **AI images** for each scene using **Stable Diffusion**, and composes them into **paginated storyboard pages**.

This project enables:

* Pre‑production storyboarding
* Creative writing visualization
* Animation and film planning
* Rapid prototyping for games & comics

---

## 🧩 System Architecture

### **1. Input Layer (Streamlit UI)**

* User enters story text
* Generates a session ID for output
* Triggers AI pipeline when "Generate Storyboard" is clicked
* Displays scenes, generated panels, and storyboard pages

### **2. Scene Processing Layer**

Performed by `scene_splitter.py`:

* Cleans text (removes tags, extra spaces)
* Splits text into sentences using regex
* Groups sentences into meaningful scene captions (≥5 words)
* Applies `MAX_SCENES` limit

### **3. Image Generation Layer**

Handled by `image_generator.py` using Stable Diffusion:

* Converts caption text to CLIP embeddings
* Generates deterministic noise latents using seeded generators
* Runs UNet denoising (25 steps)
* VAE decodes latent → final 512×512 image
* Saves images as `panel_XX.png`

### **4. Storyboard Rendering Layer**

Handled by `storyboard_renderer.py`:

* Places images into 3×3 grids
* Writes captions underneath
* Dynamically adjusts page height
* Exports multi‑page storyboards as PNG or optional PDF

### **5. Output Layer**

Directory structure:

```
outputs/
   <session_id>/
      images/
      storyboards/
```

Provides downloadable storyboard pages.

---

## 📂 Project Structure

```
├── app.py                     # Streamlit UI
├── main.py                    # CLI entrypoint
├── config.py                  # Global configuration
├── modules/
│   ├── scene_splitter.py      # Scene extraction logic
│   ├── image_generator.py     # Stable Diffusion wrapper
│   ├── storyboard_renderer.py # Storyboard page creator
│   └── utils.py               # Directory helpers
├── outputs/                   # Auto-generated files
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/neural-storyboard-generator.git
cd neural-storyboard-generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download Stable Diffusion v1.5

Place the SD v1.5 model in your HuggingFace cache directory:

```
~/.cache/huggingface/diffusers/runwayml/stable-diffusion-v1-5/
```

Or edit `SD_MODEL` in `config.py`.

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

---

## 🧠 How It Works (Detailed)

### **A) Scene Extraction**

* Cleans the raw input
* Splits text into sentences
* Forms scenes with a minimum word count

### **B) CLIP Embedding (Inside Stable Diffusion)**

* Captions are tokenized
* Transformer text encoder → CLIP embeddings
* Embeddings guide UNet during denoising

### **C) Diffusion Process**

1. Start with pure random Gaussian noise
2. UNet predicts noise to remove
3. 25 iterative denoising steps refine the latent
4. VAE decodes final latent → RGB image

### **D) Storyboard Creation**

* Combines images and captions
* Builds multi‑page storyboards
* Saves pages as PNG/PDF

---

## 🖼️ Example Output

* Extracted scene captions
* Individual image panels
* Storyboard pages (page_01.png, page_02.png, ...)

---

## 🛠️ Configuration (`config.py`)

```python
DEVICE = "cuda"
MAX_SCENES = 128
T5_MODEL = "t5-small"     # (Not used but kept for expansion)
SD_MODEL = "runwayml/stable-diffusion-v1-5"
OUTPUT_DIR = "outputs"
HF_TOKEN_ENV = "HF_TOKEN"
```

---

## 🧪 Command-Line Usage

```bash
python main.py
```

Enter a story when prompted. The pipeline runs end‑to‑end.

---

## 📝 Roadmap

* [ ] Optional LLM scene enhancer
* [ ] Character consistency across panels
* [ ] More rendering layouts (2×2, comic style, manga style)
* [ ] Built-in PDF export with custom covers
* [ ] Style presets (anime, sketch, noir, cinematic)

---

## 🤝 Contributing

Pull requests are welcome. Please maintain modular code structure.

---

## 📄 License

MIT License — free for both personal and commercial use.
