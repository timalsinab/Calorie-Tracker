# Calorie Tracker

A simple Calorie Tracker application that allows users to add food entries, display their daily food intake summary, and clear the database upon exiting the program. The application uses the CalorieNinjas API to fetch nutritional information for various foods.

## Features

- **Add Food Entries**: Add food entries with nutritional data fetched from CalorieNinjas API.
- **Display Summary**: Display a summary of daily food intake including total calories, fat, protein, and carbohydrates.
- **Clear Database**: Clear the database when exiting the program.

## Requirements

- Python 3.x
- `requests` library
- SQLite3

## Setup

1. Clone the repository or download the source code.
2. Install the required libraries using pip:
    ```sh
    pip install requests
    ```
3. Ensure you have SQLite3 installed on your system.

## Usage

1. Run the `project.py` script:
    ```sh
    python3 project.py
    ```
2. Choose an option from the menu:
   - **Add Food Entry**: Add a new food entry by selecting from predefined options or entering your own food item.
   - **Display Food Entries and Calorie Summary**: Display the food entries for the current day along with a summary of total calories, fat, protein, and carbohydrates.
   - **Exit**: Clear the database and exit the application.

## Running Style Checks and Tests

1. To run style checks with flake8:
    ```sh
    flake8
    ```
2. To run unit tests:
    ```sh
    python -m unittest discover -s tests
    ```

## Code Structure

- `project.py`: The main script that runs the Calorie Tracker application.
- `setup_database()`: Initializes the SQLite database and creates the `food_entries` table.
- `fetch_nutrition_data(food_query)`: Fetches nutritional data for a given food query from the CalorieNinjas API.
- `save_food_entry(conn, food_name, nutrition_data)`: Saves the food entry and its nutritional data to the database.
- `display_summary(conn)`: Displays the food entries for the current day and the total summary of nutritional data.
- `clear_database(conn)`: Clears all entries from the database.

## API Key

The application uses the CalorieNinjas API to fetch nutritional information. Replace the `API_KEY` in the script with your own API key from [CalorieNinjas](https://calorieninjas.com/).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
