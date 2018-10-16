import time
import datetime
import math

def getDate(event_time):
  '''
  Convert string date object (2017-01-06T12:45:52.041Z) to datetime object 
  '''
  return datetime.datetime.strptime(event_time.replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f")

class Event(object):
    '''
    Read each event with attributes 'key' and 'event_time'
    '''
    def __init__(self, event):        
        self.key = event.get('key')
        self.event_time = getDate(event.get('event_time'))


class Image(Event):
  '''
  Read Image event with attributes {key,event_time,customer_id,camera_make,camera_model} 
  '''
  def __init__(self, image):
    super(Image, self).__init__(image)
    self.customer_id = image.get('customer_id')
    self.camera_make = image.get('camera_make', '')
    self.camera_model = image.get('camera_model', '')

  
class SiteVisit(Event):
  '''
  Read Site Visit event with attributes {key,event_time,customer_id,tags}
  '''
  def __init__(self, sitevisit):
    Event.__init__(self, sitevisit)
    self.customer_id = sitevisit.get('customer_id')
    self.tags = sitevisit.get('tags', [])


class Order(Event):
  '''
  Read Order event with attributes {key,event_time,customer_id,total_amount}
  '''
  def __init__(self, order):
    Event.__init__(self, order)
    self.customer_id = order.get('customer_id')    
    self.total_amount = float(order.get('total_amount').split(' ')[0])
 

class Customer(Event):
  '''
  Read Customer event with attributes {key,event_time,customer_id,last_name,adr_city,adr_state}
  
  Set site_visits,total_amount,average_ltv and recent customer interaction in customer database till given day

  '''
  def __init__(self, customer):
    Event.__init__(self, customer)
    self.customer_id = customer.get('customer_id', None) or self.key # self.key for new customers
    self.last_name = customer.get('last_name', '')
    self.adr_city = customer.get('adr_city', '')
    self.adr_state = customer.get('adr_state', '')
    self.site_visits = customer.get('site_visits', 0)
    self.total_amount = customer.get('total_amount', 0.0)
    self.average_ltv = customer.get('average_ltv', 0.0)
    self.latest_time = customer.get('latest_time', None)
    self.earliest_time = self.event_time

  def increaseSiteVisit(self):
    """
    Increments the customer's site visits by 1
    :return: 
    """    
    self.site_visits += 1

  def updateOrderAmount(self, order, prev_orders):
    '''
    Update current order amount, update total order and add new order amout to total order
    '''
    order_id = order.key
    if order_id in prev_orders and order.event_time >= prev_orders[order_id].event_time:
      self.total_amount -= prev_orders[order_id].total_amount
      self.total_amount += order.total_amount
    elif order_id not in prev_orders:
      self.total_amount += order.total_amount

  def updateCustomerAttr(self, customer_event):
    '''
    Update customer attributes (Last name, Address, State)
    '''
    event_time = getDate(customer_event.get('event_time'))
    self.earliest_time = min(event_time, self.earliest_time)
    if (not self.latest_time) or (event_time >= self.latest_time):
      self.latest_time = event_time
      self.last_name = customer_event.get('last_name', '')
      self.adr_city = customer_event.get('adr_city', '')
      self.adr_state = customer_event.get('adr_state', '')

  def updateCustAvgLTV(self, latest_time):
    '''
    Update Customer LTV with latest available record in database
    '''
    # mktime to make available date to UTC format for week calculation
    
    life_span = 10
    
    end_time = time.mktime(latest_time.timetuple())
    
    start_time = time.mktime(self.earliest_time.timetuple())
    
    # Round up the week calculation result to calculate the first week customer LTV
    weeks = math.ceil(float(int(end_time - start_time) / (3600 * 24 * 7)))
    
    spend_per_visit = (self.total_amount / self.site_visits)
    visit_per_week = (self.site_visits / weeks)
    
    avg_cust_val =  spend_per_visit * visit_per_week
    
    self.average_ltv = round(52 * avg_cust_val * life_span,3)



