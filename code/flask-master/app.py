from flask import Flask, render_template
import random

app = Flask(__name__)

# Breakfast Pizzas That Want To Wake Up Next To You
# https://www.buzzfeed.com/rachelysanders/good-morning-pizza
images = [
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/22/13/enhanced/webdr10/enhanced-buzz-12910-1406051649-8.jpg",
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/22/12/enhanced/webdr02/original-1016-1406046783-3.jpg",
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/22/14/enhanced/webdr10/enhanced-buzz-12238-1406052511-32.jpg",
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/21/15/enhanced/webdr09/enhanced-27692-1405970823-1.jpg",
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/21/14/enhanced/webdr11/enhanced-buzz-30515-1405968961-18.jpg",
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/21/15/enhanced/webdr09/enhanced-26448-1405970636-20.jpg",
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/21/17/enhanced/webdr08/enhanced-4428-1405977456-4.jpg",
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/22/12/enhanced/webdr04/enhanced-buzz-4614-1406046869-8.jpg",
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/22/14/enhanced/webdr10/enhanced-12755-1406052410-10.jpg",
    "https://img.buzzfeed.com/buzzfeed-static/static/2014-07/22/14/enhanced/webdr02/enhanced-buzz-1275-1406053174-20.jpg"
]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

if __name__ == "__main__":
    # 'flask run --host=0.0.0.0' tells your operating system to listen on all public IPs.
    app.run(host="0.0.0.0")
