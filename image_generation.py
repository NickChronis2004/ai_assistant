import openai
import speech_recognition as sr
import sensetive_info

openai.api_key = sensetive_info.CHAT_GPT_API_KEY

def get_voice_input():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    with microphone as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        voice_input = recognizer.recognize_google(audio)
        print(f"You said: {voice_input}")
        return voice_input
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

def image_generation():
    prompt = get_voice_input()
    if prompt:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        print(f"Image URL: {image_url}")
        return image_url

if __name__ == "__main__":
    image_generation()
