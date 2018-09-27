from flask import Flask, render_template
from mtgsdk import Card
app = Flask( __name__ )

##################
##### ROUTES #####
##################

@app.route("/<string:name>/")
def hello( name ):
    number = 8675309
    cards = Card.where( set="dom" ).all()
    return render_template( 'landing/landing.html', name=name, number=number, cards=cards )


############################
##### APP STARTUP CODE #####
### KEEP AT END OF FILE ####
############################

if __name__ == "__main__":
    app.run()
