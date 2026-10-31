import psycopg2

DB_PARAMS = {
    "dbname": "sample",
    "user": "db_user",
    "password": "db_password",
    "host": "localhost",
    "port": "5433"
}

def get_connection():
    return psycopg2.connect(**DB_PARAMS)

def create_user(name, email):
    query = "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;"
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (name, email))
        user_id = cur.fetchone()[0]
        conn.commit()
        print(f"Created user with ID: {user_id}")
        cur.close()
    except Exception as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def update_user_email(user_id, new_email):
    query = "UPDATE users SET email = %s WHERE id = %s;"
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (new_email, user_id))
        conn.commit()
        print(f"Updated user ID {user_id}")
        cur.close()
    except Exception as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def delete_user(user_id):
    query = "DELETE FROM users WHERE id = %s;"
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        conn.commit()
        print(f"Deleted user ID {user_id}")
        cur.close()
    except Exception as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_user("Alice Smith", "alice@example.com")
    update_user_email(1, "alice.new@example.com")
    delete_user(1)