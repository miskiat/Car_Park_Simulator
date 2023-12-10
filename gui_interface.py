import tkinter as tk
from tkinter import messagebox
import core_functionality


class CPGUI:
    def __init__(self, root):
        self.car_park = core_functionality.initialize()
        self.root = root
        self.root.title("Car Park")
        self.task=""


        #label
        self.input_label = tk.Label(root, text="Enter Ticket Number",fg="red")
        self.input_label.grid(row=0, column=3)
        self.input_label.rowconfigure(0,weight=1)
        self.input_label.grid_remove()

        # Input for car plate number
        self.car_plate_entry = tk.Entry(root, width=30)
        self.car_plate_entry.grid(row=1, column=3, padx=1, pady=1, sticky=tk.N)
        self.car_plate_entry.rowconfigure(0,weight=1)
        self.car_plate_entry.grid_remove()


        #continue button
        self.continue_button = tk.Button(root, text="continue", command=self.use_task, bg="#4CAF50", fg="red", padx=10, pady=5, relief=tk.GROOVE)
        self.continue_button.grid(row=2, column=3, sticky=tk.N)
        self.continue_button.rowconfigure(0,weight=1)
        
        self.continue_button.grid_remove()



        # enter car park Button
        self.enter_button = tk.Button(root, text="Enter Car Park", command=lambda:self.set_task("enter_park"), bg="#4CAF50", fg="red", padx=10, pady=5, relief=tk.GROOVE)
        self.enter_button.grid(row=0, column=0, padx=10, pady=10)

       

        # available parking spaces Button
        self.available_spaces_button = tk.Button(root, text="Available Spaces", command=self.display_available_spaces, bg="#3498db", fg="red", padx=10, pady=5, relief=tk.GROOVE)
        self.available_spaces_button.grid(row=2, column=0, padx=10, pady=10)

        # querying parking records by car plate number
        self.query_by_plate_button = tk.Button(root, text="Query by Ticket", command=lambda:self.set_task("query_ticket"), bg="#8e44ad", fg="red", padx=10, pady=5, relief=tk.GROOVE)
        self.query_by_plate_button.grid(row=1, column=0, padx=10, pady=10)

         # exiting car park Button
        self.exit_button = tk.Button(root, text="Exit Car Park", command=lambda:self.set_task("exit_park"), bg="#FF5733", fg="red", padx=10, pady=5, relief=tk.GROOVE)
        self.exit_button.grid(row=3, column=0, padx=10, pady=10)

        # quit button
        self.quit_button = tk.Button(root, text="Quit", command=self.quit, bg="#FF5733", fg="red", padx=10, pady=5, relief=tk.GROOVE)
        self.quit_button.grid(row=4, column=0, padx=10, pady=10)

        # Display area
        self.display_area = tk.Text(root, height=10, width=50)
        self.display_area.grid(row=3, column=3, rowspan=6, padx=10, pady=10, sticky=tk.N)
 
    def use_task(self):
        if(self.task=='enter_park'):
            self.enter_car_park()
        elif(self.task == 'query_ticket'):
                self.query_by_ticket_number()
        elif(self.task == "exit_park"):
            self.exit_car_park()
      
    def set_task(self, task_name):
       self.task = task_name
       self.hide_fields()
       self.show_input_field(task_name)
       self.display_area.delete(1.0, tk.END)

       
    def show_input_field(self, task_name):
        self.car_plate_entry.grid()
        self.car_plate_entry.delete(0, 'end')

        self.input_label.grid()
        self.continue_button.grid()
        if(task_name=='enter_park'):
            self.input_label.config(text="Enter Car Registration Number")
        else:
            self.input_label.config(text="Enter Ticket Number")
            
        

    def hide_fields(self):
        self.car_plate_entry.grid_remove()
        self.input_label.grid_remove() 
        self.continue_button.grid_remove()
        self.display_area['state'] = 'normal'


        

    def enter_car_park(self):
        # self.display_area.delete(1.0, tk.END)
        if(self.car_park.can_car_park() == True):
            parking_space_id = self.car_park.create_parking_space_id()
            reg_number = self.car_plate_entry.get()
            if(reg_number==""):
                messagebox.showerror('Error', "Invalid Registration Number")
                return
            ticket = core_functionality.create_ticket(reg_number,parking_space_id)
            result = self.car_park.add_car_to_park(ticket)
            # self.update_display_area()
            self.update_display_screen(result)
            core_functionality.save_to_csv("parking_records.csv", self.car_park.parking_records)
        else:
            messagebox.showinfo("Result", "No Parking Space left, Available Parking Space: 0")

        self.hide_fields()
        self.display_area['state'] = 'disabled'



    def exit_car_park(self):
        ticket_number = self.car_plate_entry.get()
        self.hide_fields()
        if(ticket_number==""):
            messagebox.showerror('Error', "Invalid ticket number")
            return
        result = self.car_park.exit_car_park(ticket_number)
        if(result == 'No Available parked car with Ticket Number') :
            messagebox.showerror('Error', result)
        else:
            messagebox.showinfo('Successful Exit', f"Fess to be paid:£{result['fees']}")
        # self.update_display_area()
        # self.update_display_screen()

    def display_available_spaces(self):
        self.display_area['state'] = 'normal'
        self.display_area.delete(1.0, tk.END)
        self.hide_fields()
        available_spaces = self.car_park.available_parking_space()
        messagebox.showinfo("Car Park Spaces", f"Car Park Spaces\n {available_spaces}")

    def query_by_ticket_number(self):
        # self.display_area.delete(1.0, tk.END)
    
        ticket_number = self.car_plate_entry.get()
        self.hide_fields()
        if(ticket_number==""):
            messagebox.showerror('Error', "Invalid ticket number")
            return
        result = self.car_park.query_park(ticket_number)
        if(result == "Ticket Not registered"):
            messagebox.showerror('Error', result)
        else:
            # messagebox.showinfo("Query Result", f"Parking Records for Car Plate Number {ticket_number}:\n{result}")
            self.update_display_screen(result)
        

    def quit(self):
        
        messagebox.showinfo('Success', "Goodbye! Safe Trip")
        core_functionality.save_to_csv("parking_records.csv", self.car_park.parking_records)
        self.root.destroy()

    # def update_display_area(self):
    #     self.display_area.delete(1.0, tk.END)  # Clear previous content
    #     records = self.car_park.query_parking_record('all')
    #     for record in records:
    #         self.display_area.insert(tk.END, str(record) + "\n")

    def update_display_screen(self, message):
         self.display_area.delete(1.0, tk.END)
         self.display_area.insert(tk.END, message + "\n")
         self.display_area['state'] = 'disabled'

if __name__ == "__main__":
    root = tk.Tk()
    app = CPGUI(root)
    root.mainloop()
