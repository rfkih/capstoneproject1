import json
import os
from datetime import datetime

cars = []
car_id = 0
DATA_FILE = "cars.json"

def load_data():
    global cars, car_id
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            cars = data.get("cars", [])
            car_id = data.get("car_id", 0)

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "cars": cars,
            "car_id": car_id
        }, f, indent=4)

def show_menu(role):
    print("\n=== Car Rental System ===")
    print(f"Logged in as: {role.upper()}")
    print("1. View Cars")
    print("2. Check Car Availability by Date")
    if role == "admin":
        print("3. Add New Car")
        print("4. Update Car")
        print("5. Delete Car")
        print("6. Exit")
    else:
        print("3. Rent a Car")
        print("4. Exit")

def create_car():
    global car_id
    print("\n--- Add New Car ---")

    brand = input("Enter Car Brand: ")
    model = input("Enter Car Model: ")
    year = input("Enter Manufacture Year: ")
    car_id += 1

    car = {
        "id": car_id,
        "brand": brand,
        "model": model,
        "year": year,
        "rented_dates": []  # Format ["YYYY-MM-DD"]
    }

    cars.append(car)
    print(f"✅ Car added with ID: {car_id}")

def read_cars():
    print("\n--- List of Cars ---")
    if not cars:
        print("No cars available.")
        return

    for car in cars:
        rented = ", ".join(car["rented_dates"]) or "None"
        print(f"ID: {car['id']}, Brand: {car['brand']}, Model: {car['model']}, Year: {car['year']}, Rented Dates: {rented}")

def update_car():
    read_cars("admin")
    if not cars:
        return

    try:
        car_id_input = int(input("Enter Car ID to update: ").strip())
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    car = next((c for c in cars if c["id"] == car_id_input), None)

    if car:
        print("Leave input blank to keep current value.")
        brand = input(f"New Brand (current: {car['brand']}): ") or car['brand']
        model = input(f"New Model (current: {car['model']}): ") or car['model']
        year = input(f"New Year (current: {car['year']}): ") or car['year']
        car.update({"brand": brand, "model": model, "year": year})
        print("Car updated.")
    else:
        print(" Car ID not found.")

def delete_car():
    read_cars()
    if not cars:
        return

    try:
        car_id_input = int(input("Enter Car ID to delete: ").strip())
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    for i, car in enumerate(cars):
        if car["id"] == car_id_input:
            deleted = cars.pop(i)
            print(f"✅ Car '{deleted['model']}' deleted.")
            return
    print(" Car ID not found.")

def rent_car():
    read_cars()
    if not cars:
        return

    try:
        car_id_input = int(input("Enter Car ID to rent: ").strip())
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    car = next((c for c in cars if c["id"] == car_id_input), None)

    if car:
        date_str = input("Enter rental date (YYYY-MM-DD): ").strip()
        if not is_valid_date(date_str):
            print("Invalid date format.")
            return
        if date_str in car["rented_dates"]:
            print("Car is already rented on that date.")
        else:
            car["rented_dates"].append(date_str)
            print(f"Car rented for {date_str}.")
    else:
        print("Car ID not found.")

def check_availability():
    date_str = input("Enter date to check (YYYY-MM-DD): ")
    if not is_valid_date(date_str):
        print("Invalid date format.")
        return
    print(f"\nAvailable cars on {date_str}:")
    found = False
    for car in cars:
        if date_str not in car['rented_dates']:
            found = True
            print(f"- ID: {car['id']}, Brand: {car['brand']}, Model: {car['model']}, Year: {car['year']}")
    if not found:
        print("No cars available on this date.")

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def login():
    print("=== Welcome to the Car Rental App ===")
    while True:
        role = input("Login as 'admin' or 'renter': ").strip().lower()
        if role in ["admin", "renter"]:
            return role
        print("Invalid role. Please enter 'admin' or 'renter'.")

def main():
    load_data()
    role = login()
    while True:
        show_menu(role)
        print("0. Change Role")  # ⬅️ new option in the menu
        choice = input("Select an option: ").strip()

        if choice == "0":
            role = login()
            continue

        if role == "admin":
            if choice == "1":
                read_cars()
            elif choice == "2":
                check_availability()
            elif choice == "3":
                create_car()
            elif choice == "4":
                update_car()
            elif choice == "5":
                delete_car()
            elif choice == "6":
                save_data()
                print("Data saved. Exiting...")
                break
            else:
                print("Invalid choice.")
        else:  
            if choice == "1":
                read_cars()
            elif choice == "2":
                check_availability()
            elif choice == "3":
                rent_car()
            elif choice == "4":
                save_data()
                print("Data saved. Goodbye!")
                break
            else:
                print("Invalid choice.")

main()
