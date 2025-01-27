import json

class Product:
  product_id = ""
  name = ""
  description = ""
  price = 0
  stock = 0
  creation_date = "01/01/70"
  
  def __init__(self, pid, name, description, price, stock, creation_date):
    self.product_id = pid
    self.name = name
    self.description = description
    self.price = price
    self.stock = stock
    self.creation_date = creation_date
    
  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__)