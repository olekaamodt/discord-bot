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
        
        res = self.session.post(request_url, data = req_object, headers = self.headers, cookies = self.session.cookies)
        html = bs(res.content, "html.parser")
        self.basket_id = html.find("div", {"class":"infoBox-content infoBox-content--small"}).get("data-basketreceipt-id")

        return f"https://www.just-eat.no/account/login?returnurl=%2Forder%2Fdelivery-address%2F%3Fmenu%3D746%26basket%3D{self.basket_id}sQ%26collection%3DFalse", res.cookies
        
       

    # funker ikke
    def login(self, file):
        jsonData = open(file)
        tokenObj = json.load(jsonData)
        jsonData.close()
        self.email = tokenObj["EMAIL"]
        self.password = tokenObj["PASSWORD"]

        request_url = f"https://www.just-eat.no/account/login/?returnurl=%2F"

        get_login_page = self.session.get(request_url, headers = self.headers, cookies = self.session.cookies.get_dict())

        self.cookies = get_login_page.cookies

        login_page = bs(get_login_page.content, "html.parser")
        verification_token = login_page.find("input", {"name": "__RequestVerificationToken"}).get("value")

        cookie_string = ""
        for cookie in get_login_page.cookies:
            if cookie.name == "__RequestVerificationToken":
                request_token = cookie.value
            cookie_string += (cookie.name + "=" + cookie.value + "; ")

       
        
        print(cookie_string.rstrip(";"))

        login_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "nb-NO,nb;q=0.9,no;q=0.8,nn;q=0.7,en-US;q=0.6,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "200",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": cookie_string,
            "Host": "www.just-eat.no",
            "Origin": "https://www.just-eat.no",
            "Referer": "https://www.just-eat.no/account/login/?returnUrl=%2F",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        }


        

        login_req_url = f"https://www.just-eat.no/account/login/?returnUrl=%2F"

        res = self.session.post(login_req_url, headers = login_headers, cookies = get_login_page.cookies)
        print(res)
        html = bs(res.content, "html.parser")
        print(html)




    #funker ikke
    def make_payment(self):
        request_url = f"https://www.just-eat.no/order/delivery-address/?menu={self.menu_id}&basket={self.basket_id}g&collection=False"
        
        res = session.get(request_url, headers = self.headers, cookies = self.session.cookies)
        print(bs(res.content, "html.parser"))


    
    def get_bot_tokens(self, file):
        jsonData = open(file)
        tokenObj = json.load(jsonData)
        jsonData.close()

        bot_token = tokenObj['DISCORD_TOKEN']
        guild_name = tokenObj["DISCORD_GUILD"]

        return bot_token, guild_name

        

food = FoodDelivery()

#foodId = food.get_all_restaurants("1482")

#menu = food.get_menu(foodId)


"""for product in menu:
    print(product["Name"], product["Desc"])"""

#pprint.pprint(food.get_menu(foodId)["produkter"])
#food.add_to_cart(2308, 33020)
#food.login("token.json")

        
        
        


            

