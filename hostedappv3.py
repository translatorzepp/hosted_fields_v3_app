from flask import Flask, render_template, request, url_for
import braintree
import ssl

app = Flask(__name__)

merchant_id = "ryqy4yyw7m5bf92h"
braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id = merchant_id,
    public_key = "ymtqgy8773zq2fw3",
    private_key = "7dd7253c4c53d675f15e869212659579"
)

# self_signed_ssl_cert_path = url_for("static", filename="server.crt")
# self_signed_ssl_cert_key_path = url_for("static", filename="server.key")
self_signed_ssl_cert_path = "static/server.crt"
self_signed_ssl_cert_key_path = "static/server.key"
tls_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
tls_context.load_cert_chain(self_signed_ssl_cert_path, self_signed_ssl_cert_key_path)

@app.route('/', methods=["GET"])
def get_client_token():
    client_token = braintree.ClientToken.generate()
    return render_template('checkout.html', client_token=client_token)


@app.route('/print_client_token', methods=["GET"])
def print_client_token():
    return braintree.ClientToken.generate()


@app.route('/create_transaction', methods=["POST"])
def create_transaction():
    nonce = request.form["nonce"]
    amount = request.form["amount"]
    devdat = request.form["device_data"]

    result = braintree.Transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        },
        "device_data": devdat,
        "descriptor": {
            "name": "HostedFields*JSv3",
        },
    })

    if result.transaction:
        trans_id = result.transaction.id
        if result.is_success:
            return "Victory! Transaction ID: " + trans_id
            # return 'Victory! Transaction: <a href="https://sandbox.braintreegateway.com/merchants/{0}/transactions/{1}" target="_blank">{1}</a>'.format(merchant_id, trans_id)
            # the code that renders this does not render html rn
        else:
            return "Failure! Transaction ID: {0}. {1}".format(trans_id, result.message)
    else:
	return 'Failure! Try again.\n{0}'.format(result.message)


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        #host='0.0.0.0', #use this to make server available to anyone on network, on your machine's IP address
        debug=True,
        port=5000,
        #ssl_context=tls_context #comment out to run w/out https
    )
