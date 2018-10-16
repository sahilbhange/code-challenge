import datetime

def getDate(event_time):
  '''
  Convert string date object (2017-01-06T12:45:52.041Z) to datetime object 
  '''
  return datetime.datetime.strptime(event_time.replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f")

class Datatable():
  '''        
  Read Data from the file and prepares in-memory data for calcualations
  Input file format - JSON, thus dictionary to parse data        
  Class attributes:
      customers (dict): {"verb", "key", "event_time", "last_name":, "adr_city", "adr_state"} 
      site_visits (dict): {"verb", "key", "event_time", "customer_id", "tags": []}
      images (dict): {"verb", "key", "event_time", "customer_id", "camera_make", "camera_model"} 
      order (dict): {"verb", "key", "event_time", "customer_id", "total_amount"} 
      events (dict): {All events data for a customer}
  '''
  def __init__(self):
    self.utc_start = getDate("1970-01-01T00:00:00.000000")
    self.events = {}
    self.customers = {}
    self.site_visits = {}
    self.images = {}    
    self.orders = {}


  def getMax(self, event):
    '''
    Updates customer record with latest timedate 
    '''
    self.latest_time = max(self.utc_start, getDate(event.get('event_time')))

  def insertCustomer(self, customer):
    '''
    Insert new customer record to database
    '''
    self.customers[customer.customer_id] = customer

  def insertOrder(self, order):
    '''
    Insert new order record to database    
    '''
    self.orders[order.key] = order

  def insertSiteVisit(self, site_visit):
    '''
    Insert new site visit record to database
    '''
    site_visit_key = site_visit.key
    self.site_visits[site_visit_key] = site_visit

  def insertImage(self, image):
    '''
    Insert image record to database
    '''
    image_key = image.key 
    self.images[image_key] = image

  def insertEvent(self, event):
    '''
    Add new event to database based on event type
    '''
    self.events[event.key] = event
