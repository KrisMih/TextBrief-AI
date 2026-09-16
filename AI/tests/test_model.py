import pandas as pd
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim

from data.preprocessing import build_vocabulary
from data.dataset import TextSummaryDataset
from model.summarizer import TextSummarizer


csv_file = "data/raw/training.csv"

#Read the training data.
data = pd.read_csv(csv_file)

#Build the vocabulary from the training sentences.
vocabulary = build_vocabulary(data["sentence"])

#Create the dataset.
dataset = TextSummaryDataset(
    csv_file=csv_file,
    vocabulary=vocabulary,
    max_length=10
)

#Create the DataLoader.
dataloader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True
)

#Create the model.
model = TextSummarizer(
    vocab_size=len(vocabulary),
    embedding_dim=16,
    padding_idx=0
)

optimizer = optim.Adam(model.parameters(), lr=0.01)  #Updates the model's trainable parameters.
criterion = nn.BCEWithLogitsLoss()  #Loss function for binary classification.
model.train()  #Set the model to training mode.

for epoch in range(30):
    total_loss = 0.0
    total_samples = 0

    for sentence_batch, label_batch in dataloader:
        optimizer.zero_grad()  #Clear gradients from the previous step.

        logits = model(sentence_batch)  #Predict one logit per sentence.
        loss = criterion(logits, label_batch)  #Calculate the batch loss.

        loss.backward()  #Calculate gradients.
        optimizer.step()  #Update the model's parameters.

        total_loss += loss.item() * label_batch.size(0)
        total_samples += label_batch.size(0)

    average_loss = total_loss / total_samples
    print(f"Epoch {epoch + 1}: Loss = {average_loss:.4f}")

#BCEWithLogitsLoss compares the raw logits with the true labels (0 or 1) and computes the average loss for the batch.
#loss.item() converts the single-value loss tensor into a Python number so we can print it.
#The loss measures how well the predicted logits match the true labels; it is not an accuracy percentage.
#backward() computes gradients, but an optimizer is needed to actually update the model's weights.
#Gradients are stored in each parameter's .grad; backward() does not update the weights.
#1 'epoch()' - 1 iteration throughout all training batches.