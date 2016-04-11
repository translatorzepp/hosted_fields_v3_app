from flask import Flask, render_template, request
import braintree

app = Flask(__name__)

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id = "ryqy4yyw7m5bf92h",
    public_key = "ymtqgy8773zq2fw3",
    private_key = "7dd7253c4c53d675f15e869212659579"
)

@app.route('/', methods=["GET"])
def get_client_token():
	client_token = braintree.ClientToken.generate()
	# return "Hello world, we have a client token: " + client_token
	return render_template('checkout.html', client_token=client_token)
# def hello_world():
#     return 'Hello World!'

@app.route("/create_transaction", methods=["POST"])
def create_transaction():
	nonce = request.form["nonce"]
	amount = request.form["amount"]

	result = braintree.Transaction.sale({
		"amount": amount,
		"payment_method_nonce": nonce,
		"options": {
			"submit_for_settlement": True
		}
	})

	if result.is_success:
		return "Victory! Transaction ID: " + result.transaction.id
	else:
		return "Failure! Try again."
	# return "Victory! We got a nonce (" + nonce + ") and an amount (" + amount + ")!"

if __name__ == '__main__':
	app.debug = True
	app.run()