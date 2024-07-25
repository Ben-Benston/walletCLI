import sqlite3
import datetime
from termcolor import colored
from tabulate import tabulate

# Set the name of the table to "Transactions"
table_name = "Transactions"


# Function to get the current balance from the database
def getBalance():
    # Create a connection and a cursor
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()
    # Execute a SQL query to get the balance from the last transaction
    c.execute(f"SELECT Balance From {table_name} ORDER BY TransactionID DESC LIMIT 1")
    balance = c.fetchone()[0]
    # Close the connection
    conn.close()
    return balance


# Function to calculate the total income, total expenditure, and current balance
def totalIncExp():
    # Create a connection and a cursor
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()

    # Initialize variables for total income, total expenditure, and balance
    totalInc, totalExp, balance = 0, 0, 0

    # Calculate total income
    c.execute(f"SELECT TransactionAmount FROM {table_name} WHERE TransactionType=1;")
    incomeData = c.fetchall()
    for row in incomeData:
        totalInc += row[0]

    # Calculate total expenditure
    c.execute(f"SELECT TransactionAmount FROM {table_name} WHERE TransactionType=0;")
    expenseData = c.fetchall()
    for row in expenseData:
        totalExp += row[0]

    # Calculate balance
    balance = totalInc + totalExp

    # Close the connection
    conn.close()

    return (totalInc, totalExp, balance)


# Function to Update every single Balance field in the Database
def updateBalance():
    # Create a connection and a cursor
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()

    # Set the Balance of the First Record
    c.execute(f"SELECT TransactionAmount From {table_name} WHERE TransactionID=1")
    prevBal = c.fetchone()[0]
    c.execute(f"UPDATE {table_name} SET Balance={prevBal} WHERE TransactionID=1")

    # Get the ID of the last transaction in the table
    c.execute(f"SELECT * FROM {table_name} ORDER BY TransactionID DESC LIMIT 1")
    lastTransID = c.fetchone()[0]

    for i in range(2, lastTransID + 1):
        # Get Transaction Amount
        c.execute(f"SELECT TransactionAmount From {table_name} WHERE TransactionID={i}")
        transAmt = c.fetchone()[0]

        # Update the Transaction Amount
        c.execute(
            f"UPDATE {table_name} SET Balance={prevBal+transAmt} WHERE TransactionID={i}"
        )
        prevBal += transAmt

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Function to add a new transaction to the database
def addTransaction(transType: int, payName: str, amt: int, note=""):

    # Get current date and time
    current_date = datetime.date.today().strftime("%d-%m-%Y")
    current_time = datetime.datetime.now().time().strftime("%H:%M:%S")

    # Create a connection and a cursor
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()

    # Update the balance based on transaction type
    balance = getBalance()
    if transType == 0:
        amt = -1 * abs(amt)
    elif transType == 1:
        amt = abs(amt)
    balance += amt

    # Insert a new transaction into the database
    sql = f"INSERT INTO {table_name} (TransactionType, PayeePayerName, TransactionAmount, Date, Time, Notes, Balance) VALUES (?, ?, ?, ?, ?, ?, ?)"
    values = (transType, payName, amt, current_date, current_time, note, balance)
    c.execute(sql, values)

    # Update transaction IDs to maintain order
    c.execute(
        """UPDATE Transactions SET TransactionID = new_id
        FROM (
            SELECT ROW_NUMBER() OVER (ORDER BY date, time) AS new_id, TransactionID 
            FROM Transactions
        ) t
        WHERE Transactions.TransactionID = t.TransactionID
    """
    )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def deleteTransaction(transID: int):
    # Open a connection and create a cursor
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()

    # Get the ID of the last transaction in the table
    c.execute(f"SELECT * FROM {table_name} ORDER BY TransactionID DESC LIMIT 1")
    lastTransID = c.fetchone()[0]

    # Check if the provided transaction ID is valid
    if lastTransID < transID:
        print("\nInvalid transaction ID!!!\n")
        return

    # Get the transaction amount of the record to be deleted
    c.execute(
        f"SELECT TransactionAmount From {table_name} WHERE TransactionID={transID}"
    )
    transAmt = c.fetchone()[0]

    # Loop through all the remaining records and update their balances
    for i in range(transID + 1, lastTransID + 1):
        # Get the current balance of the iteration transaction
        c.execute(f"SELECT Balance From {table_name} WHERE TransactionID={i}")
        oldBalance = c.fetchone()[0]

        # Update the Balance
        c.execute(
            f"UPDATE {table_name} SET Balance={oldBalance+(-1*transAmt)} WHERE TransactionID={i}"
        )

    # Delete the transaction record from the table
    c.execute(f"DELETE FROM {table_name} WHERE TransactionID={transID}")

    # Update the transaction IDs to maintain sequential order
    c.execute(
        """UPDATE Transactions SET TransactionID = new_id
        FROM (
            SELECT ROW_NUMBER() OVER (ORDER BY date, time) AS new_id, TransactionID 
            FROM Transactions
        ) t
        WHERE Transactions.TransactionID = t.TransactionID
    """
    )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Function to print the Transaction Table
def printTable():

    # create a connection and a cursor
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()

    # select all the records from Transactions table
    c.execute("SELECT * FROM Transactions")
    rows = c.fetchall()

    # create a list of rows
    table = []
    for row in rows:
        # get the values of columns
        trans_id = row[0]
        trans_date = row[1]
        trans_time = row[2]
        payee_payer_name = row[3]
        notes = row[4]
        trans_type = row[5]
        trans_amt = row[6]
        balance = row[7]

        # set the color of the row based on TransactionType and Balance
        if trans_type == 0:
            trans_date = colored(trans_date, "red")
            trans_time = colored(trans_time, "red")
            payee_payer_name = colored(payee_payer_name, "red")
            notes = colored(notes, "red")
            trans_type = colored("Expense", "red")
            trans_amt = colored(trans_amt, "red")
        else:
            trans_date = colored(trans_date, "green")
            trans_time = colored(trans_time, "green")
            payee_payer_name = colored(payee_payer_name, "green")
            notes = colored(notes, "green")
            trans_type = colored("Income", "green")
            trans_amt = colored(trans_amt, "green")

        if balance < 0:
            balance = colored(balance, "red")
        else:
            balance = colored(balance, "white")

        # add the row to the table
        table.append(
            [
                trans_id,
                trans_date,
                trans_time,
                payee_payer_name,
                notes,
                trans_type,
                trans_amt,
                balance,
            ]
        )

    # print the table with borders
    print(
        "\n"
        + tabulate(
            table,
            headers=[
                "ID",
                "Date",
                "Time",
                "Payee/Payer Name",
                "Notes",
                "Type",
                "Amount",
                "Balance",
            ],
            tablefmt="simple",
        )
    )

    # close the connection
    conn.close()
