$( initialize );

function initialize() {
    var url = 'https://api.magicthegathering.io/v1/cards'
    var map = {
        set : 'dom',
    }
    $.get( url, map )
        .done( receive_fetch_cards_request )
}

function receive_fetch_cards_request( json, text_status ) {
    console.log( json );
}
