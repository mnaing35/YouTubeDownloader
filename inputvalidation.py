# For unexpected input
def int_only(userinput):
    try:
        userinput = int(userinput)
    except:
        None
    return userinput

# Number Validation
def in_vali(upbound, userinput):
    userinput = int_only(userinput)
    while userinput not in range(1, upbound + 1):
        print("Invalid Operation!")
        userinput = int_only(input(f"Enter the number only from 1 to {upbound} => "))
    return userinput

# Yes/No Validation
def yesno(state):
    while state not in ('y', 'Y', 'yes', 'Yes', 'n', 'N', 'no', 'No'):
        state = input("Enter only y/n => ")
    return 'y' if state in ('y', 'Y', 'yes', 'Yes') else 'n'