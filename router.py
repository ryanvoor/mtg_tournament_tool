from flask import Flask, render_template, request, abort
import os
import re
from fnmatch import fnmatch

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

@app.route( "/",                                    methods=["GET"], defaults={ "option" : None, "page" : None }, strict_slashes = False )
@app.route( "/page/",                               methods=["GET"], defaults={ "option" : None, "page" : None }, strict_slashes = False )
@app.route( "/page/<string:page>/",                 methods=["GET"], defaults={ "option" : None                }, strict_slashes = False )
@app.route( "/page/<string:page>/<string:option>/", methods=["GET"],                                              strict_slashes = False )
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

@app.route( "/api/<string:resource>/",                   methods=["GET", "POST", "PUT", "DELETE"], defaults={ "resource_id" : None }, strict_slashes = False )
@app.route( "/api/<string:resource>/<int:resource_id>/", methods=["GET", "POST", "PUT", "DELETE"],                                    strict_slashes = False )
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

@app.errorhandler( 400 )
def http_error_not_found( error ):
    return render_template( "errors/http_error_page.html", error_number=400, error_message="Bad request/Malformed URL" ), 400

@app.errorhandler( 403 )
def http_error_not_found( error ):
    return render_template( "errors/http_error_page.html", error_number=403, error_message="Access was forbidden" ), 403

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

    if len( re.findall( "[^a-z|_]", resource_string ) ) > 0:

        abort( 400 )

    if resource_string + ".py" not in get_files_in_dir_with_extension( "api", "py" ):

        abort( 403 )

    return

# if this returns without error then the string is fine
def sanitize_page_string( page_string ):

    if len( re.findall( "[^a-z|_]", page_string ) ) > 0:

        abort( 400 )

    if page_string + "_page.py" not in get_files_in_dir_with_extension( "pages", "py" ):

        abort( 403 )

    return

def get_files_in_dir_with_extension( directory, extension ):

    root = "./" + directory
    pattern = "*." + extension
    init_pattern = "__init__.py"
    files_to_return = []

    for path, subdirs, files in os.walk(root):

        for name in files:

            if fnmatch( name, pattern ) and not fnmatch( name, init_pattern ):

                files_to_return.append( name )

    return files_to_return



############################
##### APP STARTUP CODE #####
### KEEP AT END OF FILE ####
############################

if __name__ == "__main__":

    app.run()
