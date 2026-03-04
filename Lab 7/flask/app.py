from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # 1. Fetch Cat Fact
    fact_url = "https://catfact.ninja/fact"
    fact_data = requests.get(fact_url).json()
    fact = fact_data.get('fact')

    # 2. Fetch Cat Image
    img_url = "https://api.thecatapi.com/v1/images/search"
    img_data = requests.get(img_url).json()
    image = img_data[0].get('url') # API returns a list, so we take the first item

    return render_template('index.html', fact=fact, image=image)

if __name__ == '__main__':
    app.run(debug=True)