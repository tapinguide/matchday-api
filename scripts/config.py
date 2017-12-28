#!/usr/bin/env python
#encoding: utf-8

#API Key
KEY = 'FOOTBALL_API_KEY'
#Competition ID
COMP_ID = ''

#MySQL Credentials
MYSQL_USER = 'MYSQL_USER'
MYSQL_PASSWORD = 'MYSQL_PASSWORD'
MYSQL_HOST = 'MYSQL_HOST'
MYSQL_PORT = 0000
MYSQL_DB = 'MYSQL_DB_NAME'

try:
    from local_config import *
except ImportError as e:
    pass
