# setup.py
from distutils.core import setup

setup(name = "geocachepython",
			author = "Alan Richards",
			author_email = "alarobric@gmail.com",
			url = "code.google.com/p/geocachepython",
            version = "0.5.9",
            py_modules = ['geocache'],
            packages = ['geopy'],
            scripts = ['geocachepython.py'],
            ) 
