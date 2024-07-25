import vonage
import schedule
import time
import sensetive_info

def create_vonage_client(api_key, api_secret):
    client = vonage.Client(key=api_key, secret=api_secret)
    return client

def send_sms_via_vonage(client, message):
    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": sensetive_info.PHONE_NUMBER,  # Your recipient's phone number in international format
            "text": message,
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

def schedule_sms(send_time, message, client):
    schedule.every().day.at(send_time).do(send_sms_via_vonage, client=client, message=message)
    print(f"Scheduled SMS at {send_time} with message: {message}")

def main_notification():
    # Define the time and message
    send_time = input("enter time(HH:MM):")  # 24-hour format HH:MM
    message = input("enter message:")

    # Vonage API credentials
    api_key = sensetive_info.VONAGE_API_KEY
    api_secret = sensetive_info.VONAGE_API_SECRET

    # Create Vonage client
    client = create_vonage_client(api_key, api_secret)

    # Schedule the SMS
    schedule_sms(send_time, message, client)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main_notification()
    