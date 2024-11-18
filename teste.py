import json
from mysql.connector import Error as msqlError

import mysql.connector

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def execute_sql_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def compare_results(actual, expected):
    return actual == expected

def main():
    # Load test cases from JSON file
    test_cases = read_json('test_script.json')

    # Connect to MySQL database
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='your_database',
            user='your_username',
            password='your_password'
        )
        if connection.is_connected():
            print("Connected to MySQL database")

            for test in test_cases:
                sql_script = test['sql_script']
                expected_result = test['expected_result']

                try:
                    actual_result = execute_sql_query(connection, sql_script)
                    if compare_results(actual_result, expected_result):
                        print(f"Test '{test['test_name']}' passed.")
                    else:
                        print(f"Test '{test['test_name']}' failed. Expected: {expected_result}, Got: {actual_result}")
                except msqlError as e:
                    print(f"Error executing query for test '{test['test_name']}': {e}")

    except msqlError as e:
        print(f"Error connecting to MySQL database: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()