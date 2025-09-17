import torch
from PIL import Image
import torch.nn.functional as f

class VisualClassified:

    def __init__(self, model, preprocess, tokenizer,encode_categories, device='cpu'):
        self.model = model
        self.preprocess = preprocess
        self.tokenizer = tokenizer
        self.device = device
        self.encode_categories = encode_categories



    def classify_openclip(self, image: Image.Image):
        x = self.preprocess(image).unsqueeze(0).to(self.device)          # [1,3,H,W]
        with torch.no_grad():
            img_vec = self.model.encode_image(x)                    # [1,D]
        img_vec = f.normalize(img_vec, dim=-1)                 # נרמול לתמונת הקלט בלבד
        logits = img_vec @ self.encode_categories.to(self.device).T           # [1,C]
        return logits.softmax(dim=-1).squeeze(0)               # [C] – וקטור הסיווג



    def classify_frames(self, frames_gen):
        return torch.stack([
            self.classify_openclip(frame)
            for frame in frames_gen])