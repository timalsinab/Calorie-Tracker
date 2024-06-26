import os
import sqlite3
import requests


API_KEY = 'dQ0EeYZaDxaAOXS6LbMFsg==OcC9uVgRcxJ6r7Hk'  # CalorieNinjas API Key
BASE_URL = 'https://api.calorieninjas.com/v1/nutrition?query='

# Database setup
DB_NAME = 'calorie_tracker.db'


predefined_food_items = [
    "1lb chicken",
    "1 apple",
    "1 banana",
    "1 rice",
]

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            calories REAL NOT NULL,
            fat REAL,
            protein REAL,
            carbohydrates REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def fetch_nutrition_data(food_query):
    response = requests.get(BASE_URL + food_query, headers={'X-Api-Key': API_KEY})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def save_food_entry(conn, food_name, nutrition_data):
    cursor = conn.cursor()
    if nutrition_data and 'items' in nutrition_data:
        item = nutrition_data['items'][0]
        calories = item.get('calories', 0)
        fat = item.get('fat_total_g', 0)
        protein = item.get('protein_g', 0)
        carbohydrates = item.get('carbohydrates_total_g', 0)
        
        cursor.execute('''
            INSERT INTO food_entries (food_name, calories, fat, protein, carbohydrates)
            VALUES (?, ?, ?, ?, ?)
        ''', (food_name, calories, fat, protein, carbohydrates))
        conn.commit()
        print(f"Saved {food_name} with {calories} calories.")
    else:
        print("No nutritional data available to save.")

def display_summary(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT food_name, calories, fat, protein, carbohydrates
        FROM food_entries
        WHERE DATE(timestamp) = DATE('now')
    ''')
    entries = cursor.fetchall()
    
    if entries:
        print(f"Today's Food Entries:")
        for entry in entries:
            food_name, calories, fat, protein, carbohydrates = entry
            print(f"{food_name} - Calories: {calories}, Fat: {fat}g, Protein: {protein:.2f}g, Carbohydrates: {carbohydrates}g")
        
        cursor.execute('''
            SELECT SUM(calories), SUM(fat), SUM(protein), SUM(carbohydrates)
            FROM food_entries
            WHERE DATE(timestamp) = DATE('now')
        ''')
        result = cursor.fetchone()
        if result:
            total_calories, total_fat, total_protein, total_carbohydrates = result
            print(f"\nToday's Summary:")
            print(f"Total Calories: {total_calories}")
            print(f"Total Fat: {total_fat}g")
            print(f"Total Protein: {total_protein:.2f}g")
            print(f"Total Carbohydrates: {total_carbohydrates}g")
    else:
        print("No entries found for today.")

def clear_database(conn):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM food_entries')
    conn.commit()
    print("Database cleared.")

def main():
    conn = setup_database()
    
    while True:
        print("\nOptions:")
        print("1. Add Food Entry")
        print("2. Display Food Entries and Calorie Summary")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Choose a food item from the list below or type your own:")
            for i, item in enumerate(predefined_food_items, 1):
                print(f"{i}. {item}")
            print("0. Enter your own food item")
            food_choice = input("Enter the number of your choice or type your own food item: ")

            if food_choice.isdigit() and 0 <= int(food_choice) <= len(predefined_food_items):
                if int(food_choice) == 0:
                    food_name = input("Please enter the food you have eaten: ")
                else:
                    food_name = predefined_food_items[int(food_choice) - 1]
            else:
                food_name = food_choice


            nutrition_data = fetch_nutrition_data(food_name)
            

            save_food_entry(conn, food_name, nutrition_data)
            
        elif choice == '2':
            display_summary(conn)
        
        elif choice == '3':
            clear_database(conn)
            if conn:
                conn.close()
            print("Exiting CalorieTracker. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()