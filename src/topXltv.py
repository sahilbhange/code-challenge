import heapq
import events


event_type = {'customer':'CUSTOMER','site_visit':'SITE_VISIT','image':'IMAGE',  'order':'ORDER'}

def ingest(event, database):
  '''
  Insert/update event into the databse
  '''  
  # Check if the customer is new
  #customer_id = event.get('key')
  if event.get('customer_id'):

      customer_id = event.get('customer_id')
  else:
      customer_id = event.get('key')
  
  try:
      customer = database.customers.get(customer_id)
  except:
      customer = None

  # Insert new customer to database with customer_id

  if not customer:
    customer = events.Customer(event)
    database.insertCustomer(customer)

  # Add/update event in database
  
  if event['type'] == event_type['order']:
    order = events.Order(event)
    # Update existing order amount
    customer.updateOrderAmount(order, database.orders)
    database.insertOrder(order)
  elif event['type'] == event_type['image']:
    image = events.Image(event)
    database.insertImage(image)      
  elif event['type'] == event_type['site_visit']:
    site_visit = events.SiteVisit(event)
    customer.increaseSiteVisit()  
    # Update site visit count for existing customer
    database.insertSiteVisit(site_visit)      
  elif event['type'] == event_type['customer']:
    # Update existing customer attributes  
    customer.updateCustomerAttr(event)   
    database.insertCustomer(customer)
  else:
    e = events.Event(event)
    database.insertEvent(e)

  #  Update the latest customer interaction in database
  database.getMax(event)
  return database    

def topXSimpleLTVCustomers(x, database):
  '''
  heapq to keep the max LTV customer top  
  x - # top LTV customers
  '''
  heap = []
  for customer_id, customer in database.customers.items():
      customer.updateCustAvgLTV(database.latest_time)
      #print(customer_id,customer)
      heapq.heappush(heap, (-customer.average_ltv, customer))
  return [c for ltv, c in heap[:x]]





