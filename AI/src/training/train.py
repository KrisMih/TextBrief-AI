from pathlib import Path
import torch
import pandas as pd
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from data.preprocessing import build_vocabulary
from data.dataset import TextSummaryDataset
from model.summarizer import TextSummarizer


def main():
    csv_file = "data/raw/training.csv"

    # Load the training data and build the vocabulary.
    data = pd.read_csv(csv_file)
    vocabulary = build_vocabulary(data["sentence"])

    # Prepare the dataset and batches.
    dataset = TextSummaryDataset(
        csv_file=csv_file,
        vocabulary=vocabulary,
        max_length=10
    )

    dataloader = DataLoader(
        dataset,
        batch_size=2,
        shuffle=True
    )

    # Create the model, loss function, and optimizer.
    model = TextSummarizer(
        vocab_size=len(vocabulary),
        embedding_dim=16,
        padding_idx=0
    )

    criterion = nn.BCEWithLogitsLoss()  #Define how we measure prediction errors.
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    # Train on the entire dataset for 30 epochs.
    model.train()

    for epoch in range(30):
        total_loss = 0.0
        total_samples = 0

        for sentence_batch, label_batch in dataloader:
            optimizer.zero_grad()  #Clear gradients from the previous step.

            logits = model(sentence_batch)
            loss = criterion(logits, label_batch) #Calculate the loss for the current batch.

            loss.backward()  #Compute gradients.
            optimizer.step()  #Update the trainable parameters, using the computed gradients from 'loss.backward'.

            total_loss += loss.item() * label_batch.size(0) #0 because we want the first dimension([0, 1, 2] - as in shape).
            total_samples += label_batch.size(0) 

        average_loss = total_loss / total_samples
        print(f"Epoch {epoch + 1}: Loss = {average_loss:.4f}")

    # Save the trained weights and the information needed to rebuild the model.
    output_dir = Path("artifacts")
    output_dir.mkdir(exist_ok=True)

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "vocabulary": vocabulary,
            "embedding_dim": 16,
            "max_length": 10,
            "padding_idx": 0,
        },
        output_dir / "textbrief_model.pt"
    )

    print("Model saved to artifacts/textbrief_model.pt")

if __name__ == "__main__":
    main()

#BCEWithLogitsLoss compares the raw logits with the true labels (0 or 1) and computes the average loss for the batch.
#loss.item() converts the single-value loss tensor into a Python number so we can print it.
#The loss measures how well the predicted logits match the true labels; it is not an accuracy percentage.
#backward() computes gradients, but an optimizer is needed to actually update the model's weights.
#Gradients are stored in each parameter's .grad; backward() does not update the weights.
#1 'epoch()' - 1 iteration throughout all training batches.
#loss.item() gets a value from a tensor, with one number and turns it into a normal python number.
#'criterion = nn.BCEWithLogitsLoss()' sets up the function that calculates the loss and 'loss = criterion(logits, label_batch)' uses the defined function and calculates the current batch's loss.