# 🌐 Multimodal Data Processing & Augmentation Tool

A web-based tool for processing and augmenting different types of data including 📄 text, 🖼️ images, 🎶 audio, and 🏗️ 3D models.

## ✨ Features

### 📝 Text Data
#### 🛠️ Preprocessing Options
- **Tokenization**: Splits text into individual words or tokens 📝
- **Padding/Truncating**: Adjusts text length to a fixed size by adding padding or cutting off ✂️
- **Lowercase Conversion**: Converts all text to lowercase for consistency 🔡
- **StopWord Removal**: Removes common words that don't carry significant meaning ✋
- **Stemming**: Reduces words to their root/base form 🌱
- **Lemmatization**: Converts words to their dictionary base form while considering context 📖

#### 🔄 Augmentation Options
- **Synonym Replacement**: Replaces words with their synonyms 🔄
- **Random Insertion**: Inserts random words from the text at random positions 🔀
- **Random Deletion**: Randomly removes words from the text 🗑️
- **Random Swap**: Swaps positions of words randomly 🔄

### 🖼️ Image Data
#### 🛠️ Preprocessing Options
- **Resizing**: Changes image dimensions to a specified size 📏
- **Normalization**: Scales pixel values to a standard range (0-1) 🌈
- **Grayscaling**: Converts colored images to grayscale ⚫⚪
- **Cropping**: Cuts out a portion of the image ✂️
- **Denoising**: Removes noise from images 🔇

#### 🔄 Augmentation Options
- **Horizontal Flip**: Mirrors the image horizontally ↔️
- **Vertical Flip**: Mirrors the image vertically ↕️
- **Rotation**: Rotates the image by a random angle 🔄
- **Scaling**: Increases or decreases image size randomly 🔍
- **Brightness Adjustment**: Modifies image brightness randomly ☀️

### 🎶 Audio Data
#### 🛠️ Preprocessing Options
- **Resampling**: Changes the sampling rate of audio 🎚️
- **Normalization**: Adjusts audio volume to a standard level 🔊
- **Trimming Silence**: Removes silent portions from audio 🔇
- **Dynamic Range Compression**: Reduces the difference between loud and quiet parts 🔉

#### 🔄 Augmentation Options
- **Time Stretching**: Speeds up or slows down audio without changing pitch ⏩⏪
- **Pitch Shifting**: Changes the pitch while maintaining duration 🎶
- **Random Noise Addition**: Adds background noise to audio 🎤
- **Random Volume Adjustment**: Changes audio volume randomly 🔊🔉
- **Time Shifting**: Shifts audio forward or backward in time ⏳

### 🏗️ 3D Model Data (OFF format)
#### 🛠️ Preprocessing Options
- **Normalization**: Scales the model to have unit size while preserving proportions 🏗️
- **Centering**: Moves the model center to origin (0,0,0) 📍

#### 🔄 Augmentation Options
- **Rotation**: Applies random rotation around x, y, and z axes 🔄
- **Scaling**: Randomly scales the model in different dimensions 📏
- **Adding Noise**: Adds random perturbations to vertex positions 🎛️

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/multimodal-data-tool.git

# Install required packages
pip install -r requirements.txt
```


## 🚀 Usage

1. 🔥 Start the server:
```bash
uvicorn main:app --host 127.0.0.1 --port 8015
```

2. 🌐 Open your browser and navigate to:
```
http://localhost:8015
```

3. 📤 Upload your data file:
   - 🔍 The tool automatically detects the file type
   - 📁 Supported formats:
     - 📝 Text files (.txt)
     - 🖼️ Images (.jpg, .png, etc.)
     - 🎵 Audio files (.wav, .mp3)
     - 🎲 3D models (.off)

4. ⚙️ Select preprocessing or augmentation options from the dropdown menus

5. ✨ Click "Apply" to process your data

## 🎯 Features

- ⚡ Real-time processing and preview
- 🎮 Interactive 3D model viewer with orbit controls
- 📱 Responsive design for desktop and mobile
- 🔄 Support for multiple file formats
- 🎨 Easy-to-use interface

## 🛠️ Technical Details

- Backend: FastAPI (Python)
- Frontend: HTML, CSS, JavaScript
- 3D Rendering: Three.js
- Data Processing Libraries:
  - 📝 Text: NLTK
  - 🖼️ Image: OpenCV
  - 🎵 Audio: librosa
  - 🎲 3D: trimesh