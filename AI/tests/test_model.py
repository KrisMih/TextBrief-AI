import pandas as pd
from torch.utils.data import DataLoader

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

#Take one batch and pass it through the model.
for sentence_batch, label_batch in dataloader:
    output = model(sentence_batch)

    print("Input batch:")
    print(sentence_batch)

    print("\nInput shape:")
    print(sentence_batch.shape)

    print("\nLabels:")
    print(label_batch)

    print("\nEmbedding output:")
    print(output)

    print("\nEmbedding output shape:")
    print(output.shape)

    break