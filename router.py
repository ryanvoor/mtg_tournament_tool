from flask import Flask, render_template, request

# page imports
from pages.tournaments import tournaments_page
from pages.landing     import landing_page

# api imports
from api import tournaments
from api import entities

app = Flask( __name__ )


##################
##### ROUTES #####
##################


##### Page Route #####

@app.route( "/",                                    methods=["GET"], defaults={ "option" : None, "page" : None } )
@app.route( "/page/",                               methods=["GET"], defaults={ "option" : None, "page" : None } )
@app.route( "/page/<string:page>/",                 methods=["GET"], defaults={ "option" : None                } )
@app.route( "/page/<string:page>/<string:option>/", methods=["GET"]                                              )
def page( page, option ):
    # redirect the base url to the landing page
    if page is None:
        page = "landing"

    # definitely make sure we're clear to call "eval" on this input
    sanitize_page_string( page )

    if option is None:

        return eval( page + "_page" ).render_page_template( request )

    else:

        return eval( page + "_page" ).render_page_option_template( request )


##### API Resources Route #####

@app.route( "/api/<string:resource>/",                   methods=["GET", "POST", "PUT", "DELETE"], defaults={ "resource_id" : None } )
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

        abort( 405 )


##### HTTP Error Handling #####

@app.errorhandler( Exception )
def general_error( error ):
    return render_template( "errors/general_error_page.html", error_message=str( error ) )

@app.errorhandler( 404 )
def http_error_not_found( error ):
    return render_template( "errors/http_error_page.html", error_number=404, error_message="Page not found" ), 404

@app.errorhandler( 405 )
def http_error_method_not_allowed( error ):
    return render_template( "errors/http_error_page.html", error_number=405, error_message="Method not allowed" ), 405

@app.errorhandler( 500 )
def http_error_internal_server( error ):
    return render_template( "errors/http_error_page.html", error_number=500, error_message="Internal server error" ), 500


# TODO move this into its own file eventually
####################################
##### Utility/Helper Functions #####
####################################

# if this returns without error then the string is fine
def sanitize_api_resource_string( resource_string ):
    # TODO i should search the api/ directory and compare the string to file names. In addition to just checking for special characters and stuff
    return

# if this returns without error then the string is fine
def sanitize_page_string( page_string ):
    # TODO i should search the pages/ directory and compare the string to file names. In addition to just checking for special characters and stuff
    return


############################
##### APP STARTUP CODE #####
### KEEP AT END OF FILE ####
############################

if __name__ == "__main__":
    app.run()
