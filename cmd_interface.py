import core_functionality




def initialize():

    car_park=core_functionality.initialize()

    while True:
        
        display_menu()
        choice = user_choice()
        if choice == "1":
            # Handle option 1: Enter the car park
            print("Entering the car park")
            if(car_park.can_car_park() == True):
                parking_space_id = car_park.create_parking_space_id()
                ticket = enter_car_park(parking_space_id)
                if(ticket):
                    print(car_park.add_car_to_park(ticket))   
                    core_functionality.save_to_csv("parking_records.csv", car_park.parking_records)  
            print("======================================================")
          
        elif choice == "2":
            # Handle option 2: Exit the car park
            ticket_number = input("Ticket Number: ")
            print("Exiting the car park")
            print("======================================================")
            if(ticket_number):
                car_park.exit_car_park(ticket_number)
            else:
                print("Invalid ticket number")
            print("======================================================")
        elif choice == "3":
            # Handle option 2: View available parking spaces
            print("======================================================")
            print(car_park.available_parking_space())
            print("=====================================================")
        elif choice == "4":
            # Handle option 3: Query parking record by ticket number
           
            ticket_number = input("Ticket Number: ")
            print("======================================================")
            if(ticket_number):
                print(car_park.query_park(ticket_number))
            else:
                print("Invalid ticket number")
            print("======================================================")
        elif choice == "5":
            # Handle option 4: Quit
            print("======================================================")
            print("Goodbye! Safe Trip")
            print("======================================================")
            core_functionality.save_to_csv('parking_records.csv',car_park.parking_records )
            break
        else:
            print("======================================================")
            print("Invalid choice. Please select a valid option.")
            print("======================================================")

    

def display_menu():
    print("\nThese are the options available, choose anyone below\n")
    print("A. Type 1 to Enter the car park (Hourly rate: $2)")
    print("B. Type 2 to Exit the car park")
    print("C. Type 3 to View available parking space")
    print("D. Type 4 to Query parking record by ticket number")
    print("E. Type 5 to Quit")

def user_choice():
    choice = input("Enter your choosen number: ")
    return (choice)

def enter_car_park(parking_space_id):
    reg_number = input("Car Registration Number: ")
    print("======================================================")
    
    if(reg_number==""):
        print("Invalid Registration Number")
        return
    
    print("creating ticket")
    ticket = core_functionality.create_ticket(reg_number, parking_space_id)
    return ticket
  
        

initialize()    


