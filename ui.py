import db
import datetime
from objects import Ticket




def display_menu():
    print("")
    print("Welcome to the Vecta Corp Help Desk Application (User)")
    print("")
    print("COMMAND MENU")
    print("-" * 110)
    print("view - View all open tickets")
    print("issue - View issue for the ticket")
    print("add- Add a ticket")
    print("update - Update a ticket's status")
    print("exit - Exit the program")
    print("-" * 110)
    
def view_tickets():
    print("")
    print("VECTA CORP HELP DESK (CURRENT OPEN TICKETS)")
    print("-" * 110)
    line_format = ("{:5s} {:15s} {:25s} {:15s} {:15s} {:15s} {:15s}")
    print( line_format.format("ID", "Name", "Email", "Date", "Employee", "Solution", "Status"))
    print("-" * 110)
    tickets = db.get_open_ticket()
    for ticket in tickets:
        print(line_format.format(str(ticket.ticketid), 
                                 ticket.customername, 
                                 ticket.customeremail, 
                                 str(ticket.submitteddate), 
                                 ticket.employee,
                                 ticket.solution,
                                 ticket.status))
    print("-" * 110)
    
def view_ticket_issue():
    ticketid = input("Ticket ID: ")
    print("")
    print("VECTA CORP HELP DESK (CURRENT OPEN TICKETS)")
    print("-" * 110)
    issue = db.get_ticket_issue(ticketid)
    print(issue)
    print("-" * 110)
    
def add_ticket():
    customername    = input("Customer Name: ")
    customeremail   = input("Customer Email: ")
    submitteddate   = datetime.date.today()
    print ("")
    print("VECTA CORP HEPL DESK EMPLOYEES")
    print("-" * 95)
    line_format="{:5s} {:15s} {:5s}"
    print(line_format.format("ID", "Name", "Role"))
    print("-" * 95)
    employees =db.get_employees()
    for employee in employees:
        print(line_format.format(str(employee[0]),employee[1], employee[2]))
    print("-" * 95)
    employee        = int(input("Employee ID: "))
    solution        = int(input("Solution ID (1 = vProspect, 2 = vConvert, 3= vRetain): "))
    status          = 1
    issue           = input("Isuue: ")
    
    ticket = Ticket(customername=customername, 
                    customeremail=customeremail,
                    submitteddate=submitteddate,
                    employee=employee,
                    solution=solution,
                    status=status,
                    issue= issue)
    db.add_ticket(ticket)
    print("")
    print("The new ticket was added to the database successfully. \n")
    
def update_ticket():
    ticketid = input("Ticket ID: ")
    choice = input("Are you sure you want to update this ticket? (y/n):")
    if choice == "y":
        statusid = int(input("Enter new status (1 = Open, 2=In Progress, 3=Closed): "))
        db.update_ticket(statusid, ticketid)
        print("The ticket was successfully updated. \n")
    else:
        print("The ticket was NOT updated. \n")
    
def main():
    db.connect()
    
    while True:
        print("VECTA CORP HELP DESK USER LOG IN")
        print("-" * 110)
        username = input("Username: ")
        password = input("Password: ")
        if db.login(username,password):
            break
        else:
            print("\nYour credentials are invalid. Please try again. \n")
        
    display_menu()
    
    while True:
        command = input("Enter command: ")
        if command == "view":
            view_tickets()
        elif command == "issue":
            view_ticket_issue()
        elif command == "add":
            add_ticket()
        elif command == "update":
            update_ticket()
        elif command == "exit":
            break
        else:
            print("Not a valid command. Please try again.")
            display_menu()
            
    db.close()
    print("The program has been terminated.")
    
    
if __name__ == "__main__":
    main()
