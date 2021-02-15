from bs4 import BeautifulSoup
import requests
import json
import pprint
import json
from bs4 import BeautifulSoup as bs

pp = pprint.PrettyPrinter()

class FoodDelivery:
    
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    base_url_postCode = "https://i18n.api.just-eat.io/restaurants/bypostcode/"


    def get_all_restaurants(self, postalNr):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',"accept-tenant": "no"}
        response = self.session.get(self.base_url_postCode + postalNr, headers = headers)
        self.restaurants = response.json()
        
        return self.restaurants["Restaurants"]
    


    def get_menu(self, menu_id):
        menu_url = f"https://www.just-eat.no/menu/getproductsformenu?menuId={menu_id}"
        menu = self.session.get(menu_url, headers = self.headers)
        current_menu = {"produkter":menu.json()["Menu"]["products"], "tilbehør":menu.json()["Menu"]["accessories"]}
        self.menu_id = menu_id
        return current_menu["produkter"]
        

    
    def add_to_cart(self, restaurant_id, product_id):
        request_url = f"https://www.just-eat.no/restaurant/{restaurant_id}/menu/{self.menu_id}/basket/item"

        req_object = {"restaurantId":restaurant_id,"menuId":self.menu_id, "productId":product_id}
        
        res = self.session.post(request_url, data = req_object, headers = self.headers, cookies = self.session.cookies.get_dict())
        html = bs(res.content, "html.parser")
        self.basket_id = html.find("div", {"class":"infoBox-content infoBox-content--small"}).get("data-basketreceipt-id")

        return f"https://www.just-eat.no/account/login?returnurl=%2Forder%2Fdelivery-address%2F%3Fmenu%3D746%26basket%3D{self.basket_id}sQ%26collection%3DFalse", self.session.cookies
        
       

    # funker ikke
    def login(self, file):
        jsonData = open(file)
        tokenObj = json.load(jsonData)
        jsonData.close()
        self.email = tokenObj["EMAIL"]
        self.password = tokenObj["PASSWORD"]

        request_url = f"https://www.just-eat.no/account/login?returnurl=%2Forder%2Fuser-details%2F%3Fmenu%3D746%26basket%3D{self.basket_id}%26collection%3DFalse"

        get_login_page = self.session.get(request_url, headers = self.headers, cookies = self.session.cookies.get_dict())

        login_page = bs(get_login_page.content, "html.parser")
        verification_token = login_page.find("input", {"name": "__RequestVerificationToken"}).get("value")
        print(verification_token)


        payload = {
            "__RequestVerificationToken": verification_token,
            "Email":self.email,
            "Password":self.password,
            "RememberMe":"True",
            "RememberMe":"False"
        }

        login_req_url = f"https://www.just-eat.no/order/delivery-address/?menu=746&basket={self.basket_id}&collection=False"

        res = self.session.post(login_req_url, headers = self.headers, cookies = self.session.cookies.get_dict())
        html = bs(res.content, "html.parser")
        print(html)




    #funker ikke
    def make_payment(self):
        request_url = f"https://www.just-eat.no/order/delivery-address/?menu={self.menu_id}&basket={self.basket_id}g&collection=False"
        
        res = session.get(request_url, headers = self.headers, cookies = self.session.cookies.get_dict())
        print(bs(res.content, "html.parser"))


    
    def get_bot_tokens(self, file):
        jsonData = open(file)
        tokenObj = json.load(jsonData)
        jsonData.close()

        bot_token = tokenObj['DISCORD_TOKEN']
        guild_name = tokenObj["DISCORD_GUILD"]

        return bot_token, guild_name

        

food = FoodDelivery()

#foodId = food.get_all_restaurants("1482")[0]["CollectionMenuId"]
#menu = food.get_menu(foodId)


"""for product in menu:
    print(product["Name"], product["Desc"])"""

#pprint.pprint(food.get_menu(foodId)["produkter"])
#food.add_to_cart(2308, 33020)
#food.login("token.json")

        
        
        


            

