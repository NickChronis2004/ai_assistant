import psutil
import GPUtil
from tabulate import tabulate
import pyttsx3
import speech_recognition as sr

# Initialize the text-to-speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
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

def get_system_info():
    cpu_info = {
        "Physical cores": psutil.cpu_count(logical=False),
        "Total cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{psutil.cpu_freq().max:.2f}Mhz",
        "Current Frequency": f"{psutil.cpu_freq().current:.2f}Mhz",
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%"
    }
    
    svmem = psutil.virtual_memory()
    memory_info = {
        "Total": f"{svmem.total / (1024 ** 3):.2f}GB",
        "Available": f"{svmem.available / (1024 ** 3):.2f}GB",
        "Used": f"{svmem.used / (1024 ** 3):.2f}GB",
        "Percentage": f"{svmem.percent}%"
    }
    
    partitions = psutil.disk_partitions()
    disk_info = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append({
            "Device": partition.device,
            "Mountpoint": partition.mountpoint,
            "File System Type": partition.fstype,
            "Total Size": f"{usage.total / (1024 ** 3):.2f}GB",
            "Used": f"{usage.used / (1024 ** 3):.2f}GB",
            "Free": f"{usage.free / (1024 ** 3):.2f}GB",
            "Percentage": f"{usage.percent}%"
        })
    
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            "GPU": gpu.name,
            "Load": f"{gpu.load * 100}%",
            "Free Memory": f"{gpu.memoryFree}MB",
            "Used Memory": f"{gpu.memoryUsed}MB",
            "Total Memory": f"{gpu.memoryTotal}MB",
            "Temperature": f"{gpu.temperature} °C",
            "Driver Version": gpu.driver
        })
    
    return cpu_info, memory_info, disk_info, gpu_info

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        processes.append(proc.info)
    return processes

def display_system_info():
    cpu_info, memory_info, disk_info, gpu_info = get_system_info()
    
    speak("CPU Info:")
    for key, value in cpu_info.items():
        speak(f"{key}: {value}")
    
    speak("\nMemory Info:")
    for key, value in memory_info.items():
        speak(f"{key}: {value}")
    
    speak("\nDisk Info:")
    speak(tabulate(disk_info, headers="keys"))
    
    speak("\nGPU Info:")
    speak(tabulate(gpu_info, headers="keys"))

def display_running_processes():
    processes = get_running_processes()
    speak(tabulate(processes, headers="keys"))

def pc_report():
    speak("Would you prefer to see a component report or a stats report?")
    choice = listen()
    if choice.lower() == 'first one':
        display_system_info()
    elif choice.lower() == 'second one':
        display_running_processes()
    else:
        speak("Sorry, I didn't understand your choice. Please try again.")
