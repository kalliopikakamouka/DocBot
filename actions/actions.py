# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Any, Text, Dict, List
import arrow
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk import FormValidationAction
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict, List, Optional, Text, Dict, Any
from rasa_sdk.events import ActionExecuted
from rasa_sdk.events import ReminderScheduled
from rasa_sdk.events import UserUtteranceReverted
import datetime
import time
import requests
import pandas as pd
import json
import requests

class ActionAskMedicalSpecialty(Action):
    def name(self) -> Text:
        return "utter_ask_med_specialty"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [
            {"title": "Dermatologist", "payload": "/dermatologist"},
            {"title": "Opthalmologist", "payload": "/opthalmologist"},
            {"title": "Gynaecologist", "payload": "/gynaecologist"}
        ]
        dispatcher.utter_message(text="Got it! What type of doctor would you like to see")
        return[]

class UtterAskDate(Action):
    def name(self):
        return "utter_ask_date"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        dispatcher.utter_message(text="What day and time would you like to book?")
        return []

class UtterAskTime(Action):
    def name(self):
        return "utter_ask_time"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        dispatcher.utter_message(text="What time would you like to book?")
        return []

class ActionCheckSocialSecurity(Action):
    def name(self) -> str:
        return "action_check_ssn"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        excel_file_path = 'C:\\Users\\kakam\\OneDrive\\Υπολογιστής\\my-Rasa_Project\\docbot_user_info.csv'
        try:
            df = pd.read_csv(excel_file_path)
        except Exception as e:
            dispatcher.utter_message(response="utter_excel_read_error")
            return []
        
        user_input = tracker.get_slot('social_security_number')
        date = tracker.get_slot('date')
        time = tracker.get_slot('time')
        df['SSN'] = df['SSN'].astype(str)
        print("DataFrame Content:")
        print(df)
        print("User Input SSN:", user_input)

        matching_rows = df[df['SSN'].str.strip() == user_input.strip()]
        print("Matching Rows:")
        print(matching_rows)

        if not matching_rows.empty:
            user_name = matching_rows.iloc[0]['Name']
            appointment_info = f"{date} at {time}"
            df.loc[df['SSN'] == user_input, 'Appointment'] = appointment_info
            df.to_csv(excel_file_path, index=False)

            dispatcher.utter_message(text=f"Thank you {user_name} 😀 Your appointment is confirmed for {date} at {time} 🎉")
        else:
            dispatcher.utter_message(text="Social security number not found. Please contact 800900100")
        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_default")
        return [UserUtteranceReverted()]

class ActionQueryHeartApi(Action):
    def name(self) -> Text:
        return "action_query_heart_api"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        selected = requests.get("https://health.gov/myhealthfinder/api/v3/topicsearch.json?lang=en&keyword=heart")
        s_data = json.loads(selected.text)
        dispatcher.utter_message(text=s_data['Result']['Resources']['Resource'][0]['AccessibleVersion'])
        return[]

class ActionQueryFolicAcidApi(Action):
    def name(self) -> Text:
        return "action_query_folic_acid_api"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        selected = requests.get("https://health.gov/myhealthfinder/api/v3/topicsearch.json?lang=en&keyword=folic")
        s_data = json.loads(selected.text)
        dispatcher.utter_message(text=s_data['Result']['Resources']['Resource'][0]['AccessibleVersion'])
        return[]

class ActionQueryFallingApi(Action):
    def name(self) -> Text:
        return "action_query_falling_api"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        selected = requests.get("https://health.gov/myhealthfinder/api/v3/topicsearch.json?lang=en&keyword=falling")
        s_data = json.loads(selected.text)
        dispatcher.utter_message(text=s_data['Result']['Resources']['Resource'][0]['AccessibleVersion'])
        return[]
