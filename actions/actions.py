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
import re
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

class ActionAskWeight(Action):
    def name(self) -> Text:
        return "utter_ask_weight_kgs"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        weight_kgs = tracker.get_slot('weight_kgs')
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        dispatcher.utter_message(text="In order to calculate your BMI, I need your weight in KG (example: 65)")
        return []
    
class ActionAskHeight(Action):
    def name(self) -> Text:
        return "utter_ask_height_cm"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        dispatcher.utter_message(text="Please provide me with your height in CM as well (example: 170)")
        return []
    
class ActionBMIResults(Action):
    def name(self) -> Text:
        return "action_BMI_results"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        weight = tracker.get_slot("weight_kgs")
        height = tracker.get_slot("height_cm")

        match = re.findall(r'\d+\.\d+|\d+', weight)
        weight_num = float(match[0]) if match else None

        match = re.findall(r'\d+', height)
        height_num = float(match[0]) if match else None

        print("Extracted: w=",weight_num," h:",height_num)

        try:
            url = f'https://www.calculateconvert.com/calculators/health/bmi.php?kgs={weight_num}&cm={height_num}'
            x = requests.get(url)
            if(x.status_code == 200):
                pattern = b"your BMI is (\d+\.\d+)"
                match = re.search(pattern, x.content)
                if match:
                    bmi_value = float(match.group(1))
                    pattern = b"style=\"color:yellow;\">(\w+)"
                    match = re.search(pattern, x.content)
                    if match:
                        status = match.group(1).decode('utf-8')
                    else:
                        status = "Could not determine"
                    dispatcher.utter_message(text=f"Your BMI based on your information is: {bmi_value}⏲️\nYour BMI scale status is: {status}")
                else:
                    dispatcher.utter_message(text=f"Error calculating, check your spelling")
            else:
                dispatcher.utter_message(text=f"Error fetching the data, try again later")
        except:
            dispatcher.utter_message(text=f"Server is unfortunatelly unavailable at the moment.")
        return []


# class SSNForm(FormValidationAction):
#     def name(self) -> str:
#         return "validate_ssn_form"

#     def validate_social_security_number(
#         self,
#         value: Text,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         if len(value) == 11 and value.isdigit():
#             return {"social_security_number": value}
#         else:
#             dispatcher.utter_message("Hmm, this doesn't look right. Please provide a valid 11-digit social security number.")
#             return {"social_security_number": None}

#     # def validate(self, dispatcher: CollectingDispatcher,
#     #              tracker: Tracker,
#     #              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: