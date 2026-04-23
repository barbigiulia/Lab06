from dataclasses import dataclass
@dataclass
class Retailer:
    code : int
    name : str
    retailer_type: str
    country : str

    def __eq__(self, other):
        return self.code == other.code   # chiave primaria

    def __hash__(self):
        return hash(self.code)



