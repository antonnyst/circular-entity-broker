import json, random
from product import generate_random_sawblade, generate_sawblade_desc

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
    # Pick random products to update
    products_to_update = []
    while len(products_to_update) < min(amount, len(self.products)):
      product = random.choice(self.products)
      if product not in products_to_update:
        products_to_update.append(product)
        
    # Regenerate descriptions of selected products
    for product in products_to_update:
      product.description = generate_sawblade_desc(product.teeth_grade)
      
    # Return list of updated products
    return products_to_update
  
  def removeProducts(self, amount):
    # Pick random products to remove
    products_to_remove = []
    while len(products_to_remove) < min(amount, len(self.products)):
      product = random.choice(self.products)
      if product not in products_to_remove:
        products_to_remove.append(product)
        
    for product in products_to_remove:
      self.products.remove(product)
    
    # Return list of product IDs of the removed products
    return products_to_remove
