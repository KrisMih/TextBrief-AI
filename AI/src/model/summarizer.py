import torch
import torch.nn as nn

class TextSummarizer(nn.Module):
    #A function that initializes the 'TextSummarizer' object.
    def __init__(self, vocab_size, embedding_dim, padding_idx=0):
        super().__init__()
        self.embedding = nn.Embedding(
            vocab_size, #The ammount of rows we are going to have. It is equal to the amount of tokens in the vocabulary('vocab_size').
            embedding_dim, #The amount of columns.
            padding_idx #The token ID used for padding. Its embedding vector is not updated during training.
        )

#Embedding is a trainable lookup table that converts token IDs into numerical vectors.
#Each row represents one token from the vocabulary.
#The number of rows is equal to vocab_size, because every token needs its own embedding vector.
#The number of columns is equal to embedding_dim, because embedding_dim defines how many numerical
#values are used to represent each token.

#Example:
#vocab_size = 5
#embedding_dim = 3

#Embedding matrix shape = [5, 3]

#row 0 -> embedding for token ID 0
#row 1 -> embedding for token ID 1
#row 2 -> embedding for token ID 2
#...

#Each row contains 3 numerical values because embedding_dim = 3.
#embedding_dim is a hyperparameter chosen by us before training.
#A larger embedding_dim allows a richer representation of each token, but also increases
#the number of trainable parameters and the computational cost.

#The values inside the embedding vectors are trainable parameters.
#They usually start with initialized values and are adjusted during training through
#backpropagation and the optimizer in order to reduce the loss.


#IMPORTANT!!!:
#Token IDs themselves do not carry mathematical meaning.
#They are only indices used to select the corresponding row from the embedding table.

#A function that describes how the data goes through the model.
    def forward(self, x):
        embeddings = self.embedding(x) #Passes the input token IDs through the embedding layer and gets their embedding vectors.
        return embeddings #Returns the embedding vectors for the tokens in the input.

#The 'forward()' function shows how the data 'travles' through the model. We pass the variable 'x' through the embedding layer('x' is a tensor that contains token IDs), and we return the embedding vectors of each of the input's tensor's token IDs.