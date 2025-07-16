from datetime import datetime
import os
import sqlite3
from tabulate import tabulate


def main():
    initial_setup()
    get_action()
    

# Function Definitions

def start_bottle():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    while True:
        bottle_contents_input = input("\"Breast milk\" or \"formula\"?\n").strip().lower()
        if bottle_contents_input.lower().startswith("b"):
            bottle_contents = "Breast Milk"
            break
        elif bottle_contents_input.lower().startswith("f"):
            bottle_contents = "Formula"
            break
        else:
            print("Select a valid option\n")
    while True:
        bottle_size_input = input("How many ounces?\n").strip()
        try:
            bottle_size = float(bottle_size_input)
            if bottle_size > 0:
                break
            else:
                print("Please enter a number greater than 0\n")
        except ValueError:
            print("Please enter a valid number\n")
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bottle (date, start_time, ounces, contents) VALUES (?, ?, ?, ?)", (current_date, current_time, bottle_size, bottle_contents))
        current_id = cursor.lastrowid
    print(f"Started {bottle_size}oz bottle of {bottle_contents} at {current_time}\n")
    return current_id, now


def end_bottle(current_id, start_time_obj):
    now = datetime.now()
    end_time_str = now.strftime("%H:%M:%S")
    duration = now - start_time_obj
    minutes, seconds = divmod(duration.total_seconds(), 60)
    duration_str = f"{int(minutes):02}:{int(seconds):02}"
    bottle_notes = input("Any notes?\n")
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE bottle SET end_time = ?, duration = ?, notes = ? WHERE id = ?", (end_time_str, duration_str, bottle_notes, current_id))
    print("")
    print(f"Bottle finished at {end_time_str}. Duration {duration_str}")
    print(f"Notes: {bottle_notes}\n")


def get_action():
    action = input("Start a \"bottle\" or change a \"diaper\"? Or \"view\" bottles?\n").strip().lower()
    if action == "bottle":
        bottle_id, start_time_obj = start_bottle()
        input("Press enter to finish feeding...\n")
        end_bottle(bottle_id, start_time_obj)
    elif action == "diaper":
        print("Coming soon!")
    elif action == "view":
        view_bottles()
    else:
        print("Invalid input")


def initial_setup():
    conn = sqlite3.connect("baby_data.db")
    with open("babytracker.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def view_bottles():
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bottle")
        column_names = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        print(tabulate(rows, headers = column_names, tablefmt = "grid"))



if __name__=="__main__":
    main()