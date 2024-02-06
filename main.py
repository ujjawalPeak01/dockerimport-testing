from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

# Mocking the model here
class MockModel:
    def __init__(self):
        self.loaded = False
        self.pipe = None

    def load(self):
        self.loaded = True
        self.pipe = os.environ['pass'] + "abcd"

    def unload(self):
        self.loaded = False
        self.pipe = None

    def infer(self, text):
        # Generate a simple image with the given text
        image = self.pipe
        return image



model = MockModel()
model.load()

class InferRequest(BaseModel):
    text: str


@app.get("/v2")
@app.get("/v2/models/stable-diffusion")
def version():
    return {"name": "stable-diffusion"}


@app.get("/v2/health/live")
def health_check():
    return {"status": "running"}


@app.get("/v2/health/ready")
def health_ready():
    return {"status": "running"}


@app.get("/v2/health/live")
@app.get("/v2/health/ready")
@app.get("/v2/models/stable-diffusion/ready")
@app.get("/v2/models/stable-diffusion/versions/1/ready")
@app.get("/v2/health/live")
def health_check():
    return {"status": "running"}


@app.post("/v2/models/stable-diffusion/load")
def load_model():
    if not model.loaded:
        model.load()
        return {"status": "model loaded"}
    else:
        raise HTTPException(status_code=400, detail="Model is already loaded")


@app.post("/v2/models/stable-diffusion/unload")
def unload_model():
    if model.loaded:
        model.unload()
        return {"status": "model unloaded"}
    else:
        raise HTTPException(status_code=400, detail="Model is not loaded")


@app.post("/v2/models/stable-diffusion/versions/1/infer")
@app.post("/v2/models/stable-diffusion/infer")
def generate_image(request: InferRequest):
    if not model.loaded:
        raise HTTPException(status_code=400, detail="Model is not loaded")

    text = request.text
    image = model.infer(text)
    return {"image": image}
