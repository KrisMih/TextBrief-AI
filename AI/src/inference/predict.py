from pathlib import Path
import torch

from data.preprocessing import tokenize, encode_sentence, pad_sequence
from model.summarizer import TextSummarizer


def load_predictor():
    #Load the trained parameters, vocabulary, and model settings.
    checkpoint = torch.load(
        Path("artifacts/textbrief_model.pt"),
        map_location="cpu",
        weights_only=True
    )

    #Recreate the model and restore its trained parameters.
    model = TextSummarizer(
        vocab_size=len(checkpoint["vocabulary"]),
        embedding_dim=checkpoint["embedding_dim"],
        padding_idx=checkpoint["padding_idx"]
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    return model, checkpoint


def predict_probability(sentence, model, checkpoint):
    #Validate and prepare the input sentence.
    if not sentence.strip():
        raise ValueError("The sentence cannot be empty.")

    if len(tokenize(sentence)) > checkpoint["max_length"]:
        raise ValueError("The sentence exceeds the maximum token length.")

    token_ids = encode_sentence(sentence, checkpoint["vocabulary"]) #Encode the sentence changing known tokens to their related token IDs.
    token_ids = pad_sequence(
        token_ids,
        checkpoint["max_length"],
        pad_id=checkpoint["padding_idx"]
    )

    #Add a batch dimension for a single sentence.
    sentence_tensor = torch.tensor(token_ids, dtype=torch.long).unsqueeze(0)

    #Convert the model's logit into a probability.
    with torch.no_grad():
        logit = model(sentence_tensor)
        probability = torch.sigmoid(logit).item()

    return probability


def main():
    model, checkpoint = load_predictor()

    sentence = input("Enter a sentence: ").strip()

    try:
        probability = predict_probability(sentence, model, checkpoint)
    except ValueError as error:
        print(error)
        return

    prediction = 1 if probability >= 0.5 else 0

    print(f"Importance probability: {probability:.3f}")
    print(f"Prediction: {prediction} ({'important' if prediction else 'not important'})")


if __name__ == "__main__":
    main()