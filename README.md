# PostgreSQL CRUD Assignment using psycopg2

This project demonstrates basic user CRUD operations using Python, PostgreSQL,
and `psycopg2`.

## Project files

- `main.py` — Python code for creating, updating, and deleting users.
- `.env` — Local PostgreSQL connection settings (not committed to Git).
- `.env.example` — Safe template showing the required environment variables.
- `schema.sql` — Creates the `users` table.
- `requirements.txt` — Python dependencies.
- `.gitignore` — Excludes `.env` and generated files from Git.

## Setup

1. Create a PostgreSQL database.
2. Open `schema.sql` in pgAdmin (while connected to that database) and execute it.
3. Edit `.env` and enter the database name, username, password, host, and port.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the program:

   ```bash
   python main.py
   ```

## Environment variables

The application reads these values from `.env`:

```env
DB_NAME=your_db_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Do not commit `.env` to GitHub. It is excluded by `.gitignore`.
Commit `.env.example` instead, so others know which settings they need.

## Notes

- The `users` table has an auto-generated ID and a unique email address.
- The default example inserts `alice@example.com`. Because email is unique,
  running it repeatedly will fail after the first successful insert unless
  the row is changed or removed.
- Uncomment the UPDATE or DELETE example calls in `main.py` to test those
  operations with an existing user ID.
