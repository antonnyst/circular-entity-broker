import json, random, uuid

class Sawblade:
  product_id = ""
  name = ""
  description = ""
  price = 0.0
  min_price = 0
  max_price = 0
  stock = 0
  max_stock = 0
  manufacturer = ""
  teeth_grade = 0.0
  teeth_amount = 0.0
  
  # def __init__(self):
  #   self.product_id = str(uuid.uuid4())
    
  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__)

  def toObject(self):
    return self.__dict__
  
  # Convert product data into an array of properties that can be sent to the broker
  def toProperties(self):
    properties = []
    
    # General props
    properties.append({
      "valueType": "string",
      "property": "id",
      "value": self.product_id
    })
    properties.append({
      "valueType": "string",
      "property": "name",
      "value": self.name
    })
    properties.append({
      "valueType": "string",
      "property": "description",
      "value": self.description
    })
    properties.append({
      "valueType": "string",
      "property": "manufacturer",
      "value": self.manufacturer
    })
    # Sawblade props
    properties.append({
      "valueType": "float",
      "property": "teethGrade",
      "value": self.teeth_grade
    })
    properties.append({
      "valueType": "float",
      "property": "teethAmount",
      "value": self.teeth_amount
    })

    return properties
  
  def generate_fluid_data(self):
    # Change price sometimes
    if random.randint(1, 4) == 1:
      self.price = round(random.random() * (self.max_price - self.min_price) + self.min_price, 2)

    # Change stock sometimes
    if random.randint(1, 4) == 1:
      self.stock = random.randint(0, self.max_stock)
    
    properties = []
    
    # General props
    properties.append({
      "valueType": "float",
      "property": "price",
      "value": self.price
    })
    properties.append({
      "valueType": "float",
      "property": "stock",
      "value": self.stock
    })

    return properties


product_gen_sawblade = {
  "small": {
    "teethGrade": {
      "min": 20.0,
      "max": 40.0,
    },
    "teethAmount": {
      "min": 20,
      "max": 50,
    },
    "prodNums": [0, 1, 2, 3, 4, 5],
  },
  "large": {
    "teethGrade": {
      "min": 12.0,
      "max": 25.0,
    },
    "teethAmount": {
      "min": 80,
      "max": 200,
    },
    "prodNums": [5, 6, 7, 8, 9],
  }
}
  
def generate_random_sawblade(company_name, naming_scheme):
  sawblade = Sawblade()
  sawblade.manufacturer = company_name
  
  # Randomize properties
  size = random.choice(["small", "large"])
  params = product_gen_sawblade[size]
  sawblade.teeth_grade = round(random.random() * (params["teethGrade"]["max"] - params["teethGrade"]["min"]) + params["teethGrade"]["min"], 1)
  sawblade.teeth_amount = round(random.random() * (params["teethAmount"]["max"] - params["teethAmount"]["min"]) + params["teethAmount"]["min"], 1)

  # Create a random name based on grade and teeth
  prod_name = random.choice(params["prodNums"])
  prod_gen = random.randint(1, 9)
  variant = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
  desc = generate_sawblade_desc(sawblade.teeth_grade)
  
  # Set properties
  sawblade.name = naming_scheme(prod_gen, prod_name, variant)
  sawblade.description = desc
  
  sawblade.min_price = random.randint(1, 100)
  sawblade.max_price = sawblade.min_price + random.randint(1, 50)
  sawblade.price = round(random.random() * (sawblade.max_price - sawblade.min_price) + sawblade.min_price, 2)
  sawblade.max_stock = random.randint(10, 5000)
  sawblade.stock = random.randint(0, sawblade.max_stock)
  
  return sawblade

def generate_sawblade_desc(grade):
  desc = f"{grade} gr. Sawblade"
  # Add a random feature sometimes
  if random.randint(0, 1) == 0:
    adjectives = ["ISO-Certified", "Brand-New", "Incredible", "Fantastic"]
    features = ["Anti-Dust Technology", "Self-Repairing Technology", "AutoGrade", "Features"]
    desc += f" with {random.choice(adjectives)} {random.choice(features)}"
  
  return desc
