import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import csv
import os
from datetime import datetime




def load_and_display_budget():
    try:
        with open('budget.txt', 'r') as f:
            budget = f.read()
            budget_display_var.set(f"Current Budget: ${budget}")
    except FileNotFoundError:
        budget_display_var.set("Current Budget: Not set")


def set_budget():
    budget = budget_var.get()
    with open('budget.txt', 'w') as f:
        f.write(budget)
    messagebox.showinfo("Budget", f"Budget set to: ${budget}")


def add_expense():
    name = name_var.get()
    cost = cost_var.get()
    date = date_var.get()
    category = category_var.get()

    # Define the file name
    csv_file = 'expenses.csv'

    # Check if file exists, if not create it and add header
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Cost', 'Date', 'Category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write header only if the file is newly created

        # Write the expense data
        writer.writerow({'Name': name, 'Cost': cost, 'Date': date, 'Category': category})

    # Confirmation message to the console (for debugging)
    print(f"Expense added: {name}, {cost}, {date}, {category}")

    # Reset the fields for next entry
    name_entry.delete(0, tk.END)
    cost_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    category_entry.set('')  # Reset combobox


def view_summary():
    try:
        with open('expenses.csv', mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            total_expense = 0
            category_expenses = {}

            for row in reader:
                # Sum total expenses
                total_expense += float(row['Cost'])

                # Sum expenses by category
                if row['Category'] in category_expenses:
                    category_expenses[row['Category']] += float(row['Cost'])
                else:
                    category_expenses[row['Category']] = float(row['Cost'])

            # Prepare the summary message
            summary_message = f"Total Expenses: ${total_expense:.2f}\n\nExpenses by Category:\n"
            for category, amount in category_expenses.items():
                summary_message += f"{category}: ${amount:.2f}\n"

            # Display the summary message
            messagebox.showinfo("Summary of Expenses", summary_message)
    except FileNotFoundError:
        messagebox.showerror("Error", "Expenses file not found. Please add an expense first.")


# Creating main window
root = tk.Tk()
root.title("Monthly Budgeting Tool")

# Creating StringVars to hold input data
name_var = tk.StringVar()
cost_var = tk.StringVar()
date_var = tk.StringVar()
category_var = tk.StringVar()
current_date = datetime.now().strftime("%Y-%m-%d")
date_var.set(current_date)

# Creating an entry for the budget
budget_var = tk.StringVar()
tk.Label(root, text="Set Budget:").grid(row=6, column=0)
budget_entry = tk.Entry(root, textvariable=budget_var)
budget_entry.grid(row=6, column=1)

# Creating layout
tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Cost").grid(row=1, column=0)
tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=2, column=0)
tk.Label(root, text="Category").grid(row=3, column=0)

name_entry = tk.Entry(root, textvariable=name_var)
cost_entry = tk.Entry(root, textvariable=cost_var)
date_entry = tk.Entry(root, textvariable=date_var)
category_entry = ttk.Combobox(root, textvariable=category_var)
view_summary_btn = tk.Button(root, text="View Summary", command=view_summary)

name_entry.grid(row=0, column=1)
cost_entry.grid(row=1, column=1)
date_entry.grid(row=2, column=1)
category_entry.grid(row=3, column=1)

category_entry['values'] = ('Food', 'Transport', 'Housing', 'Entertainment', 'Other')

# Submit button
submit_btn = tk.Button(root, text="Add Expense", command=add_expense)
submit_btn.grid(row=4, column=0, columnspan=2)
view_summary_btn.grid(row=5, column=0, columnspan=2, pady=10)

# Button to set the budget
set_budget_btn = tk.Button(root, text="Set Budget", command=set_budget)
set_budget_btn.grid(row=7, column=0, columnspan=2)

# Variable and label for displaying the current budget
budget_display_var = tk.StringVar()
load_and_display_budget()  # Call this function to load and display the budget at startup
budget_display_label = tk.Label(root, textvariable=budget_display_var)
budget_display_label.grid(row=8, column=0, columnspan=2)

root.mainloop()