import pandas as pd
from data.preprocessing import build_vocabulary
from data.dataset import TextSummaryDataset

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