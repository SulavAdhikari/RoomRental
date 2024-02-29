

This uses A linear regression model to calculate a suitable rent price from BHK and number of bathrooms.
the training data was scraped and contains real data from kathmandu valley

By using python and Django. The Web app has all the basic features a ecommerce-like app needs.
like authentication, uploading images, dashboard and a admin dashboard


to run this webapp follow the instructions below. 

first download or clone the repo

open a terminal in the folder. 
run the following commands

```
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
python3 manage.py runserver
```

then you can visit the url below

http://127.0.0.1:8000