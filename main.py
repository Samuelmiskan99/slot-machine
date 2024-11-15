import random
import tkinter as tk
from tkinter import messagebox

# Slot Machine Settings
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "💎": 2,
    "🍒": 4,
    "🍋": 6,
    "🔔": 8
}

symbol_value = {
    "💎": 5,
    "🍒": 4,
    "🍋": 3,
    "🔔": 2
}


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)
    
    columns = []
    for _ in range(cols):
        column = random.sample(all_symbols, rows)
        columns.append(column)
    return columns


class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine")
        self.balance = 0  # Balance initialized to 0

        # Labels for balance and betting info
        self.balance_label = tk.Label(root, text=f"Balance: ${self.balance}", font=("Helvetica", 16))
        self.balance_label.pack(pady=10)

        # Deposit section
        self.deposit_button = tk.Button(root, text="Deposit", font=("Helvetica", 12), command=self.deposit)
        self.deposit_button.pack(pady=5)

        # Bet section
        self.bet_label = tk.Label(root, text="Bet per line:", font=("Helvetica", 12))
        self.bet_label.pack()
        self.bet_entry = tk.Entry(root)
        self.bet_entry.pack()

        # Lines section
        self.lines_label = tk.Label(root, text="Number of lines (1-3):", font=("Helvetica", 12))
        self.lines_label.pack()
        self.lines_entry = tk.Entry(root)
        self.lines_entry.pack()

        # Slot machine display grid
        self.slot_frame = tk.Frame(root)
        self.slot_frame.pack(pady=20)
        self.slot_labels = [[tk.Label(self.slot_frame, text="❔", font=("Helvetica", 24), width=4) for _ in range(COLS)] for _ in range(ROWS)]
        for i, row in enumerate(self.slot_labels):
            for j, label in enumerate(row):
                label.grid(row=i, column=j, padx=5, pady=5)

        # Spin button
        self.spin_button = tk.Button(root, text="Spin", font=("Helvetica", 14), command=self.spin)
        self.spin_button.pack(pady=10)

    def deposit(self):
        # Deposit function to add balance
        def deposit_amount():
            try:
                deposit_value = int(self.deposit_entry.get())
                if deposit_value > 0:
                    self.balance += deposit_value
                    self.balance_label.config(text=f"Balance: ${self.balance}")
                    self.deposit_window.destroy()
                else:
                    messagebox.showerror("Invalid Deposit", "Deposit must be greater than 0.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")
        
        # Create deposit window
        self.deposit_window = tk.Toplevel(self.root)
        self.deposit_window.title("Deposit")
        
        self.deposit_label = tk.Label(self.deposit_window, text="Enter deposit amount:", font=("Helvetica", 12))
        self.deposit_label.pack(pady=10)
        
        self.deposit_entry = tk.Entry(self.deposit_window)
        self.deposit_entry.pack(pady=5)

        self.deposit_button = tk.Button(self.deposit_window, text="Deposit", font=("Helvetica", 12), command=deposit_amount)
        self.deposit_button.pack(pady=5)

    def spin(self):
        try:
            bet = int(self.bet_entry.get())
            if bet < MIN_BET or bet > MAX_BET:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Bet", f"Please enter a bet between ${MIN_BET} and ${MAX_BET}.")
            return

        try:
            lines = int(self.lines_entry.get())
            if lines < 1 or lines > MAX_LINES:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Lines", f"Please enter a valid number of lines (1-{MAX_LINES}).")
            return

        total_bet = bet * lines
        if total_bet > self.balance:
            messagebox.showerror("Insufficient Funds", "Not enough balance to place bet.")
            return

        self.balance -= total_bet
        self.balance_label.config(text=f"Balance: ${self.balance}")

        # Get slot result and display it
        columns = get_slot_machine_spin(ROWS, COLS, symbol_count)
        for i in range(ROWS):
            for j in range(COLS):
                self.slot_labels[i][j].config(text=columns[j][i])

        # Calculate winnings
        winnings, winning_lines = self.check_winnings(columns, lines, bet)
        self.balance += winnings
        self.balance_label.config(text=f"Balance: ${self.balance}")

        if winnings > 0:
            messagebox.showinfo("Win!", f"You won ${winnings} on lines {', '.join(map(str, winning_lines))}!")
        else:
            messagebox.showinfo("No Win", "Better luck next time!")

    def check_winnings(self, columns, lines, bet):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            if all(column[line] == symbol for column in columns):
                winnings += symbol_value[symbol] * bet
                winning_lines.append(line + 1)
        return winnings, winning_lines


# Main application execution
root = tk.Tk()
app = SlotMachineApp(root)
root.mainloop()
