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
  
  # Convert product data into an array of properties that can be sent to the broker
  def toProperties(self):
    properties = []

    for propName, value in self.__dict__.items():
      value_is_number = type(value) == float or type(value) == int
      properties.append({
        "valueType": value_is_number and "float" or "string",
        "property": propName,
        "value": str(value),
      })

    return properties