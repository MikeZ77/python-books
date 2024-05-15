# The facade pattern provides a simple interface to a larger more complex system
# For example, we can provide conveinent methods for more complex tasks.
# Create a new interface for disconnected or seperate systems
# Or wrap a collection of poorly designed API's into a single well defined API ...
# that is easier to use.

from datetime import datetime

# We have an order that needs to be processed and shipped.
class Payment:
    def process_payment(self, ard_id: int) -> bool:
        print("Processing payment") 
        return True

class Inventory:
    def get_inventory(self, item_id: int) -> 10:
        print("Getting inventory remaining")
        return 10
        
class Shipping:
    def schedule_shipment(self, item_id: int, time: datetime):
        print("Scheduling earliest possible date for shipment.")


# The facade
class Order:
    def __init__(self):
        self.payment = Payment()
        self.inventory = Inventory()
        self.shipping = Shipping()
        
        # Lets say the order info got updated as the user entered ...
        # the info in the form.
        self.card_id = 101010101010101
        self.item_id = 15

    def create_order(self):
        self.payment.process_payment(self.card_id)
        self.inventory.get_inventory(self.item_id)
        self.shipping.schedule_shipment(self.item_id, datetime.now())
        
if __name__ == "__main__":
    Order().create_order()