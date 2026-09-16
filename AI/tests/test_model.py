import pandas as pd
import torch.nn as nn
from torch.utils.data import DataLoader

from data.preprocessing import build_vocabulary
from data.dataset import TextSummaryDataset
from model.summarizer import TextSummarizer


csv_file = "data/raw/training.csv"

# Prepare one batch for testing.
data = pd.read_csv(csv_file)
vocabulary = build_vocabulary(data["sentence"])

dataset = TextSummaryDataset(
    csv_file=csv_file,
    vocabulary=vocabulary,
    max_length=10
)

dataloader = DataLoader(dataset, batch_size=2, shuffle=False)

# Create the model.
model = TextSummarizer(
    vocab_size=len(vocabulary),
    embedding_dim=16,
    padding_idx=0
)

sentence_batch, label_batch = next(iter(dataloader))

# Check the model's output shape.
logits = model(sentence_batch)

assert logits.shape == label_batch.shape

# Check that loss and gradients can be computed.
criterion = nn.BCEWithLogitsLoss()
loss = criterion(logits, label_batch)
loss.backward()

assert model.classifier.weight.grad is not None

print("Model test passed!")
print("Logits shape:", logits.shape)
print("Loss:", loss.item())