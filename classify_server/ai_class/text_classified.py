import torch
import tensorflow as tf
import tensorflow_hub as hub
import librosa
import csv
from collections import Counter
from sentence_transformers import SentenceTransformer, util
import whisper
from GroupAnalysis.classify_server.ai_class.file_reader import FileReader
labels_csv = tf.keras.utils.get_file(
            "yamnet_class_map.csv",
            "https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv")


class TextClassified:

    def __init__(self, categories):
        self.model_sound_classified = hub.load("https://tfhub.dev/google/yamnet/1")
        self.model_text_classified = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        self.model_audio_to_text = whisper.load_model("small")
        self.emb_cats = self.model_text_classified.encode(categories, convert_to_tensor=True)
        self.cat_to_whisper = set(FileReader.load_file())
        self.labels = [r["display_name"] for r in csv.DictReader(open(labels_csv, encoding="utf-8"))]


    def text_classified(self, text):
        emb_text = self.model_text_classified.encode(text, convert_to_tensor=True)
        return util.cos_sim(emb_text, self.emb_cats).squeeze(0)


    def _sound_classified(self, audio_path):
        wave, _ = librosa.load(audio_path, sr=16000, mono=True)
        scores = self.model_sound_classified(tf.constant(wave, tf.float32))[0].numpy()  # [time, 521]
        # רשימת תוויות (החזקה בכל חלון)
        all_labels = []
        for i, row in enumerate(scores):
            label = self.labels[row.argmax()]
            all_labels.append(label)
        # מחשב את המנצח (הנפוץ ביותר)
        counter = Counter(all_labels)
        winner, count = counter.most_common(1)[0]
        return winner, ". ".join(all_labels)


    def audio_to_text(self, audio_path):
        return self.model_audio_to_text.transcribe(audio_path, language=None)["text"]



    def audio_classified(self, audio_path):
        most_common, text = self._sound_classified(audio_path)
        if most_common in self.cat_to_whisper:
            tr = self.audio_to_text(audio_path)
            if tr:
                text = f"{text}. {tr}"
        return self.text_classified(text)



    def audios_classified(self, gen_audio_path):
        return torch.stack([
            self.audio_classified(audio_path)
            for audio_path in gen_audio_path])