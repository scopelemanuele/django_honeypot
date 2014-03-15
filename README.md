django-honeypot
===============

A simple implementation of Project Honey Pot to reduce spam bot in your site
Django-honeypod analyzes all the traffic on the site by checking the reputation of the visitor on the website of the project http://www.projecthoneypot.org/home.php.

INSTALLATION:


1) Add Django-HoneyPod to INSTALLED_APPS:
    INSTALLED_APPS = (
        [...],
        'django_honeypot',
        [...]
    )

2) Add Django-HoneyPod middleware to MIDDLEWARE_CLASSES:
    MIDDLEWARE_CLASSES = (
        [...]
        'django_honeypot.middleware.HoneypotMiddleware',
        [...]
    )

CONFIGURATION:

The configuration is done by editing the file settings.py file.

Option:

--HoneyKey: is Honey Pot Key, to get the key you need to register on the site  http://www.projecthoneypot.org/home.php.

--HoneyPotUrl: is the address to redirect bad traffic, you can use an Quicklinks obtainable here: http://www.projecthoneypot.org/manage_quicklink.php

--Suspicious: if set to True allows traffic from suspicious visitor

--ThreatRating: is the reputation allowed 0 to 255 where 0 is good 255 is bad. None allow all reputation. For more info: http://www.projecthoneypot.org/threat_info.php

Every visitor suspicion is recorded on the database.
