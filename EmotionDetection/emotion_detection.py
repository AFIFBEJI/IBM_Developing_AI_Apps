"""
Import required modules to handle user request for detecting emotions.
"""
import json
import requests

def emotion_detector(text_to_analyze):
    """
    handle user request for detecting emotions.
    Input:
        text_to_analyze (str): The text input to be analyzed.

    Returns:
        dict[str, int]: A dictionary of emotion labels along with their corresponding scores.
    """
    # URL of the emotion detection analysis service
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/\
    EmotionPredict'

    # Custom header specifying the model ID for the emotion detection analysis service
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Constructing the request payload in the expected format
    raw_text = { "raw_document": { "text": text_to_analyze } }

    # Sending a POST request to the emotion detection API
    response = requests.post(
        url,
        headers = headers,
        json = raw_text,
        timeout=10
        )

    try:
        # Parsing the JSON response from the API
        formatted_response = json.loads(response.text)

        # Extracting emotions and their corresponding scores from the response
        emotions = formatted_response['emotionPredictions'][0]['emotion']

        if response.status_code == 200:
            return {
                **emotions,
                'dominant_emotion': max(emotions, key=emotions.get)
            }

        if response.status_code == 400:
            return dict.fromkeys(emotions.keys(), None)

    except requests.exceptions.RequestException:
        return None

    return None
