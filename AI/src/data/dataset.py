import torch
from torch.utils.data import Dataset
import pandas as pd
from data.preprocessing import encode_sentence, pad_sequence

#Custom dataset for our summarization project.
class TextSummaryDataset(Dataset):
    #A function that initializes our dataset.
    def __init__(self, csv_file, vocabulary, max_length):
        self.data = pd.read_csv(csv_file) #Creating an attribute 'data' inside of our object, which is a panda DataFrame that will get the data from a csv_file we put up as an argument in the function.
        self.vocabulary = vocabulary
        self.max_length = max_length

    #A function that returns the number of samples in the dataset.
    def __len__(self):
        return len(self.data) #Returns how many samples/rows are in the dataset.

    #A function that returns the row at position idx.
    def __getitem__(self, idx):
        row = self.data.iloc[idx] #Gets the row at position idx from the DataFrame
        sentence = row["sentence"] #Gets the feature from the sentence column.
        label = row["label"] #Gets the target from the label column.
        token_ids = encode_sentence(sentence, self.vocabulary) #Encodes the sentence so it becomes a list that contains it's token's IDs.
        token_ids = pad_sequence(token_ids, self.max_length, pad_id = 0) #Padding the sentence so every sentence is the same length, even if they really are not.
        sentence_tensor = torch.tensor(token_ids, dtype=torch.long) #Create a tensor, that contains the list 'token_ids' in a way that the neural network can (later) work with.
        label_tensor = torch.tensor(label, dtype=torch.float32) #Create a tensor, that contains the labels in a way that the neural network can (later) work with.
        return sentence_tensor, label_tensor #Returns the feature and the target for the row on position idx.