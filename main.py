import pymysql

FoodIDs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
FoodNames = [
    "Veg Sandwich", "Veg Burger", "Veg Patties", "Veg Pizza",
    "Red Sauce Pasta", "Veg Chowmein", "Veg Fried Rice", "Veg Manchurian",
    "Idli Sambhar", "Dosa", "Coca Cola", "Thums Up"
]
Prices = [30, 50, 30, 80, 100, 60, 60, 70, 70, 90, 40, 40]
Cuisines = [
    "Fast Food", "Fast Food", "Fast Food", "Italian", "Italian", "Chinese",
    "Chinese", "Chinese", "South Indian", "South Indian", "Beverage",
    "Beverage"
]


def fillTables(conn):
    cursor = conn.cursor()
    noOfItems = 12
    for i in range(noOfItems):
        query = "INSERT INTO MENU VALUES(%d,'%s','%s',%d);" % (
            FoodIDs[i], FoodNames[i], Cuisines[i], Prices[i])
        cursor.execute(query)
        conn.commit()
    cursor.close()


def initConn():
    serverIP = "localhost"
    username = input("Enter MySQL username: ")
    password = input("Enter password: ")
    dbName = "canteen"

    conn = pymysql.connect(host=serverIP, user=username, passwd=password)

    print("")
    print(">> Connection established!")

    cursor = conn.cursor()

    cursor.execute("SHOW DATABASES;")
    dbList = cursor.fetchall()

    dbPresent = False
    for db in dbList:
        if dbName not in db:
            dbPresent = False
            continue
        else:
            dbPresent = True
            break

    if not dbPresent:
        cursor.execute("CREATE DATABASE " + dbName)
        cursor.execute("USE " + dbName)

        cursor.execute("""Create table MENU(FoodID int primary key,
        FoodName varchar(20) NOT NULL,
        Cuisine varchar(20), Price int NOT NULL);""")

        cursor.execute("""Create table CUSTOMERS(CustID varchar(4) primary key,
        CustName varchar(20) NOT NULL, Orders int, Total int);""")
        print(">> Database and Tables generated!")
        fillTables(conn)

    else:
        cursor.execute("USE " + dbName)
        print(">> Using existing Database and Tables.")

    cursor.close()

    return conn


def displayMenu(conn):
    print("")
    print(
        "**********************************************************************"
    )
    print(
        "*                                                                    *"
    )
    print(
        "*      ___  _    _   _                                               *"
    )
    print(
        "*      |    / \  / \ | \                                             *"
    )
    print(
        "*      |-- |   ||   ||  |                                            *"
    )
    print(
        "*      |__  \_/  \_/ |_/              __                             *"
    )
    print(
        "*      /  \      __           __     /  \                            *"
    )
    print(
        "*      \__  |-- |  \ \    /| /   |-- \__                             *"
    )
    print(
        "*         \ |-- |--/  \  / ||    |--    \                            *"
    )
    print(
        "*      \__/ |-- |  \   \/  | \__ |-- \__/                            *"
    )
    print(
        "*                                                                    *"
    )
    print(
        "*                                                                    *"
    )
    cursor = conn.cursor()
    cursor.execute("Select * from MENU;")
    rows = cursor.fetchall()
    print("*     " + "{0:10} {1:20} {2:20} {3:10}".format(
        "Food ID", "Food Name", "Cuisine", "Price") + "*")
    print(
        "*     ----------------------------------------------------------     *"
    )
    for Rec in rows:
        foodID = Rec[0]
        foodName = Rec[1]
        cuisine = Rec[2]
        price = Rec[3]
        print("*  " + "{0:^9}-    {1:<18}   {2:<14} {3:>10}".format(
            foodID, foodName, cuisine, price) + "      *")
    print(
        "*     ----------------------------------------------------------     *"
    )
    print(
        "*                                                                    *"
    )
    print(
        "**********************************************************************"
    )

    cursor.close()


def billGeneration(conn, details):
    cursor = conn.cursor()
    custID = details[0]
    custName = details[1]
    orderedItems = details[2]
    orderedItemsQuantity = details[3]
    totalPrice = 0
    for i in range(len(orderedItems)):
        totalPrice += Prices[orderedItems[i] - 1] * orderedItemsQuantity[i]
    totalOrders = 0
    for i in orderedItemsQuantity:
        totalOrders += i

    query = "INSERT INTO CUSTOMERS VALUES('%s','%s',%d,%d);" % (
        custID, custName, totalOrders, totalPrice)
    cursor.execute(query)
    conn.commit()

    print(
        "\n\n*****************************************************************"
    )
    print("*                                                               *")
    print("*                        Food Services                          *")
    print("*                                                               *")
    print("*                  Customer ID: " + custID + "\t\t\t\t*")
    print("*                  Customer Name: " + custName + "\t\t\t\t*")
    print("*                                                               *")
    print("*                        You Ordered:                           *")
    print("*                                                               *")
    for i in range(len(orderedItems)):
        print("*\t", orderedItemsQuantity[i], FoodNames[orderedItems[i] - 1],
              "    \t-\t", orderedItemsQuantity[i], "x",
              Prices[orderedItems[i] - 1], "=",
              int(orderedItemsQuantity[i]) * Prices[orderedItems[i] - 1],
              "\t\t*")
    print("*                                                               *")
    print("*                                                               *")
    print("*\t Grand Total: Rs.", totalPrice, "\t\t\t\t\t*")
    print("*                                                               *")
    print("*                            ******                             *")
    print("*                                                               *")
    print("*                      Thanks for Visiting                      *")
    print("*                                                               *")
    print("*****************************************************************")

    cursor.close()


def takeOrder(conn):
    cursor = conn.cursor()
    c1 = 'y'
    cursor.execute("SELECT * FROM CUSTOMERS;")
    noOfEntriesAlready = cursor.fetchall()
    cIndex = len(noOfEntriesAlready)
    while (c1 == 'y'):
        cIndex += 1
        orderedItems = []
        orderedItemsQuantity = []
        custID = "AX" + str(cIndex)
        custName = input("Please enter your name: ")
        custPhnNo = input("Please enter your mobile number: ")
        c2 = 'y'
        while (c2 != 'n'):
            order = int(
                input("What would you like to have? (Enter choice 1-12): "))
            if order in FoodIDs:
                quantity = int(
                    input("How many of this would you like to order: "))
                if (order not in orderedItems):
                    orderedItems.append(order)
                    orderedItemsQuantity.append(quantity)
                else:
                    orderedItemsQuantity[len(orderedItemsQuantity) -
                                         1] += quantity
                c2 = input("Would you like to order anything else? (y/n): ")
                while (c2 != 'y' and c2 != 'n'):
                    print("Oops, you entered the wrong option.")
                    c2 = input(
                        "Would you like to order anything else? (y/n): ")
            else:
                print("Sorry, you entered the wrong choice.")
                c2 = input("Would you like to place an order again? (y/n): ")
                while (c2 != 'y' or c2 != 'n'):
                    print("Oops, you entered the wrong option.")
                    c2 = input(
                        "Would you like to order anything else? (y/n): ")
        print(
            "Thank you! Please wait while you receive your orders. Here's your bill..."
        )
        details = [custID, custName, orderedItems, orderedItemsQuantity]
        billGeneration(conn, details)
        print("")
        c1 = input("Are you a new customer? (y/n): ")
    print("Thank you for eating at Food Services! Have a great day!")
    cursor.close()


def Main():
    conn = initConn()
    displayMenu(conn)
    takeOrder(conn)
    conn.close()


Main()
