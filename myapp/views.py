from django.http import JsonResponse
import speech_recognition as sr
from datetime import datetime, timedelta
import re
import spacy
import dateparser
import datefinder

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")

def process_speech(request):
    if request.method == 'POST':
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Please speak something...")
            recognizer.adjust_for_ambient_noise(source, duration=2)  # Adjust for ambient noise over 2 seconds
            
            try:
                # Listen with extended phrase time limit
                audio_data = recognizer.listen(source, phrase_time_limit=10)  # Listen up to 10 seconds in one phrase
                text = recognizer.recognize_google(audio_data)  # Recognize the speech
                print("You said:", text)
                
                # Parse text for form fields
                form_data = parse_speech_to_form_data(text)
                return JsonResponse(form_data)
            
            except sr.UnknownValueError:
                return JsonResponse({"error": "Could not understand the audio."}, status=400)
            except sr.RequestError:
                return JsonResponse({"error": "Request error with the speech recognition service."}, status=500)

# Parsing function for demonstration
# Load spaCy's English language model
# Load spaCy's English language model


def parse_speech_to_form_data(speech_text):
    # Initialize form data dictionary with defaults
    data = {
        "tripType": "roundTrip" if "round trip" in speech_text.lower() else "oneWay",
        "from": "",
        "to": "",
        "departureDate": "",
        "returnDate": "",
        "passengers": "1",
        "class": "economy"
    }

    # Convert speech text to lowercase and parse with spaCy
    doc = nlp(speech_text.lower())

    # Initialize placeholders for locations and dates
    locations = []
    dates = []

    # Extract locations explicitly using regex (for "from [location] to [location]")
    location_match = re.search(r"from\s+(\w+)\s+to\s+(\w+)", speech_text, re.IGNORECASE)
    if location_match:
        data["from"] = location_match.group(1).title()
        data["to"] = location_match.group(2).title()
    
    # Date parsing using spaCy entities and dateparser
    # Parse dates with spaCy and regex
     # Use datefinder to find dates in the text
    matches = list(datefinder.find_dates(speech_text))
    
    # Assign found dates to departure and return fields
    if matches:
        data["departureDate"] = matches[0].strftime("%Y-%m-%d")
        if len(matches) > 1:
            data["returnDate"] = matches[1].strftime("%Y-%m-%d")



    # Detect passenger count using regex
    passenger_match = re.search(r"(\d+)\s*passenger", speech_text)
    if passenger_match:
        data["passengers"] = passenger_match.group(1)

    # Detect travel class
    if "first class" in speech_text:
        data["class"] = "first"
    elif "business class" in speech_text:
        data["class"] = "business"
    elif "economy class" in speech_text:
        data["class"] = "economy"

    # Print parsed data for debugging
    print("Parsed data:", data)
    return data
   
   

from django.shortcuts import render

def airline_form(request):
    return render(request, 'myapp/index.html')

