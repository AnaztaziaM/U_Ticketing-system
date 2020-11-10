import sqlite3
from contextlib import closing
from objects import Ticket




conn = None

def connect():
    global conn
    if not conn:
        conn = sqlite3.connect("db/Helpdesk.SQLite.txt")
        conn.row_factory = sqlite3.Row
    
def close():
    if conn:
        conn.close()
        
        
def get_employees():
    query = "SELECT employees.employeeid, employees.name, roles.role FROM employees INNER JOIN roles ON roles.roleid =employees.roleid"
            
    with closing(conn.cursor()) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        
    return results
      
def make_ticket(row):
    return Ticket(row ["ticketid"],
                  row ["customername"],
                  row ["customeremail"],
                  row ["submitteddate"],
                  row ["employee"],
                  row ["solution"],
                  row ["status"],
                  row ["issue"])
    
def get_open_ticket():
    query =(" SELECT tickets.ticketid, status.status, solutions.solution, employees.name AS employee, "+
            "tickets.customername, tickets.customeremail, tickets.submitteddate, tickets.issue "+
            "FROM employees INNER JOIN "+
            "tickets ON employees.employeeid = tickets.employeeid INNER JOIN "+
            "solutions ON tickets.solutionid = solutions.solutionid INNER JOIN "+
            "status ON tickets.statusid = status.statusid "+
            "WHERE tickets.statusid = 1 OR tickets.statusid = 2")
    with closing(conn.cursor()) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        
    tickets = []
    for row in results:
        tickets.append (make_ticket(row))
    return tickets
        
    
def get_ticket_issue(ticketid):
    query = "SELECT tickets.issue FROM tickets WHERE ticketid=? "
    with closing(conn.cursor()) as cursor:
        cursor.execute(query, (ticketid,))
        results = cursor.fetchone()
    
    return results[0]
    
def add_ticket(ticket):
    sql = "INSERT INTO tickets (customername, customeremail, submitteddate, employeeid, solutionid, statusid, issue) VALUES (?, ?, ?, ?, ?, ?, ?)"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql, (ticket.customername, ticket.customeremail, ticket.submitteddate, ticket.employee, ticket.solution, ticket.status, ticket.issue))
        conn.commit()
        
def update_ticket(statusid, ticketid):
    sql = "UPDATE tickets SET statusid = ? WHERE ticketid = ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql, (statusid, ticketid))
        conn.commit()
    
def login (username, password):
    query = "SELECT COUNT(*) FROM employees WHERE username = ? AND password= ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(query, (username, password))
        results = cursor.fetchone()
    
    if results[0] > 0:
        return True
    else:
        return False
    
    
