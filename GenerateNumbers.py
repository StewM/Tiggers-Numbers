from datetime import date, datetime
from random import *
from modules import db

# initialize table
db.create_numbers_table()

# get numbers
num1 = randint(1, 99)
num2 = randint(1, 99)

# ensure they're not the same number
while num1 == num2:
    num2 = randint(1, 99)

# format the numbers into strings
if(num1 < 10):
    num1string = "0" + str(num1)
else:
    num1string = str(num1)

if(num2 < 10):
        num2string = "0" + str(num2)
else:
        num2string = str(num2)

# save numbers to db
db.save_numbers(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), num1string, num2string)
