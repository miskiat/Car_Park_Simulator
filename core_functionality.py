import csv
import os
from contextlib import nullcontext
from datetime import datetime



def create_csv_file_if_not_exists(filename='parking_records.csv'):
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as file:
                fieldnames =  ['ticket_number', 'car_reg_number',"parking_space_id",'parking_fee', 'entry_time', 'exit_time']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                

def read_csv(filename='parking_records.csv'):
    
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"File '{filename}' not found. Creating a new one.")
        return list([])

def initialize():
    FILENAME = "parking_records.csv"
    create_csv_file_if_not_exists()
    parking_records = read_csv()
    return Car_Park(parking_records)



def save_to_csv(filename, records):
    with open(filename, 'w', newline='') as file:
        fieldnames = ['ticket_number', 'car_reg_number',"parking_space_id", 'parking_fee', 'entry_time', 'exit_time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def create_ticket(reg_number, parking_space_id):
    ticket = Ticket(reg_number, parking_space_id)
    return ticket

class Car_Park:
    def __init__(self, parking_records=[]):
        self.parking_records = parking_records
        self.total_parking_space = 6
        self.minute_rate = 0.033
       

    def create_parking_space_id(self):
        if(self.can_car_park()==True):
            cars = self.parked_cars()
            parking_space_number = len(cars)+1
            parking_space_id = f"space-{parking_space_number}"
            return parking_space_id
        else:
            return ""

    

    def parked_cars(self):
        cars_parked = []
        for ticket in self.parking_records:
              if(ticket["exit_time"] == ""):
                cars_parked.append(ticket)
        return cars_parked

    def can_car_park(self):
         available_space = self.total_parking_space - len(self.parked_cars())
         if available_space == 0:
                print( f"No Parking Space left, Available Parking Space: {available_space}")
                return False
         else:
            return True
            
    def available_parking_space(self): 
        available_space = self.total_parking_space - len(self.parked_cars())
        return f"Available Parking Space: {available_space}"
    

    def add_car_to_park(self, ticket):
        self.parking_records.append(ticket.get_ticket_data())
        result = f"Ticket Number: {ticket.ticket_number}\nCar Registration Number: {ticket.car_reg_number}\n" \
               f"Parking Space Id: {ticket.parking_space_id}\n" \
               f"Entry Time: {ticket.entry_time}\nExit Time: {ticket.exit_time}\n" \
               f"Parking Fee: {ticket.parking_fee}"
        return result
        

    def query_park(self, ticket_number):
        ticket = ""
        for t in self.parking_records:
          if(t["ticket_number"] == ticket_number):
            ticket=t
        if(not ticket):
        #    print("Ticket Not registered")  
           return "Ticket Not registered"
        
        result= f"Ticket Number: {ticket['ticket_number']}\nCar Registration Number: {ticket['car_reg_number']}\n" \
               f"Parking Space Id: {ticket['parking_space_id']}\n" \
               f"Entry Time: {ticket['entry_time']}\nExit Time: {ticket['exit_time']}\n" \
               f"Parking Fee: {ticket['parking_fee']}"
        
        print("Here is the ticket you requested for")    
        # print(result)
        return  result


    def calculate_fee(self,ticket):
        exit_time = datetime.now()
        duration= exit_time - datetime.strptime(ticket["entry_time"], '%Y-%m-%d %H:%M:%S.%f')
        minute_used = round(duration.total_seconds() / 60)
        # print(minute_used)
        fees = round(minute_used *self.minute_rate,2)
        print(f"Due fees: £{fees}")  
        return {"fees": fees,"exit_time": exit_time}
       


    def exit_car_park(self, ticket_number):
        ticket = ""
        for t in self.parked_cars():
          
          if(t['ticket_number'] == ticket_number):
            ticket=t
        if(ticket == ""):
           print("No Available parked car with Ticket Number")  
           return "No Available parked car with Ticket Number"
        else:
           ticket_update_data = self.calculate_fee(ticket)
           for record_ticket in self.parking_records:
              if(record_ticket["ticket_number"] == ticket_number):
                record_ticket["exit_time"] = ticket_update_data["exit_time"] 
                record_ticket["parking_fee"] = ticket_update_data["fees"]
           save_to_csv("parking_records.csv",self.parking_records)
           return ticket_update_data



class Ticket:
    def __init__(self, car_reg_number, parking_id):
        self.car_reg_number = car_reg_number
        self.entry_time = datetime.now()
        self.exit_time = ""
        self.parking_fee = ""
        self.ticket_number = self.generate_ticket_number()
        self.parking_space_id = parking_id

    def generate_ticket_number(self):
        epoch_time = int(self.entry_time.timestamp())
        ticket_number = f"{epoch_time}_{self.car_reg_number}"
        return ticket_number

    def get_ticket_data(self):
        return { "car_reg_number":self.car_reg_number,
                 "entry_time":str(self.entry_time),
                 "exit_time":self.exit_time,
                 "parking_fee":self.parking_fee,
                 "ticket_number":self.ticket_number,
                 "parking_space_id":self.parking_space_id
            
        }
