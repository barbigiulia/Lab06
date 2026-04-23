from dataclasses import dataclass
@dataclass
class Vendita:
    date: str
    ricavo: float
    retailer_code: int
    product_number: int
    product_brand: str

    def __str__(self):
        return (f"Data: {self.date}; Ricavo: {self.ricavo}; "
                f"Retailer: {self.retailer_code}; "
                f"Product Number: {self.product_number}")