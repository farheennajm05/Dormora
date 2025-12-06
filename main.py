# This is the main code for DORMORA- Smart Hostel Management Tool.

import csv
import os
from datetime import datetime   

DATA = "data"


def fullpath(name):
    return os.path.join(DATA, name)

def read_rows(filename):
    rows = []
    try:
        with open(fullpath(filename), newline="") as f:
            reader = csv.reader(f)
            for r in reader:
                if len(r) > 0:
                    rows.append(r)
    except:
        pass
    return rows


# water and washroom issue
def water_and_washroom_issue():
    print("\n Water & Washroom Issue Detector ")
    print("1. Low water pressure")
    print("2. No water in tank")
    print("3. Washroom not cleaned")
    print("4. Bad smell")
    print("5. Water leakage")
    print("6. Other issue")
    print("7. Go back")

    choice = input("Select an option (1-7): ").strip()
    if choice == "1":
        print("Your Complaint: Low water pressure has been noted.")
        save_complaint("Anonymous", "Low water pressure")
    elif choice == "2":
        print("Your Complaint: No water in tank has been noted.")
        save_complaint("Anonymous", "No water in tank")
    elif choice == "3":
        print("Your Complaint: Washroom cleaning needed.")
        save_complaint("Anonymous", "Washroom not cleaned")
    elif choice == "4":
        print("Your Complaint: Bad smell reported.")
        save_complaint("Anonymous", "Bad smell in washroom")
    elif choice == "5":
        print("Your Complaint: Water leakage reported.")
        save_complaint("Anonymous", "Water leakage")
    elif choice == "6":
        other = input("Please describe the problem: ").strip()
        if other:
            print("Your Complaint has been noted:", other)
            save_complaint("Anonymous", other)
        else:
            print("No description is entered.Please do enter valid description")
    elif choice == "7":
        print("Going back to main menu...")
    else:
        print("Invalid choice.")


# to save complaint
def save_complaint(name, issue):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")  
    try:
        with open(fullpath("complaints.csv"), "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, issue, timestamp])       
    except:
        print("Warning: could not save complaint. Check data folder.")


# matching roomates
def add_student_profile():
    print("\n Add / Update Your Roommate Profile ")
    name = input("Your Full name: ").strip()
    sleep = input("Sleep time (early/late): ").strip().lower()
    study = input("Study time (morning/night): ").strip().lower()
    noise = input("Noise tolerance (low/high): ").strip().lower()
    clean = input("Cleanliness (low/medium/high): ").strip().lower()

    try:
        with open(fullpath("students_preferences.csv"), "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, sleep, study, noise, clean])
        print("Profile saved.")
    except:
        print("Error: Could not save profile.")


def view_matches():
    print("\n View Saved Profiles & Find Matches ")
    rows = read_rows("students_preferences.csv")
    if len(rows) == 0:
        print("No profiles saved yet.")
        return

    for i, r in enumerate(rows):
        if len(r) >= 5:
            print(f"{i+1}. {r[0]} | sleep:{r[1]} study:{r[2]} noise:{r[3]} clean:{r[4]}")

    print("\nSuggested matches (score ≥ 3):")
    found = False
    for a in range(len(rows)):
        for b in range(a+1, len(rows)):
            r1, r2 = rows[a], rows[b]
            if len(r1) >= 5 and len(r2) >= 5:
                score = sum([r1[i] == r2[i] for i in range(1, 5)])
                if score >= 3:
                    print(f" - {r1[0]} & {r2[0]} (score {score}/4)")
                    found = True

    if not found:
        print("No strong matches found yet. Add more profiles.")


#3. viewing complaints
def complaint_viewer():
    print("\n Complaints ")
    rows = read_rows("complaints.csv")
    if len(rows) == 0:
        print("No complaints found.")
        return

    for i, r in enumerate(rows):
        if len(r) == 3:
            print(f"{i+1}. {r[0]} - {r[1]}  (Filed on: {r[2]})")   # <-- Shows date
        else:
            print(f"{i+1}. {r}")


# mess menu and attendance
def mess_analyzer():
    print("\n Mess Menu & Attendance ")
    print("1. Add today's mess data")
    print("2. View attendance trends")
    print("3. View dish popularity")
    print("4. Go back")
    choice = input("Choose: ").strip()

    path = "mess_data.csv"

    if choice == "1":
        day = input("Day: ").strip()
        dish = input("Main dish: ").strip()
        try:
            ate = int(input("Number of students who ate: ").strip())
            skipped = int(input("Number of students who skipped: ").strip())
        except:
            print("Invalid answer.")
            return
        try:
            with open(fullpath(path), "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([day, dish, ate, skipped])
            print("Mess data saved.")
        except:
            print("Error.")

    elif choice == "2":
        rows = read_rows(path)
        if len(rows) == 0:
            print("No mess data has been recorded yet.")
            return

        for r in rows:
            if len(r) >= 4:
                print(f"{r[0]}: {r[3]} skipped")

    elif choice == "3":
        rows = read_rows(path)
        if len(rows) == 0:
            print("No mess data yet.")
            return

        popularity = {}
        for r in rows:
            if len(r) >= 3:
                dish = r[1]
                ate = int(r[2])
                popularity[dish] = popularity.get(dish, 0) + ate

        print("\nDish popularity:")
        for d, val in popularity.items():
            print(f"{d} -> {val}")

    else:
        print("Going back...")


# 5.menu management
def menu_management():
    print("\n Menu Management ")
    print("1. View today's menu")
    print("2. Update today's menu")
    print("3. Report a food issue")
    print("4. Go back")
    ch = input("Choose: ").strip()

    path = "menu.csv"

    if ch == "1":
        rows = read_rows(path)
        if len(rows) == 0:
            print("Menu not set yet.")
            return
        for row in rows:
            print(f"{row[0]}: {row[1]}")

    elif ch == "2":
        b = input("Breakfast: ").strip()
        l = input("Lunch: ").strip()
        d = input("Dinner: ").strip()

        try:
            with open(fullpath(path), "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Breakfast", b])
                writer.writerow(["Lunch", l])
                writer.writerow(["Dinner", d])
            print("Menu has been updated.")
        except:
            print("Error updating menu.")

    elif ch == "3":
        issue = input("Describe food issue: ").strip()
        if issue:
            save_complaint("Food Issue", issue)
            print("Issue has been noted.")
        else:
            print("No description entered.")

    else:
        print("Going back...")


# smart alerts
def smart_alerts():
    print("\n Smart Alerts ")
    print("Cleaning schedule: Daily at 3:00 PM")

    rows = read_rows("water_usage.csv")
    high_usage = False
    for r in rows:
        if len(r) >= 2:
            try:
                if float(r[1]) > 120:
                    high_usage = True
            except:
                pass

    if high_usage:
        print("ALERT: High water usage recorded. Possible leak.")

    mrows = read_rows("mess_data.csv")
    for row in mrows:
        if len(row) >= 4:
            try:
                if int(row[3]) > 50:
                    print(f"ALERT: High skip count on {row[0]} - review menu.")
            except:
                pass


# main menu
def main():
    if not os.path.exists(DATA):
        os.mkdir(DATA)

    while True:
        print("\n   DORMORA : A Smart Hostel Management Tool   ")
        print("\n1. Water & Washroom Issue")
        print("2. Roommate (register / view matches)")
        print("3. Complaint Viewer")
        print("4. Mess Menu & Attendance")
        print("5. Menu Management")
        print("6. Smart Alerts")
        print("7. Exit")

        ch = input("Choose (1-7): ").strip()

        if ch == "1":
            water_and_washroom_issue()
        elif ch == "2":
            print("\nA) Register your profile")
            print("B) View saved profiles & suggested matches (admin)")
            sub = input("Choose A or B: ").strip().upper()
            if sub == "A":
                add_student_profile()
            elif sub == "B":
                view_matches()
            else:
                print("Invalid option.")
        elif ch == "3":
            complaint_viewer()
        elif ch == "4":
            mess_analyzer()
        elif ch == "5":
            menu_management()
        elif ch == "6":
            smart_alerts()
        elif ch == "7":
            print("Exiting... Bye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
