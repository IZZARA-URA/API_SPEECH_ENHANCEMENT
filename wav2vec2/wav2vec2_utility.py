import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

processor = Wav2Vec2Processor.from_pretrained("./wav2vec2/wav2vec2-data16k-200k")
model = Wav2Vec2ForCTC.from_pretrained("./wav2vec2/wav2vec2-data16k-200k")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')