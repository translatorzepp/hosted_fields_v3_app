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
	# return "Hello world, we have a client token: " + client_token
	return render_template('checkout.html', client_token=client_token)


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

	# return "Victory! We got a nonce (" + nonce + ") and an amount (" + amount + ")!"
	if result.is_success:
		return "Victory! Transaction ID: " + result.transaction.id
	else:
		return "Failure! Try again. " + result.message


if __name__ == '__main__':
	app.run('127.0.0.1', debug=True, port=5000, ssl_context=tls_context)
