import json
import os
from datetime import datetime, timedelta, date

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

def input_price(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Invalid Price. Please enter a number.") 

def input_price_update(text):
    while True:
        s = input(text).strip()
        if s == "":
            return None
        try:
            return int(s)
        except ValueError:
            print("Invalid Price. Please enter a number.")

def create_car():
    global car_id
    print("\n--- Add New Car ---")

    brand = input("Enter Car Brand: ")
    model = input("Enter Car Model: ")
    year = input("Enter Manufacture Year: ")
    rate = input_price("Enter Car Rate : ")
    car_id += 1

    car = {
        "id": car_id,
        "brand": brand,
        "model": model,
        "year": year,
        "rate" : rate,
        "rented_dates": []  # Format ["YYYY-MM-DD"]
    }

    cars.append(car)
    print(f"Car added with ID: {car_id}")

def read_cars():
    print("\n--- List of Cars ---")
    if not cars:
        print("No cars available.")
        return

    for car in cars:
        rented = ", ".join(car["rented_dates"]) or "None"
        print(f"ID: {car['id']}, Brand: {car['brand']}, Model: {car['model']}, Year: {car['year']}, Rate: Rp.{car['rate']}, Rented Dates: {rented}")

def update_car():
    read_cars()
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
        rate = input_price_update(f"New Rate (current: {car['rate']}): ") or car['rate']
        car.update({"brand": brand, "model": model, "year": year, "rate" : rate}) 
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
            print(f"Car '{deleted['model']}' deleted.")
            return
    print(" Car ID not found.")

def rent_car():
    read_cars()
    cid = _input_int("Enter Car ID to rent: ")
    car = _find_car(cid)
    if not car:
        print("Car ID not found.")
        return
    start, end = _get_rental_period()
    if not _validate_period(start, end):
        return
    requested = _generate_dates(start, end)
    if _is_conflict(car, requested):
        return
    cost = _calculate_cost(car['rate'], start, end)
    if not _process_payment(cost):
        return
    car['rented_dates'].extend(requested)
    print(f"Car booked for {(end-start).days+1} day(s) from {start} to {end}.")

def _input_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Must be a number.")


def _find_car(cid):
    return next((c for c in cars if c['id'] == cid), None)

def _get_rental_period():
    start_str = input("Enter start date (YYYY-MM-DD): ").strip()
    end_str = input("Enter end date (YYYY-MM-DD): ").strip()
    return datetime.strptime(start_str, "%Y-%m-%d").date(), datetime.strptime(end_str, "%Y-%m-%d").date()

def _validate_period(start, end):
    today = date.today()
    if start < today:
        print("Start date cannot be before today.")
        return False
    if end < start:
        print("End date must be after start date.")
        return False
    return True

def _generate_dates(start, end):
    days = (end - start).days + 1
    return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]

def _is_conflict(car, dates):
    for d in dates:
        if d in car['rented_dates']:
            print(f"Car already rented on {d}.")
            return True
    return False

def _calculate_cost(rate, start, end):
    days = (end - start).days + 1
    total = rate * days
    print(f"Total cost: {total} for {days} day(s)")
    return total

def _process_payment(amount):
    confirm = input("Proceed to payment? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Booking cancelled.")
        return False
    payment = input_price("Enter payment amount: ")
    
    while True:
        if payment >= amount:
            print(f"Payment successful. Change: {payment-amount}")
            return True
        print(f"Insufficient payment.  {amount-payment} more.")
        
        

def check_availability():
    date_str = input("Enter date to check (YYYY-MM-DD): ")
    if not is_valid_date(date_str):
        print("Invalid date format.")
        return
    today = date.today()
    if date_str < today:
        print("Cannot input past date.")
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
        print("0. Change Role")  
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
