from datetime import datetime
import os
import sqlite3
from tabulate import tabulate


def main():
    initial_setup()
    get_action()
    

# Function Definitions

def change_diaper():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    excre = False
    excrement = input('\"Pee\", \"poop\", \"shart\", or small poop \"nugget\"?\n')
    if excrement.strip().lower() in ["poop", "shart", "nugget"]:
        excre = True
        color = input('Color?\n')
        consistency = input('Consistency?\n')
    while True:
        rash_input = input('Any noticeable rash? Input severity 0-10, 10 being the worst\n')
        try:
            rash = float(rash_input)
            if rash >= 0 and rash <= 10:
                break
            else:
                print('Please enter value between 0 and 10')
        except ValueError:
            print('Please enter a valid number 0-10')
    diaper_notes = input('Any notes?\n')
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO diaper (date, time, excrement, rash_level, notes) 
                        VALUES (?, ?, ?, ?, ?)""", (current_date, current_time, excrement, rash, diaper_notes))
        current_id = cursor.lastrowid
        if excre == True:
            cursor.execute("""UPDATE diaper SET color = ?, consistency = ? 
                            WHERE id = ?""", (color, consistency, current_id))
    print('')
    print(f'{excrement} diaper changed at {current_time} on {current_date}')
    print(f'{diaper_notes}\n')


def doctor():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    reg_check = True
    symptom = "none"
    while True:
        reg_check_input = input('Is this a regular checkup?\n').strip().lower()
        if reg_check_input.startswith("y"):
            break
        elif reg_check_input.startswith("n"):
            reg_check = False
            symptom = input('Reason for visit?\n')
            break
        else:
            print('Please enter yes or no\n')
            continue
    height = int(input('Baby\'s height in inches? '))
    weight = int(input('Baby\'s weight in ounces? '))
    notes = input('Any notes?\n')
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO doctor (date, time, regular_checkup, symptom, height, weight, notes) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)""", (current_date, current_time, reg_check, symptom, height, weight, notes))
    print('')
    print(f'Doctors visit logged at {current_time} {current_date}')
    print(f'Height - {height} inches')
    print(f'Weight - {weight // 16}lb {weight % 16}oz')


def end_bottle():
    now = datetime.now()
    end_time_str = now.strftime("%H:%M:%S")
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT id, start_time, date, progress
                        FROM bottle
                        WHERE progress = 'In Progress'
                        ORDER BY id DESC
                        LIMIT 1""")
        row = cursor.fetchone()
        if not row:
            print('No bottles in progress')
            return
        current_id, start_time, date, progress = row
        start_time_str = f"{date} {start_time}"
        start_time_obj = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        duration = now - start_time_obj
        minutes, seconds = divmod(duration.total_seconds(), 60)
        duration_str = f"{int(minutes):02}:{int(seconds):02}"
        bottle_notes = input('Any notes?\n')
        cursor.execute("""UPDATE bottle SET end_time = ?, duration = ?, notes = ?, progress = ?
                        WHERE id = ?""", (end_time_str, duration_str, bottle_notes, "Finished", current_id))
        conn.commit()
    print('')
    print(f'Bottle finished at {end_time_str}. Duration {duration_str}')
    print(f'Notes: {bottle_notes}\n')


def get_action():
    while True:
        print('What would you like to do?\n')
        print('1: Start a bottle')
        print('2: Finish a bottle')
        print('3: Change a diaper')
        print('4: Take a bath')
        print('5: Log doctors visit')
        print('6: Give medicine')
        print('7: Log previous medicine effects')
        print('8: View tables')
        print('0: EXIT')
        print('')
        try:
            action = int(input('Choose a number: ').strip())
        except ValueError:
            os.system('cls')
            print('')
            print('Choose a valid number\n')
            continue
        else:
            match action:
                case 1:
                    start_bottle()
                case 2:
                    end_bottle()
                case 3:
                    change_diaper()
                case 4:
                    give_bath()
                case 5:
                    doctor()
                case 6:
                    give_medicine()
                case 7:
                    update_medicine()
                case 8:
                    print('')
                    print('Bottles:')
                    view_bottles()
                    print('')
                    print('Diapers:')
                    view_diapers()
                    print('')
                case 0:
                    return
                case _:
                    print('')
                    print('Invalid input\n')
                    continue
            break


def give_bath():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    bath_notes = input('Notes?\n')
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO bath (date, time, notes) 
                        VALUES (?, ?, ?)""", (current_date, current_time, bath_notes))
    print('')
    print(f'Took bath at {current_time}')
    print(f'Notes: {bath_notes}\n')


def initial_setup():
    conn = sqlite3.connect("baby_data.db")
    with open("babytracker.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def give_medicine():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    meds = input('What are you giving baby?\n')
    dose = input('How much?\n')
    reason = input('What are the baby\'s symptoms?\n')
    notes = input('Any notes?\n')
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO medicine (date, time, medicine, dose, reason, notes) 
                        VALUES (?, ?, ?, ?, ?, ?)""", (current_date, current_time, meds, dose, reason, notes))
    print(f'Gave {dose} of {meds} at {current_time}')
    print(f'Reason: {reason}')
    print(f'Notes: {notes}')


def start_bottle():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    while True:
        bottle_contents_input = input('\"Breast milk\" or \"formula\"?\n').strip().lower()
        if bottle_contents_input.lower().startswith("b"):
            bottle_contents = "Breast Milk"
            break
        elif bottle_contents_input.lower().startswith("f"):
            bottle_contents = "Formula"
            break
        else:
            print('Select a valid option\n')
    while True:
        bottle_size_input = input('How many ounces?\n').strip()
        try:
            bottle_size = float(bottle_size_input)
            if bottle_size > 0:
                break
            else:
                print('Please enter a number greater than 0\n')
        except ValueError:
            print('Please enter a valid number\n')
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO bottle (date, start_time, ounces, contents, progress) 
                        VALUES (?, ?, ?, ?, ?)""", (current_date, current_time, bottle_size, bottle_contents, "In Progress"))
        current_id = cursor.lastrowid
    print(f'Started {bottle_size}oz bottle of {bottle_contents} at {current_time}\n')
    return


def update_medicine():
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT id, time, medicine, dose 
                        FROM medicine 
                        WHERE effectiveness IS NULL
                        ORDER BY id DESC
                        LIMIT 1""")
        row = cursor.fetchone()
        if not row:
            print('No medicine needs updating')
            return
        entry_id, time, meds, dose = row
        print(f'Gave {dose} of {meds} at {time}')
        effect = input('How well did it work?\n')
        final_notes = input('Any final notes?\n')
        cursor.execute("""UPDATE medicine 
                        SET effectiveness = ?, final_notes = ? 
                        WHERE id = ?""", (effect, final_notes, entry_id))
        conn.commit()
        print(f'Added efficacy and notes')


def view_bottles():
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bottle")
        column_names = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        print(tabulate(rows, headers = column_names, tablefmt = "grid"))


def view_diapers():
    with sqlite3.connect("baby_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM diaper")
        column_names = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        print(tabulate(rows, headers = column_names, tablefmt = "grid"))



if __name__=="__main__":
    main()