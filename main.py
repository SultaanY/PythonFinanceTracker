import pandas as pd
import csv 
from datetime import datetime
from data_entry import get_amount, get_category,get_date, get_description
import matplotlib.pyplot as plt
plt.ion()




class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"
    
    @classmethod
    def initialize_csv(cls):
        try: 
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def add_entry(cls, date, amount, category,description):
        new_entry = {
            "date": date,
            "amount":amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")
    
    @classmethod
    def show_all(cls):
        dfall = pd.read_csv(cls.CSV_FILE)
        print(dfall.to_string())
        total_income = dfall[dfall["category"]== "Income"]["amount"].sum()
        total_expense = dfall[dfall["category"]=="Expense"]["amount"].sum()
        print("\nSummary: ")
        print(f"Total Income: £{total_income:.2f}")
        print(f"Total Expense: £{total_expense:.2f}")
        print(f"Net Savings: £{(total_income - total_expense):.2f}")


    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df['date'], format=CSV.FORMAT)
        start_date= datetime.strptime(start_date,CSV.FORMAT)
        end_date= datetime.strptime(end_date,CSV.FORMAT)
        # print(f"start:{start_date}")
        # print(f"end:{end_date}")

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
        # print(f"filtered_df:{filtered_df}")

        if filtered_df.empty:
            print('No transactions found in the give date range.')
        else:
            print(f"Transacations from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")

            print(filtered_df.to_string(index=False, formatters= {"date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df["category"]== "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()
            print("\nSummary: ")
            print(f"Total Income: £{total_income:.2f}")
            print(f"Total Expense: £{total_expense:.2f}")
            print(f"Net Savings: £{(total_income - total_expense):.2f}")
        
        return filtered_df
    



def add():
    CSV.initialize_csv()
    date= get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for todays date: ", allow_default= True) 

    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category,   description)

def plot_transactions(df):
    if df.empty:
        print("No data to plot.")
        return
    df.set_index("date", inplace=True)

    income_df = df[df["category"]== "Income"].resample("D").sum().reindex(df.index, fill_value = 0)

    expense_df = df[df["category"]== "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label= "Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label= "Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses")
    plt.legend()
    plt.grid(True)
    plt.show()

    

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Show all")
        print("4. Exit")
        
        choice = input("\nEnter your choice please: ")


        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df= CSV.get_transaction(start_date, end_date)
            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df)
        
        elif choice == "3":
            CSV.show_all()
                
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

if __name__ == "__main__":
    main()