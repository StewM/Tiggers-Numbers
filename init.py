from modules import db
import GenerateNumbers

# Set up tables and generate the number for today
db.create_numbers_table()
db.create_channel_table()
GenerateNumbers.Generate()
