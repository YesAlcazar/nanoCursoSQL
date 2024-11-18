import argparse
import subprocess

import mysql.connector

def create_db():
    try:
        subprocess.run(['mysql', '-u', 'root', '-p', '<', 'Chinook_MySQL_AutoIncrementPKs.sql'], check=True)
        print("Database created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating database: {e}")

def run_tests():
    try:
        subprocess.run(['python', 'test.py'], check=True)
        print("Tests ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")

def connect_db(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()
        while True:
            command = input("Enter SQL command (or 'exit' to quit): ")
            if command.lower() == 'exit':
                break
            cursor.execute(command)
            if command.strip().upper().startswith("SELECT"):
                for row in cursor.fetchall():
                    print(row)
            else:
                connection.commit()
                print("Command executed successfully.")
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def main():
    parser = argparse.ArgumentParser(description="CLI for database operations")
    parser.add_argument('--create-db', action='store_true', help="Create the database")
    parser.add_argument('--run-tests', action='store_true', help="Run tests")
    parser.add_argument('--connect-db', action='store_true', help="Connect to the database")
    parser.add_argument('--host', type=str, help="Database host")
    parser.add_argument('--user', type=str, help="Database user")
    parser.add_argument('--password', type=str, help="Database password")
    parser.add_argument('--database', type=str, help="Database name")

    args = parser.parse_args()

    if args.create_db:
        create_db()
    elif args.run_tests:
        run_tests()
    elif args.connect_db:
        if args.host and args.user and args.password and args.database:
            connect_db(args.host, args.user, args.password, args.database)
        else:
            print("Please provide host, user, password, and database to connect.")

if __name__ == "__main__":
    main()