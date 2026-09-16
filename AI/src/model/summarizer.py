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
        self.classifier = nn.Linear(embedding_dim, 1)  # Converts each sentence vector into one importance logit.
        self.padding_idx = padding_idx #Here we create an attribute 'padding_idx' in the 'TextSummarizer' object, that is initialized to 0.

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
    def forward(self, x): #IMPORTANT: 'x' is the input batch tensor containing token IDs. Its shape is [batch_size, sequence_length], for example [2, 5] means one batch with 2 samples and 5 token IDs in each sample.
        embeddings = self.embedding(x) #Passes the input token IDs through the embedding layer and gets their embedding vectors.
        mask = x != self.padding_idx #Creates a boolean mask from the input batch 'x': True for real token IDs and False for padding token IDs.
        mask = mask.unsqueeze(-1) #Adds one new dimension at the end of the mask: [batch_size, sequence_length] -> [batch_size, sequence_length, 1].
        masked_embeddings = embeddings * mask #Applies the mask to every token's embedding vector. Real token embeddings remain unchanged, while padding token embeddings become vectors filled with zeros.
        summed_embeddings = masked_embeddings.sum(1) #Sum all of the embedding vectors for a sentence into 1. 
        tokens_count = mask.sum(dim=1) #Counts the amount of real tokens in a sentence by summing them up(True = 1, False = 0).
        sentence_vectors = summed_embeddings / tokens_count.clamp(min=1) #Calculates the average embedding vector for each sentence by dividing the sum of its token embeddings by the number of real tokens. clamp(min=1) prevents division by zero.
        logits = self.classifier(sentence_vectors) #Shape: [batch_size, 1]
        logits = logits.squeeze(-1) #Shape: [batch_size]
        return logits

#Returns one averaged embedding vector per sentence, with shape [batch_size, embedding_dim].
#The 'forward()' function shows how the data 'travles' through the model. We pass the variable 'x' through the embedding layer('x' is a tensor that contains token IDs), and we return the embedding vectors of each of the input's tensor's token IDs.
#The mask is used as a filter that tells the model which token positions are real and should be taken into consideration(True), and which positions are only padding and should be ignored during training(False).

#IMPORTANT:
#'padding_idx' keeps the PAD embedding fixed at zero during training,
#while the mask tells us which positions are padding so we do not count them during pooling.

#IMPORTANT:
#Summing along dim=1 combines all token embeddings into one vector per sentence.
#Shape: [batch_size, sequence_length, embedding_dim] -> [batch_size, embedding_dim].
#Example: [2, 10, 16] -> [2, 16] means 2 sentence vectors, each containing 16 values.

#IMPORTANT:
#Tensor dimensions (axes) are indexed from 0 in Python/PyTorch.
#The shape shows the size of each axis. For example, [2, 10, 1] means
#2 samples, 10 token positions per sample, and 1 mask value per token.
#sum(dim=1) sums along the token axis, changing the shape to [2, 1] - so it technically sums up every position in the vector, even though they are 'conceptually' vectors on their own(we did this in order for the mask to be the same dimension(to be 3-dimensional as the embedding vector - not the actual dimensions!!!) as the embedding vector).

#IMPORTANT:
#Mean pooling combines all real token embeddings into one vector per sentence.
#We use the average instead of the sum to reduce the effect of sentence length.
#Padding tokens are excluded, so we divide only by the number of real tokens.

#IMPORTANT:
#The Linear layer produces one raw importance score (logit) per sentence.
#squeeze(-1) removes the last dimension: [batch_size, 1] -> [batch_size], without changing the values.
#This makes the logits' shape match the labels' shape for BCEWithLogitsLoss.