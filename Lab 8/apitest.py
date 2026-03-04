import requests
from flask import Flask, render_template

app = Flask(__name__)

# NASA API Configuration
NASA_URL = 'https://api.nasa.gov/planetary/apod?api_key=1CJ1JyHSqta0isZxYCDjfLmKQZxx6S2Hud5sQxkp'

@app.route('/')
def home():
    # 1. NASA se data mangwana
    response = requests.get(NASA_URL)
    
    if response.status_code == 200:
        data = response.json()
        
        # NASA data ko variables mein store karna
        title = data.get('title')
        image_url = data.get('url')
        description = data.get('explanation')
        date = data.get('date')
        
        # 2. Ye data HTML (index.html) ko bhej dena
        return render_template('index.html', t=title, img=image_url, desc=description, d=date)
    else:
        return "NASA API Error: " + str(response.status_code)

# Aapki apni banayi hui JSON API (Optional)
@app.route('/mydata')
def my_api():
    data_dict = {'name': 'Ishmal', 'age': 20, 'city': 'Lahore'}
    return data_dict

if __name__ == '__main__':
    app.run(debug=True)