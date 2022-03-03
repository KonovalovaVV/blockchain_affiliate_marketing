from flask import Flask, request, jsonify, url_for, render_template
from blockchain_stuff import Block, Blockchain
from config_peers import peers
from datetime import datetime
import os
import ecdsa
from flask import redirect

AD_FOLDER = os.path.join('static', 'ad')
print(AD_FOLDER)
app = Flask(__name__)
app.url_map.strict_slashes = False

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True #to enable pretty printing with jsonify.
app.config['JSON_SORT_KEYS'] = False #to not sort while returning json response.
app.config['UPLOAD_FOLDER'] = AD_FOLDER

blockchain = Blockchain()

# form to create new transaction
@app.route('/')
def index():

	return render_template("make_transaction.html")

# receives form data from '/', generates signature and announces transaction.
@app.route('/process_transaction', methods= ['POST'])
def process_transaction():
	request.get_json(force=True)
	#generating keys
	private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
	public_key = private_key.get_verifying_key()

	#converting to string (for json)
	public_key = (public_key.to_string()).hex()

	# get the id of the ad banner and add to the message
	ad_name = request.json.get('name') # gets from the url, not from page
	ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

	timestamp = str(datetime.now())
	msg = {'transaction_timestamp': timestamp, 'from_addr': public_key, 'ad_name': ad_name, 'ip_address': ip_address}

	#signing with PRIVATE key
	signature = blockchain.generate_signature(private_key, msg)

	#converting bytes type to hex string, so it will be accepted by json.
	signature = signature.hex() 

	blockchain.announce_transaction(peers, {'message': msg, 'signature': signature})
	print('transaction has been made with - ', ad_name)
	return "Transaction has been made!"

# to view entire blockchain
@app.route('/chain', methods=['GET'])
def display_chain():
	blocks = []
	for each_block in blockchain.chain:
		blocks.append(each_block.__dict__)
	return jsonify({'blockchain': blocks, 
					'chain_length': len(blockchain.chain)})

# mine and announce block
@app.route('/mine', methods=['GET'])
def mining():
	mined_block = blockchain.mine()
	if mined_block:
		blockchain.announce_block(peers, mined_block)
		return jsonify({'mined_block': mined_block.__dict__})
	else:
		return "Nothing to mine!!"

# to check if larger chain exits on network and if yes then switch to it.
@app.route('/consensus', methods= ['GET'])
def chain_conflict():
	if blockchain.consensus(peers):
		return "Conflict detected, Switched to longest valid chain on the network!"
	else:
		return "We are good, no conflict in blockchain!"

# announced block gets added in blockchain
@app.route('/add_block', methods=['POST'])
def add_block():
	block_data = request.get_json()
	# clearing the blockchain.unconfirmed_transaction after block having those transaction is already mined.
	if block_data['transactions'] == blockchain.unconfirmed_transactions:
		blockchain.unconfirmed_transactions = []

	block = Block(block_data['index'], block_data['block_timestamp'], block_data['transactions'], block_data['prev_hash'], block_data['proof_of_work'])
	added = blockchain.add_block(block)
	if not added:
		return "The block was discarded by the node", 400
	return "Block added to the chain", 201

# announced transaction gets added in unconfirmed_transactions list.
@app.route('/add_transaction', methods= ['POST'])
def add_transaction():
	transaction_dict = request.get_json()
	blockchain.unconfirmed_transactions.append(transaction_dict)
	return "Transaction added to unconfirmed_transactions and is ready to be mined!"

# to view peers(all host url's from 'config_peers.py')
@app.route('/peers', methods= ["GET"])
def display_peers():
	return jsonify({
		'peers': str(peers),
		'count': len(peers)
		})

# to view unconfirmed_transactions list, which can be mined into a block
@app.route('/unconfirmed_transactions', methods= ["GET"])
def display_unconfirmed_transactions():
	return jsonify({
		'unconfirmed_transactions': blockchain.unconfirmed_transactions
		})