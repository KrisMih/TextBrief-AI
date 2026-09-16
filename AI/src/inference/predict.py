from pathlib import Path
import torch

from data.preprocessing import tokenize, encode_sentence, pad_sequence
from model.summarizer import TextSummarizer


def main():
    checkpoint_path = Path("artifacts/textbrief_model.pt") #Load the trained model and its vocabulary.
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True) #Load the model and running it on the cpu.

    vocabulary = checkpoint["vocabulary"] #Loading the vocabulary.
    max_length = checkpoint["max_length"] #Getting the max length of the sentences.

    model = TextSummarizer( #Recreate the same model architecture used during training. The same as the one in the 'train.py' file
        vocab_size=len(vocabulary), #The size of the vocabulary is the length of the vocabulary that was loaded earlier in the code.
        embedding_dim=checkpoint["embedding_dim"], #The dimensions of the embedding layer are being loaded.
        padding_idx=checkpoint["padding_idx"] #The padding index is loaded.
    )

    model.load_state_dict(checkpoint["model_state_dict"]) #Load the model.
    model.eval()  #Switch to evaluation(prediction) mode.

    sentence = input("Enter a sentence: ").strip() #Entering the sentence.

    if not sentence: 
        print("Please enter a sentence.")
        return

    if len(tokenize(sentence)) > max_length: 
        print(f"Please enter a sentence with at most {max_length} tokens.") 
        return

    #Convert the sentence into token IDs and pad it to the expected length.
    token_ids = encode_sentence(sentence, vocabulary)
    token_ids = pad_sequence(
        token_ids,
        max_length,
        pad_id=checkpoint["padding_idx"]
    )

    #Add the batch dimension: [max_length] -> [1, max_length].
    sentence_tensor = torch.tensor(token_ids, dtype=torch.long).unsqueeze(0)

    with torch.no_grad():  #No gradients are needed for inference(we are not training the model).
        logits = model(sentence_tensor)
        probability = torch.sigmoid(logits).item()

    prediction = 1 if probability >= 0.5 else 0

    print(f"Importance probability: {probability:.3f}")
    print(f"Prediction: {prediction} ({'important' if prediction == 1 else 'not important'})")


if __name__ == "__main__":
    main()