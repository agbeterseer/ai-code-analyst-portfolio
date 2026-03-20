import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("unitary/toxic-bert")
model = AutoModelForSequenceClassification.from_pretrained("unitary/toxic-bert").to(device)

def check_toxicity(text):
    # Serialize if it's a dict or list
    if isinstance(text, (dict, list)):
        text = json.dumps(text)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        scores = torch.sigmoid(outputs.logits).cpu().numpy()
    
    toxicity_score = float(scores[0][0])  # Use first label’s score
    return toxicity_score
