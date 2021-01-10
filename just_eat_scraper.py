from bs4 import BeautifulSoup
import requests
import json
import pprint

pp = pprint.PrettyPrinter()

class FoodDelivery:
    
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    base_url_postCode = "https://i18n.api.just-eat.io/restaurants/bypostcode/"


    def get_all_restaurants(self, postalNr):
        headers = headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',"accept-tenant": "no"}
        response = self.session.get(self.base_url_postCode + postalNr, headers = headers)
        self.restaurants = response.json()
        
        return self.restaurants["Restaurants"]
    


    def get_menu(self, restaurant_id):
        menu_url = f"https://www.just-eat.no/menu/getproductsformenu?menuId={restaurant_id}"
        menu = self.session.get(menu_url, headers = self.headers)
        current_menu = {"produkter":menu.json()["Menu"]["products"], "tilbehør":menu.json()["Menu"]["accessories"]}
        return current_menu["produkter"]
        

    
    def add_to_cart(self):
        body = "restaurantId=2915&menuId=7419&productId=416281"
        session.post(url, body = body, headers = self.headers)
        

food = FoodDelivery()

foodId = food.get_all_restaurants("1482")[0]["CollectionMenuId"]
#menu = food.get_menu(foodId)


"""for product in menu:
    print(product["Name"], product["Desc"])"""

#pprint.pprint(food.get_menu(foodId)["produkter"])

        
        
        


            

