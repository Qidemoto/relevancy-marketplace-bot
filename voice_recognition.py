import torch
import tempfile
import os
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

os.environ["HF_HUB_DISABLE_XET"] = "1"

MODEL_ID = "openai/whisper-large-v3"

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

print(f"[INFO] Инициализация модели Whisper на устройстве: {device}")

# Загрузка модели и процессора (однократно)
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    MODEL_ID,
    torch_dtype=torch_dtype,
    low_cpu_mem_usage=True
).to(device)

processor = AutoProcessor.from_pretrained(MODEL_ID)

asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
    return_timestamps=False,
    chunk_length_s=25,
)

generate_kwargs = {
    "num_beams": 2,
    "task": "transcribe",
    "language": "russian",
}


def transcribe_voice_ogg_to_text(ogg_bytes: bytes) -> str:
    try:
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp_ogg:
            tmp_ogg.write(ogg_bytes)
            tmp_ogg_path = tmp_ogg.name

        result = asr_pipeline(tmp_ogg_path, generate_kwargs=generate_kwargs)

        os.remove(tmp_ogg_path)

        return result.get("text", "").strip()

    except Exception as e:
        return f"[Ошибка распознавания]: {e}"
