from flask import Flask, render_template, request
from mtgsdk import Card

# api imports
from api import tournaments
from api import entities

app = Flask( __name__ )

##################
##### ROUTES #####
##################

##### Page Routes #####

@app.route("/<string:name>/", methods=["GET"] )
def hello( name ):
    number = 8675309
    cards = Card.where( set="dom" ).all()
    return render_template( 'landing/landing.html', name=name, number=number, cards=cards )


##### API Resources Route #####

@app.route( "/api/<string:resource>/",                   methods=["GET", "POST", "PUT", "DELETE"], defaults={ 'resource_id' : None } )
@app.route( "/api/<string:resource>/<int:resource_id>/", methods=["GET", "POST", "PUT", "DELETE"] )
def api( resource, resource_id ):
    # definitely make sure we're clear to call "eval" on this input
    sanitize_api_resource_string( resource )

    if request.method == "GET" and resource_id is not None:

        return eval( resource ).get( resource_id, request )

    elif request.method == "GET" and resource_id is None:

        return eval( resource ).search( request )

    elif request.method == "POST":

        return eval( resource ).create( request )

    elif request.method == "PUT":

        return eval( resource ).update( resource_id, request )

    elif request.method == "DELETE":

        return eval( resource ).delete( resource_id )

    else:
        # TODO return some sort of http error
        return

# TODO move this into its own file eventually
##### Utility/Helper Functions #####

# if this returns without error then the string is fine
def sanitize_api_resource_string( resource_string ):
    # TODO i should search the api/ directory and compare the string to file names. In addition to just checking for special characters and stuff
    return

############################
##### APP STARTUP CODE #####
### KEEP AT END OF FILE ####
############################

if __name__ == "__main__":
    app.run()
