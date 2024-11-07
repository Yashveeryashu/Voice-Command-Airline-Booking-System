# from django.http import JsonResponse
# import speech_recognition as sr
# from datetime import datetime, timedelta
# import re
# import spacy
# import dateparser
# import datefinder

# # Load spaCy's English language model
# nlp = spacy.load("en_core_web_sm")

# def process_speech(request):
#     if request.method == 'POST':
#         recognizer = sr.Recognizer()
        
#         with sr.Microphone() as source:
#             print("Please speak something...")
#             recognizer.adjust_for_ambient_noise(source, duration=2)
            
#             try:
#                 audio_data = recognizer.listen(source, phrase_time_limit=10)
#                 text = recognizer.recognize_google(audio_data)
#                 print("You said:", text)
                
#                 form_data = parse_speech_to_form_data(text)
                
#                 # Speak the booking information
#                 speak_booking_info(form_data)
                
#                 return JsonResponse(form_data)
            
#             except sr.UnknownValueError:
#                 return JsonResponse({"error": "Could not understand the audio."}, status=400)
#             except sr.RequestError:
#                 return JsonResponse({"error": "Request error with the speech recognition service."}, status=500)


# # Parsing function for demonstration
# # Load spaCy's English language model
# # Load spaCy's English language model


# def parse_speech_to_form_data(speech_text):
#     # Initialize form data dictionary with defaults
#     data = {
#         "tripType": "roundTrip" if "round trip" in speech_text.lower() else "oneWay",
#         "from": "",
#         "to": "",
#         "departureDate": "",
#         "returnDate": "",
#         "passengers": "1",
#         "class": "economy"
#     }

#     # Convert speech text to lowercase and parse with spaCy
#     doc = nlp(speech_text.lower())

#     # Initialize placeholders for locations and dates
#     locations = []
#     dates = []

#     # Extract locations explicitly using regex (for "from [location] to [location]")
#     location_match = re.search(r"from\s+(\w+)\s+to\s+(\w+)", speech_text, re.IGNORECASE)
#     if location_match:
#         data["from"] = location_match.group(1).title()
#         data["to"] = location_match.group(2).title()
    
#     # Date parsing using spaCy entities and dateparser
#     # Parse dates with spaCy and regex
#      # Use datefinder to find dates in the text
#     matches = list(datefinder.find_dates(speech_text))
    
#     # Assign found dates to departure and return fields
#     if matches:
#         data["departureDate"] = matches[0].strftime("%Y-%m-%d")
#         if len(matches) > 1:
#             data["returnDate"] = matches[1].strftime("%Y-%m-%d")



#     # Detect passenger count using regex
#     passenger_match = re.search(r"(\d+)\s*passenger", speech_text)
#     if passenger_match:
#         data["passengers"] = passenger_match.group(1)

#     # Detect travel class
#     if "first class" in speech_text:
#         data["class"] = "first"
#     elif "business class" in speech_text:
#         data["class"] = "business"
#     elif "economy class" in speech_text:
#         data["class"] = "economy"

#     # Print parsed data for debugging
#     print("Parsed data:", data)
#     return data
   
# from gtts import gTTS
# import os

# def speak_booking_info(booking_info):
#     # Combine the booking information into a single string
#     text = f"You have booked a {booking_info['tripType']} from {booking_info['from']} to {booking_info['to']}."
#     text += f" Departure date is {booking_info['departureDate']}."
#     if booking_info['returnDate']:
#         text += f" Return date is {booking_info['returnDate']}."
#     text += f" You have {booking_info['passengers']} passenger(s) and your class is {booking_info['class']}."

#     # Create a gTTS object
#     tts = gTTS(text=text, lang='en')

#     # Save the speech to a file
#     tts.save("booking_info.mp3")

#     # Play the audio (this will work on most systems, but you may need to adapt this for your OS)
#     # os.system("start booking_info.mp3")  # For Windows
#     # os.system("afplay booking_info.mp3")  # For Mac
#     # os.system("mpg123 booking_info.mp3")  # For Linux


# from django.shortcuts import render

# def airline_form(request):
#     return render(request, 'myapp/index.html')



# from django.shortcuts import render, redirect
# from .models import FlightBooking
# from django.http import JsonResponse

# def submit_booking(request):
#     if request.method == 'POST':
#         trip_type = request.POST.get('tripType')
#         from_location = request.POST.get('from')
#         to_location = request.POST.get('to')
#         departure_date = request.POST.get('departureDate')
#         return_date = request.POST.get('returnDate') or None  # Handle one-way trip case
#         passengers = request.POST.get('passengers')
#         travel_class = request.POST.get('class')

#         # Save the data to the database
#         booking = FlightBooking.objects.create(
#             trip_type=trip_type,
#             from_location=from_location,
#             to_location=to_location,
#             departure_date=departure_date,
#             return_date=return_date,
#             passengers=passengers,
#             travel_class=travel_class
#         )

#         # Redirect to a success page or send a response
#         return render(request, 'myapp/booking_success.html', {'booking': booking})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)



# myapp/views.py

from django.http import JsonResponse
from datetime import datetime, timedelta
import re
import spacy
import datefinder
from django.shortcuts import render
from .models import FlightBooking

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")

def process_speech(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        field = data.get('field')
        text = data.get('text', '')
        
        if not field or not text:
            return JsonResponse({"error": "Invalid data."}, status=400)
        
        # Parse the text for the specific field
        value = parse_speech_for_field(field, text)
        
        return JsonResponse({field: value})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)

def parse_speech_for_field(field, speech_text):
    speech_text = speech_text.lower()
    value = ""
    
    if field == "tripType":
        value = "roundTrip" if "round trip" in speech_text or "return" in speech_text else "oneWay"
    
    elif field == "from":
        from_match = re.search(r"from\s+(\w+)", speech_text)
        if from_match:
            value = from_match.group(1).title()
        else:
            # If not in the format "from [location]", take the entire input as location
            value = speech_text.strip().title()
    
    elif field == "to":
        to_match = re.search(r"to\s+(\w+)", speech_text)
        if to_match:
            value = to_match.group(1).title()
        else:
            # If not in the format "to [location]", take the entire input as location
            value = speech_text.strip().title()
    
    elif field == "departureDate":
        matches = list(datefinder.find_dates(speech_text))
        if matches:
            value = matches[0].strftime("%Y-%m-%d")
        else:
            # Default to tomorrow if no date found
            value = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    elif field == "returnDate":
        matches = list(datefinder.find_dates(speech_text))
        if matches and len(matches) > 1:
            value = matches[1].strftime("%Y-%m-%d")
        elif "next friday" in speech_text:
            # Calculate next Friday
            today = datetime.now()
            days_ahead = 4 - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            value = (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        else:
            value = ""
    
    elif field == "passengers":
        passenger_match = re.search(r"(\d+)\s*passenger", speech_text)
        if passenger_match:
            value = passenger_match.group(1)
        else:
            value = "1"
    
    elif field == "class":
        if "first class" in speech_text:
            value = "first"
        elif "business class" in speech_text:
            value = "business"
        else:
            value = "economy"
    
    # Debugging: Print parsed value
    print(f"Parsed value for {field}: {value}")
    return value

def airline_form(request):
    return render(request, 'myapp/index.html')

def submit_booking(request):
    if request.method == 'POST':
        trip_type = request.POST.get('tripType')
        from_location = request.POST.get('from')
        to_location = request.POST.get('to')
        departure_date = request.POST.get('departureDate')
        return_date = request.POST.get('returnDate') or None  # Handle one-way trip case
        passengers = request.POST.get('passengers')
        travel_class = request.POST.get('class')

        # Save the data to the database
        booking = FlightBooking.objects.create(
            trip_type=trip_type,
            from_location=from_location,
            to_location=to_location,
            departure_date=departure_date,
            return_date=return_date,
            passengers=passengers,
            travel_class=travel_class
        )

        # Redirect to a success page or send a response
        return render(request, 'myapp/booking_success.html', {'booking': booking})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
