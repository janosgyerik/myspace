MySpace
=======
TODO
Open ID login with whitelisting.
Open-source project, using Django, Python,
HTML5, Bootstrap from Twitter.


Setup
-----
1. Install required python modules

        pip install -r requirements.txt

2. Create database (sqlite3), and admin account

        ./manage.py syncdb

3. ... TODO

6. Start local website on localhost:8000

        ./manage.py runserver

7. Visit http://localhost:8000/


Local settings
--------------
The default settings.py is suitable for development. To override some
settings, especially DATABASES and SECRET_KEY, create a custom
local_settings.py file, based on the included local_settings.py.sample
and call manage.py like this:

    ./manage cmd --settings=local_settings


Live demos
----------
- http://myspace.janosgyerik.com/


Screenshots
-----------
TODO
![Folders](https://github.com/janosgyerik/myspace/raw/master/common/static/screenshots/image1.png)


Features
--------
TODO


