import sqlite3
conn = sqlite3.connect('tigger.db')

# day, number1, number2
def create_numbers_table():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS numbers 
        (day datetime, number1 text, number2 text)''')
    conn.commit()
    return True

def save_numbers(day, number1, number2):
    #check to see if there's already numbers for today
    numbers = get_numbers(day)
    #if not, save the numbers
    if(len(numbers) == 0):
        c = conn.cursor()
        c.execute("INSERT INTO numbers VALUES (?, ?, ?)",
                (day, number1, number2))
        conn.commit()
    return True

def get_numbers(day):
    c = conn.cursor()
    c.execute("SELECT * FROM numbers WHERE day=?", (day,))
    numbers = c.fetchall()
    return numbers