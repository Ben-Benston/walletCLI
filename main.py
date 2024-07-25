import database
import os

expense = 0
income = 1


def cli():
    inp = input(
        """\nEnter command and the details : 
    1. Add Transaction - values(income/expense, 'Payee/Payer Name', 'Amount', 'Notes (Optional)')
    2. Delete transaction - values(ID)
    3. Calculate Total Income, Total Expenditure, Balance
    4. Update Balance
    5. Print Table
    6. Exit
    
    Input : """
    )
    if inp == "1":
        values = input(
            "Please input the values for adding the Transaction to the table : "
        )
        values = values.split(" ")
        if values[0] == "income":
            if len(values) >= 4:
                database.addTransaction(income, values[1], int(values[2]), values[3])
                os.system("cls")
                print(
                    database.colored(
                        (
                            "Transaction added of "
                            + values[2]
                            + " from "
                            + values[1]
                            + " as an income with notes "
                            + values[3]
                        ),
                        "yellow",
                        attrs=["blink", "bold"],
                    )
                )
            else:
                database.addTransaction(income, values[1], int(values[2]))
                os.system("cls")
                print(
                    database.colored(
                        (
                            "Transaction added of "
                            + values[2]
                            + " from "
                            + values[1]
                            + " as an income"
                        ),
                        "yellow",
                        attrs=["blink", "bold"],
                    )
                )
        elif values[0] == "expense":
            if len(values) >= 4:
                database.addTransaction(expense, values[1], int(values[2]), values[3])
                os.system("cls")
                print(
                    database.colored(
                        (
                            "Transaction added of "
                            + values[2]
                            + " to "
                            + values[1]
                            + " as an expense with notes "
                            + values[3]
                        ),
                        "yellow",
                        attrs=["blink", "bold"],
                    )
                )
            else:
                database.addTransaction(expense, values[1], int(values[2]))
                os.system("cls")
                print(
                    database.colored(
                        (
                            "Transaction added of "
                            + values[2]
                            + " to "
                            + values[1]
                            + " as an expense"
                        ),
                        "yellow",
                        attrs=["blink", "bold"],
                    )
                )
        cli()
    elif inp == "2":
        id = input("Please input the ID of the transaction you wish to delete : ")
        database.deleteTransaction(int(id))
        os.system("cls")
        print(
            database.colored(
                "Transaction bearing the ID " + id + " has been removed",
                "yellow",
                attrs=["blink", "bold"],
            )
        )
        cli()
    elif inp == "3":
        values = database.totalIncExp()
        os.system("cls")
        print(
            database.colored(
                (
                    "The total income is "
                    + str(values[0])
                    + ", the total expenditure is "
                    + str(values[1])
                    + ", the balance is "
                    + str(values[2])
                ),
                "yellow",
                attrs=["blink", "bold"],
            )
        )
        cli()
    elif inp == "4":
        os.system("cls")
        database.updateBalance()
        print(
            database.colored(
                "Balance Updated Successfully !!", "yellow", attrs=["blink", "bold"]
            )
        )
        cli()
    elif inp == "5":
        os.system("cls")
        database.printTable()
        cli()
    elif inp == "6":
        os.system("cls")
        os._exit(0)
    cli()


cli()
