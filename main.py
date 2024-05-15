import inputvalidation as iv
import crud
import os

print("Welcome to the Video Management System")
print("!Enter the number in the menu to perform various operations!")
print("!You have to manually install pandas package before running this program!")
print("---------------------------------------------------------")
print("1. Add a New Video\n2. View Video List\n3. Search for a Video\n4. Update Video Information\n5. Delete a Video\n6. Close the Program")
print("---------------------------------------------------------")

os.makedirs("./videos/", exist_ok=True)
# Update json and csv
crud.list_json_csv('./videos/')

# Input Validation
menu_input = iv.in_vali(6, input("Enter your choice (1-6) => "))

# For Repeated Operations
while menu_input != 6:

    if menu_input == 1:
        crud.addvideo()
    if menu_input == 2:
        crud.viewrecord()
    if menu_input == 3:
        crud.searchvideo()
    if menu_input == 4:
        crud.updatevideo()
    if menu_input == 5:
        crud.deletevideo()

    print("Going back to the Main Menu...")
    print("1. Add a New Video\n2. View Video List\n3. Search for a Video\n4. Update Video Information\n5. Delete a Video\n6. Close the Program")
    menu_input = iv.in_vali(6, input("Enter your choice (1-6) => "))

print("Program Closed!!\nThank You For Using the Program!")