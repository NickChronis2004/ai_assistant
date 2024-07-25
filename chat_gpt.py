import openai
import pyttsx3
import speech_recognition as sr
import sensetive_info

# Use the API key from the sensetive_info module
openai.api_key = sensetive_info.CHAT_GPT_API_KEY

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def chat_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant named JARVIS."},
                {"role": "user", "content": prompt}
            ]
        )
        message = response['choices'][0]['message']['content'].strip()
        return message
    except Exception as e:
        return f"An error occurred: {str(e)}"

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"You: {query}\n")
            return query
        except Exception as e:
            print(f"Could not understand your audio, please try again! {str(e)}")
            return "None"

def main():
    while True:
        print("Say something...")
        user_input = listen()
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        if user_input != "None":
            response = chat_gpt(user_input)
            print(f"Chatbot: {response}")
            speak(response)

if __name__ == "__main__":
    main()
