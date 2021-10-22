import boto3

import json

comprehend = boto3.client(service_name="comprehend", region_name="us-east-1")


def analyze(title, text):
    sentiment = comprehend.detect_sentiment(Text=title, LanguageCode="en")
    entities = comprehend.detect_entities(Text=text[:4800], LanguageCode="en")

    processed_entities = []

    for entity in entities["Entities"]:
        data = {"type": entity["Type"].lower(), "text": entity["Text"]}

        if entity["Score"] > 0.95:
            processed_entities.append(data)

    data = {
        "sentiment": sentiment["Sentiment"].lower().capitalize(),
        "score": sentiment["SentimentScore"][
            sentiment["Sentiment"].lower().capitalize()
        ],
        "entities": processed_entities,
    }

    return data


if __name__ == "__main__":
    print(analyze("It is raining today in Seattle"))
