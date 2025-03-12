# DocBot 🩺💊

This is my Project for the course M913 ("Conversational Systems & Voice Agents / Διαλογικά Συστήματα και Φωνητικοί Βοηθοί"). Using RASA, I had the chance to create my own, personalized chatbot called "**DocBot**". DocBot can: </br>

1. Book appointments with the use of slots and forms making the chatbot more dynamic.
2. Connect with an Excel file, which works as a dummy database
3. Give links to various health topics based on an API
4. Calculate the BMI based on the users' inputs (height + weight), which is connected to another API address
5. Reply to chitchat and FAQs
6. Handle out-of-scope inputs
7. Make use of newly-integrated policies

### Conversational flow - Happy path

The main point of the created chatbot is to book doctor's appointments, which are inplemented with the use of forms, that are considered necessary for the completion of the task. We can check a simplified conversational flow, which follows a happy path:

👱🏻‍♀️ --> user greets <br />
🤖 --> bot greets back and asks the user how it can help them <br />
👱🏻‍♀️ --> user wants to book an appointment <br />
🤖 --> bot suggests 3 medical specialties <br />
👱🏻‍♀️ --> the user chooses between these options: dermatologist, opthalmologist, gynaecologist <br />
🤖 --> bot suggest available doctors based on the chosen medical field <br />
👱🏻‍♀️ --> user chooses a doctor <br />
🤖 --> bot tells the user to choose a date and a time (use of forms) <br />
👱🏻‍♀️ --> user types their preferred date and time <br />
🤖 --> bot asks for the user's Social Security Number (ssn) (use of form) <br />
👱🏻‍♀️ --> user types their SSN <br />
🤖 --> bot checks the existence of the given input in the database (Excel). If the number exists the appointment is set, if not, the user is asked to call a telephone number. <br />

I would like to point out two features, which in my opinion help DocBot stand out.

a. **The use of buttons**:

After requesting to book an appointment, users are asked to make two main choices. At first, they have to choose the type of medical specialty they wish to visit. After they click on the option they prefer, they choose the doctor they would like to book an appointment with, based on the chosen specialty. The reason why I proceeded with the use of buttons regards the following:<br />
    1. Limiting the options. If the user doesn’t know which and how many medical specialties there are, they can see their options straightforward<br />
    2. Robustness.<br />

b. **The SSN number**:

It is well known that clinics need a database, which consists of every patient’s information. For that reason, I created my own dummy database, which contains the information of a few fake patients. I proceeded with this implementation, because I wanted to take the experience further and create a realistic booking process. 
Instead of the typical name-surname-number-email request, I proceeded to create an Excel file, which is considered to be the "clinic's database", consisting of various information about its patients. The columns I created include information about the following topics: SSN number (it's unique for every patient), Name, Surname, Email and Appointment. Here's how it works: When the user gives their SSN number, the bot runs a custom action called 'action_check_ssn'. At first, this custom action checks the existence of the given ssn number in the Excel file. If the number exists, the bot implements two different activities:<br />
    1. It makes use of the {date} and {time} slots given by the user previously in the conversation and adds the chosen appointment date and time in the column             "Appointment". The bot manages to locate the row that the SSN is set in the Excel file and adds the date and time to the corresponding cell.<br />
    2. After adding the chosen date and time, the bot 'sees' whom this SSN number belongs to in the list and replies kindly with the following message: "Thank you, {name}!, your appointment on {date} at {time} is confirmed", making the approach even friendlier. If the user gives an SSN number, which is not part of the Excel file or an SSN number which is invalid, they are asked to call the clinic for further assistance.<br />

### Conversational Flow - Sad path
Life could be a little better and easier for us if users followed an absolutely ideal conversation. However, knowing that this can almost never be the case, being prepared for a scenario as such is considered necessary! For that reason, I implemented the FAQ/chitchat capabilities. It is impossible to predict every single thing that a user can say. Hence, I created a few chitchat and FAQ questions with corresponding answers, which can help DocBot to not fail the conversation. 

### Handling interruption during slot filling 
In addittion to the sad path scenario, I would like to point out the cases, where the conversation is being interrupted during slot filling. This case is important to be handled gracefully and that the bot manages to bring the user back to the conversation. Here are some examples:<br />

_Chitchat scenario_:<br />
🤖 --> In order to proceed with booking, I need your 11-digit Social Security Number<br />
👱🏻‍♀️ --> What is your age?<br />
🤖 --> Age is just a number<br />
🤖 --> In order to proceed with booking, I need your 11-digit Social Security Number<br />

_FAQ scenario_:<br />
🤖 --> In order to proceed with booking, I need your 11-digit Social Security Number<br />
👱🏻‍♀️ --> What are the opening hours of the clinic?<br />
🤖 --> The clinic is open Monday - Friday 08:30 - 17:00 <br />
🤖 --> In order to proceed with booking, I need your 11-digit Social Security Number<br />

Let's not forget the out-of-scope cases. As mentioned earlier, users can sometimes ask questions, which are completely random. Afterall chatting with a chatbot can be quite fun and users want to check its knowledge. However, this might lead to the failure of the conversation. DocBot has been designed to handle such cases. Here's an example:<br />

_Out-of-scope scenario_:<br />
🤖 --> What day and time would you like to book?<br />
👱🏻‍♀️ --> Who is the President of USA?<br />
🤖 --> Sorry, I didn't catch that, can you please rephrase? <br />
👱🏻‍♀️ --> I want an appointment on Monday at 12:30 <br />
🤖 --> In order to proceed with booking, I need your 11-digit Social Security Number<br />


### API Integration
### API: Health Blog
DocBot has been connected to two different API addresses and can implement two different actions as well.<br />
The first address I chose to conect to DocBot is the following one: **https://health.gov/our-work/national-health-initiatives/health-literacy/consumer-health-content/myhealthfinder** <br />
Considering that this health blog contains various subjects about health, I decided on focusing on three which are related to the following topics:<br />
        1. Heart<br />
        2. Folic Acid<br />
        3. Falling<br />
Users can ask DocBot about these subjects, and based on the keyword they have provided, they will get the corresponding link for the article they are interested in reading<br />

### API: BMI Calculator
The second API address connected to DocBot is a BMI calculator (**https://www.calculateconvert.com/calculators/health/bmi.php?kgs=%7Bweight_num%7D&cm=%7Bheight_num%7D**). Users are asked to type in their height in cm and their weight in kg and the calculator will give them the following information: <br />
    1. The BMI based on their input<br />
    2. Their status (underweight/normal/overweight)<br />
Considering that I wanted to make use of an open-source API address, I couldn't find one, which could be more accurate. In my opinion, the parameters of sex (male/female) and health condition, also play a role and should be considered for an accurate BMI calculation.<br />

### Policies

Regarding the policies that I activated and implemented for the functionality of DocBot, I can conclude the following:<br />
- MemoizationPolicy<br />
- RulePolicy<br />
- UnexpecTEDIntentPolicy<br />
- TEDPolicy<br />

The MemorizationPolicy efficiently manages predictable dialogue paths but struggles with novel inputs due to its reliance on historical patterns. In contrast, the RulePolicy ensures consistency in specific intents but lacks adaptability for unexpected inputs, requiring explicit rule definition. The UnexpecTEDIntentPolicy addresses uncertainty effectively but demands sufficient training data for optimal performance. Similarly, the TEDPolicy captures nuanced similarities but requires substantial computational resources and training data to operate effectively.

### Future work 

DocBot can be implemented in clinics and personal doctors’ offices, making it suitable for patients who struggle with communicating (e.g people who are deaf), or people who don’t want to waste time waiting for the receptionist to pick up the phone. However, it is important to note, that DocBot could become even better. Here are some features, that I would want to upgrade:<br />

- Connect DocBot with an actual calendar<br />
- Connect DocBot to more API addresses, and thus offer more services<br />
- Add more medical specialties<br />
- Add a cancelation feature, which is absolutely necessary
