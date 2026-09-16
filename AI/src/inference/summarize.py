import re

from inference.predict import load_predictor, predict_probability

def select_summary(sentences, probabilities, top_k=2):
    #Select the indices of the top-k highest-scoring sentences.
    ranked_indices = sorted(
        range(len(sentences)), #Returns the indexes of the sentences.
        key=lambda i: probabilities[i], #Sorts the sentences's indexes by importance.
        reverse=True #Sorts them from biggest to smallest grade.
    )

    selected_indices = sorted(ranked_indices[:top_k]) #Gets the two sentences with highest grades. Sorts them from smallest to biggest index.

    #Preserve the original sentence order in the summary.
    return " ".join(sentences[i] for i in selected_indices) #Concatinets the sentences into one text.

def summarize_text(text, model, checkpoint, top_k=2):
    #Split the text into sentences.
    sentences = [
        sentence.strip() #Remove any training/leading whitespaces.
        for sentence in re.split(r"(?<=[.!?])\s+", text.strip()) #Split sentences by full stops, question marks, exclamation marks and etc.
        if sentence.strip() #Remove any remaining trailing/leading whitespaces.
    ]

    if not sentences: #An 'if' statement that states if the there is no text we raise a ValueError.
        raise ValueError("The text cannot be empty.") 

    #Predict an importance probability for each sentence.
    probabilities = [
        predict_probability(sentence, model, checkpoint)
        for sentence in sentences
    ]

    #Select the highest-scoring sentences in their original order.
    return select_summary(sentences, probabilities, top_k)


def main():
    model, checkpoint = load_predictor()  #Load the model only once.

    text = input("Enter a text: ").strip() #Remove any trailing/leading whitespaces.

    try:
        summary = summarize_text(text, model, checkpoint, top_k=2) #Summarize text using the function we wrote earlier in this file.
        print("\nSummary:")
        print(summary)
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()