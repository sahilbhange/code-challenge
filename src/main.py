'''
Execute main: python src/main.py input/events.txt output/events_output.txt 3
'''
import topXltv
import database
import json
import sys


# Check if the the correct number of arguments are given to script
if (len(sys.argv)!=4):
    sys.exit("Provide the apropriate number of parameters to scrpit like {python src/main.py input/events.txt output/events_output.txt 3}");

# Get the arguments from the command line

input_file = sys.argv[1]
out_file = sys.argv[2]
top_x = int(sys.argv[3])

# Create data table
D = database.Datatable()

# Ingest data

with open(input_file) as data_file:
    data = json.load(data_file)

for event in data:
  topXltv.ingest(event, D)

# Top customers (top_x = 4)
X = top_x

topX = topXltv.topXSimpleLTVCustomers(X, D)

# Print topX customer as well as write them to file
file = open(out_file,'w')  
for cust in topX:
    print("Customer ID --",cust.customer_id)
    print('Customer Last Name --', cust.last_name)
    print('Customer Total Site Visits --', cust.site_visits)
    print('Customer Total Spending --', cust.total_amount)
    print('Customer LTV --$',cust.average_ltv)
    print('Customer City --',cust.adr_city)
    print('Customer State --',cust.adr_state)
    file.write(cust.customer_id + ',' + cust.last_name + ',' + str(cust.site_visits) + ',' + str(cust.total_amount) + ',' + str(cust.average_ltv) + ',' + cust.adr_city + ',' + cust.adr_state +'\n')
    
    print("\n\n")
file.close() 

