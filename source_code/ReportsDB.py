import pandas as pd
import sqlite3
import csv
import os

class DataBase():
    # Assign object attributes
    def __init__(self, dbPath = './data/MDVRPTW_database.db', 
                 problemDataPath = './data/problem_data.csv'):
        self.__dbPath = dbPath
        self.__problemDataPath = problemDataPath
        
    # Getters
    def getDbPath(self):
        return self.__dbPath

    def getProblemDataPath(self):
        return self.__problemDataPath
    
    def getCustomersDataPath(self, problemIndex):
        return f'./data/problem{problemIndex}/customers.csv'

    def getDepotsDataPath(self, problemIndex):
        return f'./data/problem{problemIndex}/depots.csv'

    def isPathExist(self, path):
        if os.path.exists(path):
            return True
        else:
            return False

    # Handle database connection
    def connect_db(self):
        if self.isPathExist(self.getDbPath()):
            return sqlite3.connect(self.getDbPath())
        else:
            return False
        
    def loadTables(self):
        # Create if path does not exists or connect to database
        conn = sqlite3.connect(self.getDbPath())
        cursor = conn.cursor()
        
        # Load data from CSV
        df = pd.read_csv(self.getProblemDataPath())
        
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
            # (1, 'Roulette Wheel', 0.1, 123.45, '2024-09-15', '12:30'),
            # (1, 'Tournament', 0.15, 130.78, '2024-09-16', '12:35')
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
        # Check if path exists 
        if self.isPathExist(self.getCustomersDataPath(problemIndex)):
            # Load customer data without header titles and the first index column
            # usecols uses 0-indexed column numbering
            df = pd.read_csv(self.getCustomersDataPath(problemIndex), usecols=[1, 2, 3, 4, 5], header=0)
        
            # Convert DataFrame to a list of lists
            data = df.values.tolist()
            return data
        else:
            print("An error occured in returning customers data due to an incorrect customers.csv path")
            return []

    def returnDepotData(self, problemIndex: int): 
        """ 1-indexed index notation """
        
        if self.isPathExist(self.getDepotsDataPath(problemIndex)):
            # Read depots data and create DataFrame object
            df = pd.read_csv(self.getDepotsDataPath(problemIndex), usecols=[1, 2, 3, 4, 5], header=0)

            # Convert DataFrame to a list of lists
            data = df.values.tolist()
            return data
        else:
            print("An error occured in returning depots data due to an incorrect depots.csv path")
            return []
  
    def returnSolutions(self, problemIndex: int):
        """ 1-indexed for indexes"""
        
        # Connect to the database
        conn = self.connect_db()
        if conn:
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
        else:
            print("An error occured in returning solutions from database due to an incorrect database path")
            return pd.DataFrame(None)