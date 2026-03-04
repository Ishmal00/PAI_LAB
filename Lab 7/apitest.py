# ------------------------------------------------------------------------
#  Kisi or ki API key se request krne ka tareeka :
# ------------------------------------------------------------------------
import requests
api_key = '1CJ1JyHSqta0isZxYCDjfLmKQZxx6S2Hud5sQxkp'
url = 'https://api.nasa.gov/planetary/apod?api_key=1CJ1JyHSqta0isZxYCDjfLmKQZxx6S2Hud5sQxkp'

# response = requests.get(url)
# print(response)
# # data = response.json()


# #agar response agya h to , json do uska , 200 is correct response code.
# # 200= success , 404 = url do not exist,500,403,429 => server error, client error, too many request(all response code have different meaning)

# if response.status_code == 200:
#     data = response.json()
#     print(data)

# # json is like a dictionary, we can access the data using keys

#     print(data['title'])


# -------------------------------------------------------------------------





### Apni PI bnane ka tareeka : 
# ---------------------------------------------------------
import requests
import flask
app = flask.Flask(__name__)

data_dict = {
    'name': 'Ishmal',
    'age': 20,
    'city': 'Lahore'
} # this is to make json data, we can also get data from database and convert it to json format and return it to the client.


@app.route('/data')  #LOCALHOST:5000/data  => home page
def home():
    # return 'ISHMAL HERE!'
    return data_dict
if __name__ == '__main__':
    app.run(debug=True)  #Deploy krne k liye debug false krna chahiye, production me false krna chahiye.

# -----------------------------------------------------------







# -----information about flask and api-----
# flask is a web framework for python, it allows us to create web applications easily. It is a micro framework, which means it does not have a lot of built-in features, but it is easy to use and flexible. We can use flask to create a simple web application that displays the data we get from the API.
from flask import Flask
app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)  #True ka matlab changes refresh kr k deta h, false krne se changes refresh nhi hoga, production me false krna chahiye.