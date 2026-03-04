
### Apni PI bnane ka tareeka : 
# ---------------------------------------------------------
import requests
from flask import Flask,render_template
app = Flask(__name__)



@app.route('/')  #LOCALHOST:5000/ => home page
def main():
    # return 'ISHMAL HERE!'
    return render_template('index.html')  # this is to render the html file, we can also pass data to the html file and display it on the webpage.
if __name__ == '__main__':
    app.run(debug=True)  #Deploy krne k liye debug false krna chahiye, production me false krna chahiye.

# -----------------------------------------------------------