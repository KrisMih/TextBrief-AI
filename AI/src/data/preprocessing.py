#A function that splits a sentence by whitespaces.
def tokenize(text):
    text = text.lower() #All letters become lowercase.

    tokens = text.split() #Splits the text into tokens using whitespaces.

    return tokens #Returns the list that contains all tokens.

#IMPORTANT:
#We tokenize the text because the neural network cannot work directly with words or sentences.
#Each token gets an ID from a vocabulary.
#After this, the IDs go through an embedding layer
#(a way to represent data as vectors of numbers),
#after which they become numerical vectors that the neural network can work with.

#Process:
#sentence(text) -> tokens -> token IDs -> embeddings -> numerical vectors -> neural network

#A function that builds a vocabulary by iterating through the training data's sentences.
def build_vocabulary(sentences):
    vocabulary = { #Define the vocabulary with two reserved IDs - 0 as '<PAD>', so all of the sentences are the same length for the model even if they really aren't, and 1 for '<UNK>' - when a word is new and has no ID we assign it automatically to 1 that is reserved for unknown tokens(this happens only when the vocabulary is already built!!!).
        "<PAD>": 0,
        "<UNK>": 1
    }

    for sentence in sentences: #A 'for' loop that iterates through the training data's sentences.
        tokens = tokenize(sentence) #Tokenizing the sentences via the 'tokenize(text)' function that we wrote earlier in this file.
        for token in tokens: #Iterating throughout one sentence's tokens.
            if token not in vocabulary: #If the token is not in the vocabulary it is assigned to the next available ID, that is equal to the current length of the vocabulary dictionary.
                vocabulary[token] = len(vocabulary)
    
    return vocabulary #Return the built vocabulary.

#A function that turns the sentence into a list of token IDs
def encode_sentence(sentence, vocabulary):
    tokens = tokenize(sentence) #Tokenizing the sentence via the 'tokenize(text)' function we wrote earlier in this file.
    token_ids = [] #Creating/defining an empty list that will contain the token IDs of the input sentence's tokens.
    for token in tokens: #A 'for' loop which iterates throughout the input sentence's tokens.
        if token in vocabulary: #An 'if' statement which states that if the token is in the already built vocabulary it gets the value in vocabulary on position 'token'(in the vocabulary the keys are the tokens not the IDs!!!)
            token_ids.append(vocabulary[token]) #Append = add to the back of the list!!! 
        if token not in vocabulary: #An 'if' statement which states that if the current token is not in the already built vocabulary it gets the value in the vocabulary on position '<UNK>'(in the vocabulary the keys are the tokens not the IDs!!!). The value on this position is 1, which we reserved earlier.
            token_ids.append(vocabulary["<UNK>"]) #Append = add to the back of the list.
    return token_ids #Returns the list of token_ids in the input sentence.

#A function that pads the sentence so every sentence has the same length for the model, even if they are not really the same length.
def pad_sequence(token_ids, max_length, pad_id = 0):
    difference = max_length - len(token_ids) #Calculating the difference between the permitted 'max_length' in our programme and the length of the 'token_ids' list, that contains all of our sentence's token's ids.
    if difference < 0: #If the difference is smaller than 0 it is guaranteed that the permitted 'max_length' in our programme has been passed - in result we return a text that describes the problem.
        return "An error occured - the input sentence is longer than it should be!"
    if difference > 0: #When the difference is bigger than zero, we have to pad the sentence in order to be the permitted 'max_length' so all of the sentences are the same length.
        while difference > 0: #A 'while' loop that runs as long as the difference 'max_length - len(token_ids)' isn't zero. While it runs it appends 0s('pad_id') to the back of the token_ids list.
            token_ids.append(pad_id) #Append = add to the back of the list.
            difference-=1 #Making the difference smaller, because we increased the token_ids list's length via padding(appending) one 0 to the back of this list.
    return token_ids #Return the padded 'token_ids' list.
