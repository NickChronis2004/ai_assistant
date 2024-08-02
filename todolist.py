import json
import os

list_of_todos = []

def add_todo(todo):
    list_of_todos.append(todo)
    print(f"Added {todo} to the list of todos.")

def check_todo(todo):
    if todo in list_of_todos:
        list_of_todos.remove(todo)
        print(f"Removed {todo} from the list of todos.")
    else:
        print(f"{todo} is not in the list of todos.")

def show_todos():
    if not list_of_todos:
        print("No todos to show.")
    else:
        for i, todo in enumerate(list_of_todos, start=1):
            print(f"{i}. {todo}")

def clear_todos():
    list_of_todos.clear()
    print("Todos cleared.")

def save_todos():
    with open('todos.json', 'w') as file:
        json.dump(list_of_todos, file)
    print("Todos saved.")

def load_todos():
    global list_of_todos
    try:
        with open('todos.json', 'r') as file:
            list_of_todos = json.load(file)
        print("Todos loaded.")
    except FileNotFoundError:
        print("No saved todos found.")

def main():
    load_todos()
    while True:
        print("What would you like to do? (add/show/check/clear/exit)")
        user_input = input().lower()
        if user_input == "add":
            print("What would you like to add?")
            todo = input()
            add_todo(todo)
            show_todos()
        elif user_input == "show":
            show_todos()
        elif user_input == "clear":
            clear_todos()
            os.remove("todos.json")
            print("Todos file deleted.")
        elif user_input == "check":
            print("What would you like to check?")
            todo = input()
            check_todo(todo)
        elif user_input == "exit":
            save_todos()
            print("Exiting...")
            break
        else:
            print("Invalid command. Please try again.")

def run():
    main()

if __name__ == "__main__":
    main()
