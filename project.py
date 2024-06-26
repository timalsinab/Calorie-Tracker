import os

# Constants
API_KEY = 'dQ0EeYZaDxaAOXS6LbMFsg==OcC9uVgRcxJ6r7Hk'  # CalorieNinjas API Key
BASE_URL = 'https://api.calorieninjas.com/v1/nutrition?query='


def fetch_nutrition_data(food_query):
    response = requests.get(BASE_URL + food_query, headers={'X-Api-Key': API_KEY})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def main():
    
    while True:
        print("\nOptions:")
        print("1. Add Food Entry")
        print("2. Display Food Entries and Calorie Summary")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            food_name = input("Please enter the food you have eaten: ")
            
            # Fetch nutritional data
            nutrition_data = fetch_nutrition_data(food_name)
            
            print(nutrition_data)

        elif choice == '2':
            display_summary(conn)
        
        elif choice == '3':
            if conn:
                conn.close()
            print("Exiting CalorieTracker. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
