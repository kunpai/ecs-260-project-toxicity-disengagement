import onnxruntime
from transformers import AutoTokenizer
import torch
import json
import os

token = AutoTokenizer.from_pretrained('distilroberta-base')

types = ['Toxic', 'Severe_toxic', 'Obscene', 'Threat', 'Insult', 'Identity_hate']
# Get the absolute path of the current script
script_path = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the .onnx file
onnx_file_path = os.path.join(script_path, 'classifier-quantized.onnx')

inf_session = onnxruntime.InferenceSession(onnx_file_path)
input_name = inf_session.get_inputs()[0].name
output_name = inf_session.get_outputs()[0].name

def classify_sentence(sentence):
    input_ids = token(sentence)['input_ids'][:512]
    logits = inf_session.run([output_name], {input_name: [input_ids]})[0]
    logits = torch.FloatTensor(logits)
    probs = torch.sigmoid(logits)[0]
    return dict(zip(types, map(float, probs)))

def nltk_classify_sentence(sentence):
    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(sentence)

if __name__ == "__main__":
    # Example usage:
    sentence = "Even my 6 year old can do this."
    result = classify_sentence(sentence)

    print(json.dumps(result, indent=2))

