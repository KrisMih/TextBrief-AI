import pandas as pd
from data.preprocessing import build_vocabulary
from data.dataset import TextSummaryDataset
from torch.utils.data import DataLoader

csv_file = "data/raw/training.csv"

#Read the training data.
data = pd.read_csv(csv_file)

#Build the vocabulary only from the training sentences.
vocabulary = build_vocabulary(data["sentence"])

#Create the dataset.
dataset = TextSummaryDataset(
    csv_file=csv_file,
    vocabulary=vocabulary,
    max_length=10
)

print("Vocabulary:")
print(vocabulary)

print("\nDataset length:")
print(len(dataset))

print("\nFirst sample:")
print(dataset[0])

print("\nFirst sentence tensor:")
print(dataset[0][0])

print("\nFirst label:")
print(dataset[0][1])

#Testing the DataLoader.
dataloader = DataLoader(
    dataset, #Our dataset is contained in this variable.
    batch_size=2, #The dataset has 4 samples, so the DataLoader creates 2 batches with 2 samples each.
    shuffle=True #Shuffles the samples before iterating through them.
)

#A 'for' loop which prints the sentences, labels and their shape(their dimensions.)
for sentence_batch, label_batch in dataloader:
    print("Sentences:")
    print(sentence_batch)

    print("Labels:")
    print(label_batch)

    print("Sentence batch shape:", sentence_batch.shape)
    print("Label batch shape:", label_batch.shape)