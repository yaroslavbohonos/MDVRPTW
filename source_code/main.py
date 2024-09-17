from Reports import Reports

DB = Reports()

DB.loadTables()

DepotData = DB.returnDepotData(0)
CustomerData = DB.returnCustomerData(0)

# Printing each depot data
print("Depots: ")
for row in DepotData:
    print(row)

# Printing each customer data
print("Customers: ")
for row in CustomerData:
    print(row)