import pandas as pd
import sqlite3

# Load data file
df = pd.read_csv("./data/problem_data.csv")

# Data clean up
df.columns = df.columns.str.strip()

# Create or connect to a SQLite database
conn = sqlite3.connect('MDVRPTW_database.db')
cursor = conn.cursor()

# Create 'Problems' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Problems (
        ProblemID INTEGER PRIMARY KEY AUTOINCREMENT,
        NumCustomers INTEGER NOT NULL,
        NumDepots INTEGER NOT NULL,
        NumVehicles INTEGER NOT NULL,
        FileName TEXT NOT NULL
    )
''')

# Create  'Solutions' table with a foreign key to 'Problems'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Solutions (
        SolutionID INTEGER PRIMARY KEY AUTOINCREMENT,
        ProblemID INTEGER,
        SelectionType TEXT NOT NULL,
        MutationProb REAL NOT NULL,
        Distance REAL NOT NULL,
        Date TEXT NOT NULL,
        Time TEXT NOT NULL,
        FOREIGN KEY (ProblemID) REFERENCES Problems(ProblemID)
    )
''')

# Load CSV data into 'Problems' table, removing the "index" column
df.to_sql('Problems', conn, if_exists='replace', index=False)

# Add test data to 'Solutions' table using substitution of solutions_data into SQL queury
# Inserting a solution for ProblemID = 1
solutions_data = [
    (1, 'Roulette Wheel', 0.1, 123.45, '2024-09-15', '12:30'),
    (1, 'Tournament', 0.15, 130.78, '2024-09-16', '12:35')
]

cursor.executemany('''
    INSERT INTO Solutions (ProblemID, SelectionType, MutationProb, Distance, Date, Time)
    VALUES (?, ?, ?, ?, ?, ?)
''', solutions_data)

# Commit changes for database and close connection
conn.commit()
conn.close()
