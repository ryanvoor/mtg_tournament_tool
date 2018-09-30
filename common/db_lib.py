# external libraries
import psycopg2
import re
import os

# returns a db_connection object using the DATABASE_URL config var
def get_db_connection():
    # TODO need to implement the database_url
    # grab the DATABASE_URL config var
    db_url = os.environ.get('DATABASE_URL')

    # make sure that we got the DATABASE_URL
    if db_url is None:
        raise IOError( "Could not get the DATABASE_URL config variable" )

    # parse the DATABASE_URL into the host, port, db_name, and db_user
    # the url looks like this: postgres://db_username:db_password@db_host_name:port/name_of_db_itself
    p = "^postgres://(.*):(.*)@(.*):(\d*)/(.*)$"
    db_user     = re.match(p, db_url).group(1)
    db_password = re.match(p, db_url).group(2)
    db_host     = re.match(p, db_url).group(3)
    db_port     = re.match(p, db_url).group(4)
    db_name     = re.match(p, db_url).group(5)

    # get the db_connection
    return psycopg2.connect("dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (db_name, db_user, db_host, db_port, db_password))


