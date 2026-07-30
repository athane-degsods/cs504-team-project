install sqlite3 from the official website: https://www.sqlite.org/quickstart.html

create a new database file: auth.db

create the first table using SQL command:
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  pin TEXT NOT NULL
);
```

how to use sqlite3 in python: https://www.geeksforgeeks.org/python/introduction-to-sqlite-in-python/

Tutorial on using sqlite3 with Sqlitestudio: https://www.sqlitetutorial.net/download-install-sqlite/

add the first (test) user to the database using SQL command:
```sql
INSERT INTO users (username, password, pin)
VALUES ('admin', '123456', '1234');
```

