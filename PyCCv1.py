# PyCC ---- A user Friendly Bin Generator , CC generator , Validator 
# feel free to comment 
# Donate a cup of cofee at 1BbiJW33WsqW1gWGMjV9RVQEzuFMtz1Yoa BTC

import random
import requests
from datetime import datetime, timedelta
import csv

# Step 1: Input Validation
def is_valid_bin(bin_number):
    return bin_number.isdigit() and len(bin_number) in [6, 8]

# Step 2: Check BIN/IIN against binlist API
def check_bin(bin_number):
    response = requests.get(f"https://lookup.binlist.net/{bin_number}")
    return response.status_code == 200

# Step 3: Generate random 8 or 10 digits to make a 16-digit number
def generate_random_digits(length):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

# Step 4: Generate 1000 random combinations
def generate_combinations(bin_number, num_combinations=1000):
    combinations = []
    while len(combinations) < num_combinations:
        remaining_digits = 16 - len(bin_number)
        random_number = bin_number + generate_random_digits(remaining_digits)
        if random_number not in combinations:
            combinations.append(random_number)
    return combinations

# Step 5: Luhn Algorithm Check
def luhn_check(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10 == 0

def filter_valid_combinations(combinations):
    return [number for number in combinations if luhn_check(number)]

# Step 6: Generate expiration date and CVV
def generate_expiry_date_and_cvv():
    current_date = datetime.now()
    expiry_date = current_date + timedelta(days=3*365)
    expiry_date_str = expiry_date.strftime("%m|%y")
    cvv = '{:03d}'.format(random.randint(0, 999))
    return expiry_date_str, cvv

# Save valid combinations to CSV file
def save_to_csv(valid_combinations, filename='card_details.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Card Number", "Valid", "CVV"])
        for number, expiry_date, cvv in valid_combinations:
            writer.writerow([number, expiry_date, cvv])

def main():
    bin_number = input("Enter BIN/IIN number (6 or 8 digits): ")
    
    if not is_valid_bin(bin_number):
        print("Invalid BIN/IIN number. It should be 6 or 8 digits long.")
        return
    
    if not check_bin(bin_number):
        print("Invalid BIN/IIN number according to binlist API.")
        return
    
    combinations = generate_combinations(bin_number)
    valid_combinations = filter_valid_combinations(combinations)
    
    valid_card_details = []
    for number in valid_combinations:
        expiry_date, cvv = generate_expiry_date_and_cvv()
        valid_card_details.append((number, expiry_date, cvv))
        print(f"Card Number: {number}, Valid: {expiry_date}, CVV: {cvv}")
    
    save_to_csv(valid_card_details)
    print(f"\nValid card details saved to 'card_details.csv'")

if __name__ == "__main__":
    main()
