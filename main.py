import random

MAX_LINES = 3 #Global constant
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = { #This is a dictionary of how many possible symbols in each reel / column
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = { #This is a dictionary of each symbol with the respective multiplier
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

#In all these functions, we work on the slot machine with the rows and columns switched

def deposit():
    """Return the amount that the user will bet with."""
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount) #Since by default, the user input was a string
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a positive number.")
    return amount

def get_number_of_lines():
    """Returns the number of lines that will be betted on."""
    while True:
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + "): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a positive number.")
    return lines

def get_bet():
    """Return the user's bet."""
    while True:
        bet = input("Enter the bet that you would like to place on each line (" + str(MIN_BET)+ "-" + str(MAX_BET) + ")")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Enter a positive number")
    return bet

def get_slot_machine_spin(rows, cols, symbols):
    """Return all the columns after spin, using symbols as a dictionary."""
    all_symbols = [] #Creating a list of all symbols for each reel / column
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:] #Creates a copy of all_symbols by slice
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value) 
            column.append(value)
        columns.append(column)
    return columns

def print_slot_machine(columns):
    """Transpose columns for user visualisation."""
    for row in range(len(columns[0])): #Assume we have at least one row in the slot machine
        for i, column in enumerate(columns):
            if i != len(columns) - 1:   
                print(column[row], end = " | ") #pipe operator to separate each item
            else:
                print(column[row], end = "")
        
        print() #Separate each row

def spin(balance):
    """Returns the profit/loss from spinning."""
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough to bet that amount. Your current balance is {balance}.")
        else:
            break
    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines) #Splat / unpack operator
    return winnings - total_bet

def check_winnings(columns, lines, bet, values):
    """Return winnings and respective lines in the bet."""
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line] #This is the first symbol on the first column
        for column in columns:
            symbol_to_check = column[line] #Going through each row 
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def main():
    """Put the game together and plays it."""
    balance = deposit()
    while True:
        print(f"Current balance is: ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)
        
    print(f"You left with ${balance}")

main()