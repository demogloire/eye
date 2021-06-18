
var csrf_token = "{{ csrf_token() }}";

paypal.Button.render({
  env: 'sandbox', // Or 'production' 'sandbox'
  // Set up the payment:
  // 1. Add a payment callback
  payment: function(data, actions) {
    // 2. Make a request to your server
    return actions.request.get("{{url_for('projet.payement_donation',  _external=True)}} ")
      .then(function(res) {
        // 3. Return res.id from the response
        return res.paymentID;
      });
  },
  // Execute the payment: 
  // 1. Add an onAuthorize callback
  onAuthorize: function(data, actions) {
    // 2. Make a request to your server
    return actions.request.post("{{url_for('projet.execute_donation',  _external=True)}}", {
      paymentID: data.paymentID,
      payerID:   data.payerID
    }, {
        headers: {
            'X-CSRFToken': csrf_token,
        }
    }
    
    
    )
      .then(function(res) {
        window.setTimeout(function(){
        // Move to a new location or you can do something else
        location.replace("{{url_for('projet.parrainer')}}");
        }, 1000); 

      });
  }
}, '#paypal-button');