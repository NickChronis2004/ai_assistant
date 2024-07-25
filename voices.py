import pyttsx3
import speech_recognition as sr

# Initialize the text-to-speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def list_voices():
    # Get available voices
    voices = engine.getProperty('voices')

    # Print available voices to choose from and play a sample phrase
    for index, voice in enumerate(voices):
        print(f"Voice {index}: {voice.name} - {voice.id}")
        engine.setProperty('voice', voice.id)
        engine.say(f"This is voice number {index}.")
        engine.runAndWait()

def set_voice(voice_index):
    try:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[int(voice_index)].id)
        engine.say("Voice has been changed.")
        engine.runAndWait()
    except (IndexError, ValueError):
        engine.say("Invalid voice ID. Please try again.")
        engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"You: {query}\n")  # Print the user's input
            return query.lower()
        except Exception as e:
            print(f"Could not understand your audio, please try again! {str(e)}")
            return "None"

def main_voice():
    while True:
        print("Say a command...")
        command = listen()
        if command == "list voices":
            list_voices()
        elif command.startswith("activate voice id"):
            try:
                voice_id = command.split()[-1]
                set_voice(voice_id)
            except (IndexError, ValueError):
                engine.say("Invalid command format. Please say 'activate voice id {ID}'.")
                engine.runAndWait()
        elif command in ["quit", "exit", "bye"]:
            engine.say("Goodbye!")
            engine.runAndWait()
            break

if __name__ == "__main__":
    main_voice()
