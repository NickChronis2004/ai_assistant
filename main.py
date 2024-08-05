import os
import pyttsx3
import speech_recognition as sr
import threading
from pc_report import pc_report
from chat_gpt import chat_gpt
from image_generation import image_generation
from vision import detect_faces, detect_emotions, detect_colors, video, reader
from real_time_info import get_weather
from spotify import search_and_play_song, get_user_name
from news import get_daily_news
from google_search import search_google
from voices import list_voices, set_voice, main_voice
from mail_report import open_webmail
import webbrowser
from notification_sms import send_sms_via_vonage, create_vonage_client, schedule_sms, main_notification
import sensetive_info
import todolist
from game_mode import start_game

# Global flag for stopping vision thread
stop_vision = threading.Event()

# Initialize the text-to-speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def help():
    speak("You can say the following commands:")
    commands = [
        "open spotify - to open Spotify",
        "face detection - to activate face detection",
        "weather report - to get the weather report",
        "emotion detection - to activate emotion detection",
        "color detection - to activate color detection",
        "video detection - to activate video detection",
        "image generation - to activate image generation",
        "shut down - to shut down the computer",
        "pc report - to give a PC report",
        "available commands: first one / second one",
        "news - to get the latest news",
        "terminate - to terminate the current function",
        "game mode - to play tic-tac-toe",
        "google search - to search for something on Google",
        "qr reader - to read QR codes",
        "voice settings - to change the voice",
        "q -to quit vision functions",
        "list voices - to list available voices",
        "activate voice id Voice_ID - to set the voice with the specified ID",
        "notifications - to send a message/notification",
        "open github - to open the GitHub repository",
        "open youtube - to open YouTube",
        "open chrome - to open Chrome",
        "email report - to open the webmail",
        "do list - to show the todo list(show-add-check-clear-exit)",
        "exit - bye - quit - to exit the program",
        "note that you can also type commands in the format /command_name"
    ]
    for command in commands:
        speak(command)

def vision_manager(vision_function):
    global stop_vision
    stop_vision.clear()
    vision_thread = threading.Thread(target=vision_function)
    vision_thread.start()
    return vision_thread

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

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

def pc_shut_down():
    speak("Are you sure you want to shut down the computer? Please say 'yes' to confirm or 'no' to cancel.")
    confirmation = listen()
    if confirmation.lower() == 'yes':
        speak("Shutting down the computer.")
        os.system('shutdown /s /t 1')
        # os.system('sudo shutdown now')  # Uncomment this line for Unix/Linux systems
    else:
        speak("Shut down canceled.")

def process_command(user_input):
    global stop_vision
    vision_thread = None
    
    if user_input in ["quit", "exit", "bye"]:
        stop_vision.set()
        if vision_thread is not None:
            vision_thread.join()
        return True

    elif user_input == "open spotify":
        speak("Welcome to Spotify. Please type the song name or say it.")
        song_name = input("Type the song name: ").strip()
        if not song_name:
            song_name = listen()
        
        if song_name != "None":
            response = search_and_play_song(song_name)
            speak(response)
        else:
            speak("Sorry, I didn't catch that. Please try again.")

    elif user_input == "face detection":
        vision_thread = vision_manager(detect_faces)

    elif user_input == "weather report":
        speak(get_weather())

    elif user_input == "emotion detection":
        vision_thread = vision_manager(detect_emotions)

    elif user_input == "color detection":
        vision_thread = vision_manager(detect_colors)
        speak("Color detection activated.")

    elif user_input == "video detection":
        vision_thread = vision_manager(video)
        speak("Video detection activated.")

    elif user_input == "image generation":
        speak("Image generation activated.")
        image_url = image_generation()
        if image_url:
            speak(f"The image has been created. You can view it here")
            webbrowser.open(image_url)

    elif user_input == "shut down":
        pc_shut_down()

    elif user_input == "pc report":
        pc_report()

    elif user_input == "terminate":
        stop_vision.set()
        if vision_thread is not None:
            vision_thread.join()
        speak("Terminating current function.")

    elif user_input == "news":
        get_daily_news()

    elif user_input == "game mode":
        speak("Game mode activated.")
        start_game() 

    elif user_input == "google search":
        speak("What would you like me to search for?")
        search_query = listen()
        if search_query != "None":
            search_google(search_query)
            speak("Here are the results of your search:")

    elif user_input == "qr reader":
        speak("QR reader activated.")
        reader()

    elif user_input == "open github":
        speak("Opening GitHub repository...")
        webbrowser.open(sensetive_info.GITHUB_LINK)

    elif user_input == "open youtube":
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com/")

    elif user_input == "open chrome":
        speak("Opening Chrome...")
        webbrowser.open("https://www.google.com/chrome/")
    
    elif user_input in ["email report", "webmail report", "mail report"]:
        speak("Here is your daily email report:")
        open_webmail()
    
    elif user_input == "notifications":
        speak("Notifications activated.")
        main_notification()

    elif user_input == "do list" or user_input == "to do list":
        speak("Here are today's tasks:")
        todolist.run()
        
    elif user_input == "help":
        help()

    elif user_input == "voice settings":
        main_voice()
    else:
        # Fall back to general chat response using chat_gpt
        response = chat_gpt(user_input)
        speak(response)
    
    return False

def main():
    global stop_vision
    vision_thread = None
    user_name = get_user_name()
    
    speak(f"Hello Boss. How can I assist you today?")
    while True:
        print("Say something or type a command...")
        user_input = input().strip()
        
        if user_input.startswith("/"):
            user_input = user_input[1:]
        else:
            user_input = listen().lower()

        if user_input != "None" and process_command(user_input):
            break

if __name__ == "__main__":
    main()
