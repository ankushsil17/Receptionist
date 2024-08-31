import time
import random
import spacy
import streamlit as st


nlp = spacy.load("en_core_web_md")

emergency_db = {}
emergency_keywords = {}

def load_emergency_data(file_path):
    global emergency_db, emergency_keywords
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith("#"):  # Ignore comments and empty lines
                emergency, response, keywords = line.strip().split('|')
                emergency_db[emergency.lower()] = response
                emergency_keywords[emergency.lower()] = [keyword.strip() for keyword in keywords.split(',')]

file_path = r'C:\Users\Ankush Sil Sarma\downloads\Receptionist\emergency_db.txt'
load_emergency_data(file_path)

def lookup_emergency(emergency_description):
    time.sleep(10)
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


if 'additional_input_selected' not in st.session_state:
    st.session_state.additional_input_selected = "No"
if 'additional_info_submitted' not in st.session_state:
    st.session_state.additional_info_submitted = False

def ai_receptionist():
    st.title("Welcome to Dr. Adrin's Clinic")

    user_input = st.selectbox("Are you having an emergency or would you like to leave a message?",
                              ["Select an option", "Emergency", "Message"])

    if user_input == "Emergency":
        emergency_description = st.text_input("What is the emergency?")

        if st.button("Submit Emergency"):
            area = st.text_input("Can you tell me which area are you located right now?")
            response = lookup_emergency(emergency_description)
            eta = random.randint(5, 30)
            st.write(f"Dr. Adrin will be coming to your location immediately. Estimated time of arrival: {eta} minutes.")
            st.write(location_based_response(area))

            if response:
                if eta > 10:
                    st.write(f"I understand that you are worried that Dr. Adrin will arrive too late, meanwhile we would suggest that you start {response.lower()}.")
                else:
                    st.write("Don't worry, please follow these steps. Dr. Adrin will be with you shortly.")
            else:
                st.write(provide_comforting_response())


            st.session_state.additional_input_selected = st.selectbox("Do you need to say anything more?", ["No", "Yes"])
            if st.session_state.additional_input_selected == "Yes":
                user_additional_input = st.text_input("Please go ahead, we are listening.")
                if st.button("Submit Additional Info"):
                    st.session_state.additional_info_submitted = True
                    st.write("Don't worry, Dr. Adrin will take care of that. Thank you.")
            elif st.session_state.additional_input_selected == "No":
                st.write("Alright, take care until the doctor arrives.")

    elif user_input == "Message":
        message = st.text_area("Please leave your message for Dr. Adrin.")
        if st.button("Submit Message"):
            st.write("Thanks for the message, we will forward it to Dr. Adrin.")
            another_message = st.selectbox("Would you like to leave another message?", ["No", "Yes"])
            if another_message == "Yes":
                st.text_area("Please leave your additional message here.")

if __name__ == "__main__":
    ai_receptionist()
