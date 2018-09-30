from common.util import return_hello_world
from common      import db_lib

def get( tournament_id, request ):
    return return_hello_world()

def search( request ):
    db_lib.get_db_connection()
    return "successfully got a db connection i think"

def create( request ):
    # TODO
    return "CREATE"

def update( tournament_id, request ):
    # TODO
    return "UPDATE"

def delete( tournament_id ):
    # TODO
    return "DELETE"
