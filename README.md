# PostgreSQL CRUD Operations Using Python

## Project Overview

This project demonstrates how to perform basic **CRUD (Create, Read, Update, Delete)** operations on a PostgreSQL database using Python and the `psycopg2` library.

The program establishes a connection to a PostgreSQL database and performs operations on a table named `users`.

## Technologies Used

- **Python** – Programming language used to write the application.
- **PostgreSQL** – Relational database management system used to store user information.
- **pgAdmin 4** – Graphical interface for managing the PostgreSQL database.
- **psycopg2** – Python library used to connect and interact with PostgreSQL.

## Database Configuration

The program connects to a PostgreSQL database using the following parameters:

| Parameter | Value |
|---|---|
| Database name | `sample` |
| Username | `db_user` |
| Host | `localhost` |
| Port | `5433` |

**Note:** Database credentials are configured in the Python script for this practice example. For better security, credentials should be stored in environment variables rather than hardcoded in the source code.

## Operations Performed

### 1. Database Connection

The `get_connection()` function establishes a connection to the PostgreSQL database using the `psycopg2.connect()` method.

### 2. Create User

The `create_user(name, email)` function inserts a new user record into the `users` table.

- Accepts a user's name and email address.
- Inserts the information into the database.
- Returns the newly created user's ID.
- Uses `commit()` to save the changes.

### 3. Update User Email

The `update_user_email(user_id, new_email)` function updates the email address of an existing user.

- Identifies the user using their ID.
- Updates the email address.
- Saves the changes to the database.

### 4. Delete User

The `delete_user(user_id)` function removes a user record from the `users` table.

- Identifies the record using the user's ID.
- Executes a DELETE statement.
- Commits the changes to the database.

## Error Handling and Transaction Management

The program uses `try`, `except`, and `finally` blocks to manage database operations.

- **try:** Executes database operations.
- **except:** Handles errors that may occur during execution.
- **rollback():** Reverses uncommitted changes if an error occurs.
- **finally:** Ensures that the database connection is closed.

The SQL queries use parameterized statements (`%s`) to safely pass user inputs and reduce the risk of SQL injection.

## How to Run the Project

1. Ensure Python and PostgreSQL are installed.
2. Install the required Python library:

   ```bash
   pip install psycopg2-binary
   ```

3. Create a PostgreSQL database named `sample`.
4. Create a table named `users`:

   ```sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100),
       email VARCHAR(150)
   );
   ```

5. Configure the database connection parameters in the Python file.
6. Run the Python script:

   ```bash
   python dot.py
   ```

## Video Explanation

A video explanation of the project is available here:

[Watch the PostgreSQL CRUD Operations Explanation](https://vimeo.com/1240189236?fl=tl&fe=ec)

## Learning Outcomes

Through this project, I practised:

- Connecting Python applications to PostgreSQL.
- Performing CRUD operations.
- Writing and executing SQL queries through Python.
- Managing database transactions using `commit()` and `rollback()`.
- Handling database errors.
- Closing database connections properly.

## Project Purpose

This project was developed as a practical exercise to understand the fundamentals of Python database connectivity and PostgreSQL operations.
