import os

import psycopg2
from dotenv import load_dotenv

# Load database settings from the .env file.
load_dotenv()

# Database configuration is kept outside the Python source code.
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}


def get_connection():
    """Establishes and returns a database connection."""
    missing = [key for key in ("dbname", "user", "password") if not DB_PARAMS[key]]
    if missing:
        raise ValueError(
            "Missing database settings in .env: " + ", ".join(missing)
        )
    return psycopg2.connect(**DB_PARAMS)


def create_user(name, email):
    """CREATE: Inserts a new user into the database."""
    query = "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;"
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (name, email))
        user_id = cur.fetchone()[0]
        conn.commit()
        print(f"Successfully created user '{name}' with ID: {user_id}")

    except Exception as error:
        print(f"Error creating user: {error}")
        if conn:
            conn.rollback()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def update_user_email(user_id, new_email):
    """UPDATE: Modifies an existing user's email."""
    query = "UPDATE users SET email = %s WHERE id = %s;"
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (new_email, user_id))
        conn.commit()

        if cur.rowcount:
            print(f"Successfully updated user ID {user_id} to new email: {new_email}")
        else:
            print(f"No user found with ID: {user_id}")

    except Exception as error:
        print(f"Error updating user: {error}")
        if conn:
            conn.rollback()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def delete_user(user_id):
    """DELETE: Removes a user from the database."""
    query = "DELETE FROM users WHERE id = %s;"
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        conn.commit()

        if cur.rowcount:
            print(f"Successfully deleted user ID {user_id}")
        else:
            print(f"No user found with ID: {user_id}")

    except Exception as error:
        print(f"Error deleting user: {error}")
        if conn:
            conn.rollback()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    print("--- Starting CRUD Exercise ---")

    # CREATE: Use a unique email each time you run this example.
    create_user("Alice Smith", "alice@example.com")

    # UPDATE: Uncomment and use an existing user ID.
    # update_user_email(1, "alice.new@example.com")

    # DELETE: Uncomment and use an existing user ID.
    # delete_user(1)
