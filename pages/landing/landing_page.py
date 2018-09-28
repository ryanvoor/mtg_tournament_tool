from flask import render_template
from mtgsdk import Card

def render_page_template( request ):
    number = 8675309
    cards = Card.where( set="dom" ).all()
    return render_template( "landing/landing.html", name=request.args.get("name"), number=number, cards=cards )

def render_page_option_template( request ):
    # TODO
    return "render landing page option template"
