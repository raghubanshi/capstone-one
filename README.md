# Link to API

https://newsapi.org/docs/get-started

# Title 
News App

# URL deployed at:
https://capstone-one.onrender.com/

# Setup

First clone it to your local machine by running
```
git clone https://github.com/raghubanshi/capstone-one.git
cd capstone-one
```

Create virtual environment and activate it
```
$ python3 -m venv venv
$ source /venv/bin/activate
```
Then install all the necessary dependencies
```
pip install -r requirements.txt
```
# about API key

To run the website, we must create account at link provided for api that will provide us the api code. Then in app.py create a variable 
API_KEY_FOR_NEWS and assign the value to the api code. Or create secrets_api.py file inside news-app directory and then create a variable API_KEY_FOR_NEWS and assign the value to the api code.

To run the application, run the command below to start the application.
```
flask run --debug
```

# features:

User can create an account, get logged in and see various news from various parts of the world. They can serach, use filter to get the desired news. They can save the news and see that news in their saved news section. 

# Tech stack

Used Flask, Python, HTMLL, CSS, Bootsrap, Javascript. Flask-wtforms was not used as in most of the real website doesn't prefer using python/flask for frontend part. 
