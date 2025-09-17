import subprocess, os
from PIL import Image

class DataHandler:
    def __init__(self, file_path, dir_path):
        self.file_path = file_path
        self.dir_path  = dir_path
        os.makedirs(self.dir_path, exist_ok=True)
        self.length = self.media_duration()

    def media_duration(self) -> float:
        try:
            out = subprocess.check_output(
                ["ffprobe","-v","error","-show_entries","format=duration",
                 "-of","default=nw=1:nk=1", self.file_path],
                text=True
            ).strip()
            dur = float(out)
            return dur if dur > 0 else 30.0
        except Exception:
            return 30.0  # fallback סביר

    def decide_frame_count(self) -> int:
        L = self.length
        if L <= 30:        return 8
        if L <= 60:        return 12
        if L <= 5*60:      return 16
        if L <= 10*60:     return 24
        if L <= 20*60:     return 36
        return 48

    def frames_by_length(self, size=(224, 224)):

        n   = max(self.decide_frame_count(), 1)
        fps = max(n / max(self.length, 0.001), 0.001)
        w,h = size
        pattern = os.path.join(self.dir_path, "f_%05d.jpg")

        subprocess.run([
            "ffmpeg","-hide_banner","-loglevel","error","-y","-an",
            "-i", self.file_path, "-map","0:v:0",
            "-vf", f"fps={fps},scale={w}:{h},format=yuvj420p",
            "-vsync","vfr", pattern
        ], check=True)

        return [os.path.join(self.dir_path, f)
                for f in sorted(os.listdir(self.dir_path))
                if f.lower().endswith(".jpg")]

    def decide_segment_count(self) -> int:
        if self.length <= 30:        return 1
        if self.length <= 60:        return 2
        if self.length <= 4 * 60:    return 6
        if self.length <= 8 * 60:   return 10
        if self.length <= 12 * 60:   return 14
        return 18


    def audio_segments_to_wav_by_length(self, seg_sec: float = 11.0, rate: int = 16000):
        d = max(self.length, 0.001)
        n = self.decide_segment_count()
        span = max(d - seg_sec, 0.0)
        starts = [0.0] if n == 1 or span == 0 else [i * (span / (n - 1)) for i in range(n)]

        files = []
        for i, s in enumerate(starts):
            out = os.path.join(self.dir_path, f"seg_{i:02d}.wav")
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-ss", f"{s:.3f}", "-t", f"{seg_sec:.3f}",
                "-i", self.file_path,
                "-vn", "-map", "0:a:0",
                "-ac", "1", "-ar", str(rate),
                "-c:a", "pcm_s16le", out
            ], check=True)
            files.append(out)

        return files

    @staticmethod
    def get_text_from_file(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def load_image(path) -> Image.Image:
        img = Image.open(path)
        return img.convert("RGB")

    @staticmethod
    def gen_load_image(gen_path):
        for path in gen_path:
            yield DataHandler.load_image(path)