# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
# import arrow
# import dateparser

# from rasa_sdk import Action, Tracker
# from rasa_sdk.events import 
# from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

from typing import Any, Text, Dict, List
import arrow
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionGreet(Action):
    def name(self):
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Hello! How can I assist you today?")
        return []

class ActionGoodbye(Action):
    def name(self):
        return "action_goodbye"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Goodbye! Have a great day!")
        return []

class ActionBotChallenge(Action):
    def name(self):
        return "action_bot_challenge"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("I am a bot. How can I assist you?")
        return []

class ActionAskForSocialSecurityNumber(Action):
    def name(self):
        return "action_ask_for_social_security_number"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Of course! I need your 10-digit social security number")
        return []

class ActionAskMedicalSpecialty(Action):
    def name(self):
        return "action_ask_med_specialty"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Got it! What type of doctor would you like to see? (e.g., dermatologist)")
        return []

class ActionSuggestOpthalmologistInfo(Action):
    def name(self):
        return "action_suggest_opthalmologist_show_info"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("There are 3 opthalmologists available. Please provide the name of the opthalmologist you want to visit.")
        return []

class ActionSuggestGynaecologistInfo(Action):
    def name(self):
        return "action_suggest_gynaecologist_show_info"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("There are 2 gynaecologists available. Please provide the name of the gynaecologist you want to visit.")
        return []

class ActionSuggestDermatologistInfo(Action):
    def name(self):
        return "action_suggest_dermatologist_show_info"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("There are 2 dermatologists available. Please provide the name of the dermatologist you want to visit.")
        return []

class ActionProposeDateTime(Action):
    def name(self):
        return "action_propose_date_time"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Great! Please choose a date and a time and complete the form: https://calendar.app.google/whroAPdvM8vGddkWA")
        return []

class ActionConfirmBooking(Action):
    def name(self):
        return "action_confirm_booking"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Your appointment is confirmed. Is there anything else I can help you with?")
        return []

class ActionCloseConversation(Action):
    def name(self):
        return "action_close_conversation"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("No problem. Let me know if you change your mind. Goodbye!")
        return []

# class ActionCancelAppointment(Action):
#     def name(self):
#         return "utter_ask_name_for_cancellation"

#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message("Absolutely! Please provide me with your full name as seen on your ID card in CAPITAL letters")
#         return []

class ActionVerifyCancellation(Action):
    def name(self):
        return "utter_verify_cancellation"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Your appointment on 15/11/23 with Dr. Sekos has been cancelled. Is there anything else I can do for you?")
        return []

class ActionGiveAddressInfo(Action):
    def name(self):
        return "utter_give_address_info"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("The clinic's address is Praksitelous 34, Syntagma, Attiki, Athens")
        return[]

class ActionGiveTelNumberInfo(Action):
    def name(self):
        return "utter_give_tel_number_info"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("The clinic's number is 12345678910. You can call Mon-Fri 09:30-12:00")
        return []

class ActionGiveOfficeHoursInfo(Action):
    def name(self):
        return "utter_give_officehours_info"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("The clinic is open Mon-Fri 08:30-17:00")
        return []

# class ActionGiveEmergencyNumber(Action):
#     def name(self):
#         return "utter_give_emergency_number"

#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message("In case of an emergency please call 210987654372937")
#         return []

# class ActionCancelAppointment(Action):
#     def name(self):
#         return "utter_ask_ssn_cancellation"
    
#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message("Absolutely! I need your 10-digit social security number")
#         return[]

# class ActionConfirmCancellation(Action):
#     def name(self):
#         return "utter_verify_cancellation"
    
#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message("Your appointment on 15/11/23 with Dr. Sekos has been cancelled. Is there anything else I can do for you?")
#         return[]
    
# Define actions to handle the entities, if needed.
