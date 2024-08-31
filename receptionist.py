import time
import random
import spacy

nlp = spacy.load("en_core_web_md")
emergency_db = {}
emergency_keywords = {}

def load_emergency_data(file_path):
    global emergency_db, emergency_keywords
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                emergency, response, keywords = line.strip().split('|')
                emergency_db[emergency.lower()] = response
                emergency_keywords[emergency.lower()] = [keyword.strip() for keyword in keywords.split(',')]

file_path = r'C:\Users\Ankush Sil Sarma\downloads\Receptionist\emergency_db.txt'
load_emergency_data(file_path)

def lookup_emergency(emergency_description):
    print("I am checking what you should do immediately...")
    time.sleep(15)
    doc = nlp(emergency_description.lower())
    best_match = None
    best_similarity = 0
    for emergency in emergency_db.keys():
        emergency_doc = nlp(emergency)
        similarity = doc.similarity(emergency_doc)
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = emergency
    if best_similarity > 0.75:
        return emergency_db[best_match]

    return None

def repeat_last_question(last_question):
    print("I don't understand that. " + last_question)

def provide_comforting_response():
    comforting_responses = [
        "Stay calm. Help is on the way.",
        "Please remain calm. We're here to help you.",
        "Take a deep breath. The doctor is on the way.",
        "Don't panic. Assistance is coming soon."
    ]
    return random.choice(comforting_responses)

def location_based_response(area):
    location_responses = {
        "downtown": "There is a first aid center near Central Hospital in downtown.",
        "suburbs": "The nearest emergency service is at Suburb Health Clinic.",
        "northside": "You can find emergency services at Northside Medical Center.",
        "eastside": "There is an urgent care facility at Eastside Health Pavilion.",
        "westend": "Check out the Westend Emergency Room at City Hospital.",
        "southgate": "Emergency services are available at Southgate Health Clinic.",
        "midtown": "The Midtown Health Center offers emergency assistance.",
        "lakeview": "Visit the Lakeview Medical Center for urgent care.",
        "central park": "Central Park has a medical tent near the main entrance.",
        "industrial district": "Emergency services are available at Industrial District Health Center.",
        "university area": "The university hospital provides emergency care in the university area.",
        "harbor": "Emergency assistance is available at Harbor Medical Center.",
        "riverside": "Riverside Medical Clinic can help with emergency situations.",
        "highlands": "Check with Highlands Emergency Services located near the main road.",
        "village": "Village Health Clinic offers urgent medical services.",
        "town center": "Town Center has an emergency room at the local hospital."
    }
    return location_responses.get(area.lower(), "Please stay where you are, help is on the way.")


def receptionist():
    print(
        "Welcome to Dr. Adrin's clinic. Are you having an emergency or would you like to leave a message?(emergency/message)")
    user_input = input().strip().lower()
    last_question = "Are you having an emergency or would you like to leave a message?"

    while user_input not in ["emergency", "i have an emergency", "message", "leave a message"]:
        repeat_last_question(last_question)
        user_input = input().strip().lower()

    if user_input in ["emergency", "i have an emergency"]:
        print("What is the emergency?")
        emergency_description = input().strip()
        last_question = "What is the emergency?"

        print(
            "I am checking what you should do immediately, meanwhile, can you tell me which area are you located right now?")
        area = input().strip()
        last_question = "Can you tell me which area are you located right now?"

        start_time = time.time()
        response = lookup_emergency(emergency_description)
        elapsed_time = time.time() - start_time

        eta = random.randint(5, 30)
        print(f"Dr. Adrin will be coming to your location immediately. Estimated time of arrival: {eta} minutes.")
        print(location_based_response(area))

        if eta > 10:
            if elapsed_time < 15:
                time.sleep(15 - elapsed_time)
                print("Please hold just a sec.")

            if response:
                print(
                    f"I understand that you are worried that Dr. Adrin will arrive too late, meanwhile we would suggest that you start {response.lower()}.")
            else:
                print(provide_comforting_response())
        else:
            if elapsed_time < 15:
                time.sleep(15 - elapsed_time)  # Ensure the total delay is 15 seconds
                print("Please hold just a sec.")

            if response:
                print("Don't worry, please follow these steps. Dr. Adrin will be with you shortly.")
            else:
                print(provide_comforting_response())

        print("Do you need to say anything more? (yes/no)")
        additional_input = input().strip().lower()

        if additional_input in ["yes", "y"]:
            print("Please go ahead, we are listening.")
            user_additional_input = input().strip()
            print("Dr Adrin will take care of all your worries. Stay Strong. We are reaching you asap")
        else:
            print("Alright, take care until the doctor arrives.")

    elif user_input in ["message", "leave a message"]:
        while True:
            print("Please leave your message for Dr. Adrin.")
            message = input().strip()
            print(f"Thanks for the message, we will forward it to Dr. Adrin.")
            print("Would you like to leave another message? (yes/no)")
            another_message = input().strip().lower()

            if another_message not in ["yes", "y"]:
                break

    else:
        repeat_last_question(last_question)

receptionist()

