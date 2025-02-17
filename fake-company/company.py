import json, random
from product import generate_random_sawblade

class FakeCompany:
  id = ""
  name = ""
  access_token = ""
  registered = False
  products = []
  sawblade_naming_scheme = lambda gen, prod, variant, desc: ""
  
  def __init__(self):
    self.name = self.generateName()
    
    # Create sawblade product naming scheme lambda function
    gen_zeros = random.randint(0, 2)
    prod_zeros = random.randint(0, 2)
    pnum_separator = random.choice(["-", "", ":"])
    include_variant = random.randint(0, 1) == 0
    
    self.sawblade_naming_scheme = lambda gen, prod, variant: f"{str(gen)}{"0"*gen_zeros}{pnum_separator}{str(prod)}{"0"*prod_zeros}{pnum_separator}{include_variant and variant or ""}"
    
  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__)
  
  def generateName(self):
    founder_names = ["Adam", "Anton", "Filip", "Viggo", "Eric"]
    adjectives = ["Fantastic", "Special", "Amazing", "Interesting", "Useful"]
    company_descriptors = ["Sawblades", "Woodworking Tools", "Machinery", "Solutions"]
    
    return f"{random.choice(founder_names)}'s {random.choice(adjectives)} {random.choice(company_descriptors)}"
  
  def generateProducts(self, amount):
    new_products = []
    for _ in range(amount):
      new_products.append(generate_random_sawblade(self.name, self.sawblade_naming_scheme))
      
    # Return list of new products
    return new_products
  
  def updateProducts(self, amount):
    # Return list of updated products
    pass
  
  def removeProducts(self, amount):
    # Return list of product IDs of the removed products
    pass
