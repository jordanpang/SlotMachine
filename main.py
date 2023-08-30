import random

MAX_LINES = 3 #Global constant
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = { #This is a dictionary of how many symbols in each reel / column
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

def deposit(): #This is the amount that the user will bet with
    while True: #Continue this loop until we break out, i.e. until we get a valid deposit input
        amount = input("What would you like to deposit? $")
        if amount.isdigit(): #This checks whether the input is a positive full number
            amount = int(amount) #By default, the user input is a string
            if amount > 0:
                break #Breaks out of loop
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a positive number.")
    return amount

def get_number_of_lines():
    while True: #Continue this loop until we break out, i.e. until we get a valid deposit input
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + "): ") #Concatenation for strings
        if lines.isdigit(): #This checks whether the input is a positive full number
            lines = int(lines) #By default, the user input is a string
            if 1 <= lines <= MAX_LINES:
                break #Breaks out of loop
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a positive number.")
    return lines

def get_bet():
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

def get_slot_machine_spin(rows, cols, symbols): #We are passing these parameters through to later on
    #We would like to put all the symbols into a dictionary as individual elements
    all_symbols = [] #Creating a list of all symbols for each reel / column
    for symbol, symbol_count in symbols.items(): # Looping through the dictionary, key is symbol and value is symbol_count. symbols is a new dictionary
        #.items gives you the keys and values associated to a dictionary
        for _ in range(symbol_count): # _ so you don't care about what you are iterating
            all_symbols.append(symbol)

    columns = [] # All the columns, i.e. a list of spins for each column
    for _ in range(cols): #_ is just a junk variable (unused)
        column = [] #The spin in each column
        current_symbols = all_symbols[:] #A copy of all_symbols. Slice
        for _ in range(rows):
            value = random.choice(current_symbols) #picks a random value from the list
            current_symbols.remove(value) 
            column.append(value)
        #Now you have a complete spin for a column
        columns.append(column)
    #Now you have spins for each column
    return columns

def print_slot_machine(columns):
    #Want to transpose
    for row in range(len(columns[0])): #Assuming we have at least one row in the slot machine
        for i, column in enumerate(columns): #Looking at each column in columns
            if i != len(columns) - 1:   
                print(column[row], end = " | ") #pipe operator to separate each item
            else:
                print(column[row], end = "")
        
        print() #Makes it go onto new line after we finish the row

def spin(balance): #The balance comes from the main function
    lines = get_number_of_lines()
    while True: #Checking if the bet is within the balance
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough to bet that amount. Your current balance is {balance}.")
        else:
            break
    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")
    #Okay so we have decided what they are betting
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count) #Spin the slot machine
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines) #splat / unpack operator
    return winnings - total_bet

def check_winnings(columns, lines, bet, values): #Want to check if the first symbol in each row is the same in each column with same row
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
    balance = deposit()
    while True:
        print(f"Current balance is: ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)
        
    print(f"You left with ${balance}")

main()