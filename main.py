import os
import magic
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware

# Text processing imports
from utils.text_processing import (
    tokenize, padding_truncating, lowercase, 
    perform_stemming, perform_lemmatization, remove_stopwords
)
from utils.text_augmentation import (
    random_insertion, synonym_replacement, 
    random_swap, random_deletion
)

# Audio processing imports
from utils.audio_processing import resample, normalize as audio_normalize, trim_silence, compress
from utils.audio_augmentation import (
    time_stretch, pitch_shift, add_noise, 
    random_volume_adjustment, time_shift
)

# Image processing imports
from utils.image_processing import (
    resize, normalize as image_normalize, 
    grayscaling, crop_image, denoise_image
)
from utils.image_augmentation import (
    random_horizontal_flip, random_vertical_flip, 
    random_rotation as image_rotation, 
    random_scaling as image_scaling, color_jitter
)

# 3D processing imports
from utils.three_d_processing import normalization as normalize_3d, centering
from utils.three_d_augmentation import (
    rotation as rotate_3d, 
    scaling as scale_3d, 
    adding_noise
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(os.path.join("static", UPLOAD_DIR), exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(content).split('/')[0]
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    file_path = os.path.join('static/', UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    input_display = ""
    if file_type == "image":
        input_display = f"<img src='/static/{UPLOAD_DIR}/{file.filename}' alt='Uploaded Image' style='max-width: 100%; height: auto;' />"
    elif file_type == "audio":
        input_display = f"<audio controls><source src='/static/{UPLOAD_DIR}/{file.filename}' type='audio/mpeg'></audio>"
    elif file_extension == ".off":
        file_type = "3d"
        input_display = f"""
        <div id="3d-container" style="width: 100%; height: 400px;">
            <canvas id="3d-canvas" data-model-path="/static/{UPLOAD_DIR}/{file.filename}"></canvas>
        </div>
        """
    elif file_type == "text":
        lines = content.decode("utf-8").splitlines() 
        input_display = "<br>".join(lines)
    else:
        file_type = "unsupported"
        input_display = "Unsupported file type."

    preprocess_options = {
        "text": ["Tokenize", "Padding/Truncating", "Lowercase", "StopWord Removal", "Stemming", "Lemmatization"],
        "image": ["Resizing", "Normalization", "Grayscaling", "Cropping", "Denoising"],
        "audio": ["Resampling", "Normalization", "Trimming Silence", "Dynamic Range Compression"],
        "3d": ["Normalization", "Centering"]
    }

    augmentation_options = {
        "text": ["Synonym Replacement", "Random Insertion", "Random Deletion", "Random Swap"],
        "image": ["Horizontal Flip", "Vertical Flip", "Rotation", "Scaling", "Brightness Adjustment"],
        "audio": ["Time Stretching", "Pitch Shifting", "Random Noise Addition", "Random Volume Adjustment", "Time Shifting"],
        "3d": ["Rotation", "Scaling", "Adding Noise"]
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "uploaded_content": input_display,
        "file_type": file_type,
        "preprocess_options": preprocess_options.get(file_type, []),
        "augmentation_options": augmentation_options.get(file_type, []),
        "file_path": file_path
    })

@app.post("/apply_preprocess/")
async def apply_preprocess(request: Request):
    data = await request.json()
    option = data.get("option")
    file_path = data.get("file_path")
    file_type = data.get("file_type")
    
    # Text Preprocessing
    if option == "Tokenize":
        result = tokenize(file_path)
    elif option == "Padding/Truncating":
        result = padding_truncating(file_path)
    elif option == "Lowercase":
        result = lowercase(file_path)
    elif option == "StopWord Removal":
        result = remove_stopwords(file_path)
    elif option == "Stemming":
        result = perform_stemming(file_path)
    elif option == "Lemmatization":
        result = perform_lemmatization(file_path)
    
    # Image Preprocessing
    elif option == "Resizing":
        result = resize(file_path)
    elif option == "Normalization" and file_type == "image":
        result = image_normalize(file_path)
    elif option == "Grayscaling":
        result = grayscaling(file_path)
    elif option == "Cropping":
        result = crop_image(file_path)
    elif option == "Denoising":
        result = denoise_image(file_path)
    
    # Audio Preprocessing
    elif option == "Resampling":
        result = resample(file_path)
    elif option == "Dynamic Range Compression":
        result = compress(file_path)
    elif option == "Normalization" and file_type == "audio":
        result = audio_normalize(file_path)
    elif option == "Trimming Silence":
        result = trim_silence(file_path)
    
    # 3D Preprocessing
    elif option == "Normalization" and file_type == "3d":
        result = normalize_3d(file_path)
        if not result.startswith("Error"):
            result = '/static/uploads/' + os.path.basename(result)
    elif option == "Centering" and file_type == "3d":
        result = centering(file_path)
        if not result.startswith("Error"):
            result = '/static/uploads/' + os.path.basename(result)
    else:
        result = "Invalid option selected."

    return JSONResponse({"output": result, "file_type": file_type})

@app.post("/apply_augmentation/")
async def apply_augmentation(request: Request):
    data = await request.json()
    option = data.get("option")
    file_path = data.get("file_path")
    file_type = data.get("file_type")

    # Text Augmentation
    if option == "Synonym Replacement":
        result = synonym_replacement(file_path)
    elif option == "Random Insertion":
        result = random_insertion(file_path)
    elif option == "Random Deletion":
        result = random_deletion(file_path)
    elif option == "Random Swap":
        result = random_swap(file_path)
    
    # Image Augmentation
    elif option == "Horizontal Flip" and file_type == "image":
        result = random_horizontal_flip(file_path)
    elif option == "Vertical Flip" and file_type == "image":
        result = random_vertical_flip(file_path)
    elif option == "Rotation" and file_type == "image":
        result = image_rotation(file_path)
    elif option == "Scaling" and file_type == "image":
        result = image_scaling(file_path)
    elif option == "Brightness Adjustment" and file_type == "image":
        result = color_jitter(file_path)
    
    # Audio Augmentation
    elif option == "Time Stretching":
        result = time_stretch(file_path)
    elif option == "Pitch Shifting":
        result = pitch_shift(file_path)
    elif option == "Random Noise Addition":
        result = add_noise(file_path)
    elif option == "Random Volume Adjustment":
        result = random_volume_adjustment(file_path)
    elif option == "Time Shifting":
        result = time_shift(file_path)
    
    # 3D Augmentation
    elif option == "Rotation" and file_type == "3d":
        result = rotate_3d(file_path)
        if not result.startswith("Error"):
            result = '/static/uploads/' + os.path.basename(result)
    elif option == "Scaling" and file_type == "3d":
        result = scale_3d(file_path)
        if not result.startswith("Error"):
            result = '/static/uploads/' + os.path.basename(result)
    elif option == "Adding Noise" and file_type == "3d":
        result = adding_noise(file_path)
        if not result.startswith("Error"):
            result = '/static/uploads/' + os.path.basename(result)
    else:
        result = "Invalid option selected."

    return JSONResponse({"output": result, "file_type": file_type})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8015)
