from googlesearch import search
import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"You: {query}\n")  # Print the user's input
            return query
        except Exception as e:
            print(f"Could not understand your audio, please try again! {str(e)}")
            return "None"

def search_google():
    query = listen()
    if query == "None":
        print("No valid input detected.")
        return

    print(f"Searching for: {query}")
    data = search(query, start=0, stop=10, tld='com', lang='en', verify_ssl=False)

    for i in data:
        print(i)

if __name__ == "__main__":
    search_google()
