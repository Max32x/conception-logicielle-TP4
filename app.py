import requests

class ProductDTO:
    def __init__(self, barcode):
        self.barcode = barcode
        self.product_data = self._fetch_product_data()
        if self.product_data:
            self.product_name = self.product_data.get('product', {}).get('product_name', '')
            self.ingredients_text = self.product_data.get('product', {}).get('ingredients_text', '')
            self.allergens = self.product_data.get('product', {}).get('allergens_from_user', '').lower()
            self.additives = self.product_data.get('product', {}).get('additives_tags', [])
        else:
            self.product_name = ""
            self.ingredients_text = ""
            self.allergens = ""
            self.additives = []

    def _fetch_product_data(self):
        """
        Fetch product data from Open Food Facts API using barcode.
        """
        url = f"https://world.openfoodfacts.org/api/v0/product/{self.barcode}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data for barcode: {self.barcode}")
            return None

    def has_intolerance(self, intolerances):
        """
        Check if any intolerance is present in the product.
        """
        if not isinstance(intolerances, list):
            raise TypeError("Intolerances must be provided as a list.")
        
        for intolerance in intolerances:
            if intolerance.lower() in self.allergens:
                return True
        return False

# Exemple d'utilisation
barcode = "3276550614043"
intolerances = ["eggs", "milk"]
product = ProductDTO(barcode)
if product.product_data:
    if product.has_intolerance(intolerances):
        print("Intolérance(s) trouvée(s) dans le produit.")
    else:
        print("Aucune intolérance trouvée dans le produit.")
else:
    print("Impossible de récupérer les données du produit.")
