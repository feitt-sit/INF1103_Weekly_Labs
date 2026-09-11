inventory = 0
while True:
    user_input = input("Enter stock quantity:")
    if user_input.lower() == "quit":
        print("Exiting program.")
        break
    try:
        quantity = int(user_input)
        if quantity < 0:
            print("Error: Stock number cannot be negative")
            print("Please enter a valid stock quantity.")
            print("Current inventory: ", inventory)
            continue
        if quantity > 500:
            print("Alert: Stock number exceeds 500")
            print("Current inventory: ", inventory)
            continue
        inventory += quantity
        print(f"Current inventory: {inventory}")
    except ValueError:
        print("Error: Invalid input. Please enter a valid stock quantity.")
        continue



    