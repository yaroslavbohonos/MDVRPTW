import pandas as pd
import sqlite3
import csv

class DataBase():
    # Assign object attributes
    def __init__(self, dbPath='./data/MDVRPTW_database.db'):
        self.dbPath = dbPath

    # Handle database connection
    def connect_db(self):
        return sqlite3.connect(self.dbPath)

    def loadTables(self):
        # Create or connect to database
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # Load data from CSV
        df = pd.read_csv("./data/problem_data.csv")
        
        # Create Problems table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Problems (
                ProblemID INTEGER PRIMARY KEY AUTOINCREMENT,
                NumCustomers INTEGER NOT NULL,
                NumDepots INTEGER NOT NULL,
                NumVehicles INTEGER NOT NULL,
                FileName TEXT NOT NULL
            )
        ''')
        
        # Create Solutions table, with a foreign key to 'Problems'
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

        # Load CSV data into Problems table
        df.to_sql('Problems', conn, if_exists='replace', index=False)

        # Add test data to Solutions table
        solutions_data = [
            (1, 'Roulette Wheel', 0.1, 123.45, '2024-09-15', '12:30'),
            (1, 'Tournament', 0.15, 130.78, '2024-09-16', '12:35')
        ]
        
        cursor.executemany('''
            INSERT INTO Solutions (ProblemID, SelectionType, MutationProb, Distance, Date, Time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', solutions_data)

        # Commit and close database connection
        conn.commit()
        conn.close()

    def returnCustomerData(self, problemIndex: int):
        """ 1-indexed index notation """        

        # Connect to database
        conn = self.connect_db()
        cursor = conn.cursor()

        # Load customer data without header titles and the first index column
        # usecols uses 0-indexed column numbering
        df = pd.read_csv(f"./data/problem{problemIndex}/customers.csv", usecols=[1, 2, 3, 4, 5], header=0)
        
        # Convert DataFrame to a list of lists
        data = df.values.tolist()

        # Close database connection
        conn.close()

        return data

    def returnDepotData(self, problemIndex: int): 
        """ 1-indexed index notation """
        
        # Connect to database
        conn = self.connect_db()
        cursor = conn.cursor()

        # Load depot data without header titles and the first index
        df = pd.read_csv(f"./data/problem{problemIndex}/depots.csv", usecols=[1, 2, 3, 4, 5], header=0)

        # Convert DataFrame to a list of lists
        data = df.values.tolist()
        
        # Close database connection
        conn.close()

        return data
  
    def returnSolutions(self, problemIndex: int):
        """ 1-indexed for indexes"""
        
        # Connect to the database
        conn = self.connect_db()
        cursor = conn.cursor()

        # Query to select all columns except SolutionID for the given ProblemID
        query = '''
            SELECT ProblemID, SelectionType, MutationProb, Distance, Date, Time
            FROM Solutions
            WHERE ProblemID = ?
        '''
        
        # Execute the query with the provided problemIndex
        cursor.execute(query, (problemIndex,))

        # Fetch all results into a list
        results = cursor.fetchall()

        # Create a DataFrame from the query result and exclude the SolutionID
        columns = ['ProblemID', 'SelectionType', 'MutationProb', 'Distance', 'Date', 'Time']
        df = pd.DataFrame(results, columns=columns)

        # Close the connection
        conn.close()

        # Return the DataFrame
        return df