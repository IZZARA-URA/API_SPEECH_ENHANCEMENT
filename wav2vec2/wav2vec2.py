import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

processor = Wav2Vec2Processor.from_pretrained("./wav2vec2/wav2vec2-data16k-200k")
model = Wav2Vec2ForCTC.from_pretrained("./wav2vec2/wav2vec2-data16k-200k")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def speech_file_to_array_fn(batch: dict) -> dict:
    speech_array, sampling_rate = torchaudio.load(batch["path"])
    batch["speech"] = speech_array[0]
    batch["sampling_rate"] = sampling_rate
    return batch

def resample(batch: dict) -> dict:
    resampler=torchaudio.transforms.Resample(batch['sampling_rate'], 16_000)
    batch["speech"] = resampler(batch["speech"]).numpy()
    batch["sampling_rate"] = 16_000
    return batch

def prepare_dataset(batch: dict) -> dict:
    # check that all files have the correct sampling rate
    batch["input_values"] = processor(batch["speech"], sampling_rate=batch["sampling_rate"]).input_values
    return batch

def Wav2Vec2_larynx(file: str, tokenized: bool = False) -> str:
    b = {}
    b['path'] = file
    a = prepare_dataset(resample(speech_file_to_array_fn(b)))
    input_dict = processor(a["input_values"][0], return_tensors="pt", padding=True)
    logits = model(input_dict.input_values).logits
    pred_ids = torch.argmax(logits, dim=-1)[0]

    if tokenized:
        txt = processor.decode(pred_ids)
    else:
        txt = processor.decode(pred_ids).replace(' ','')
    return txt