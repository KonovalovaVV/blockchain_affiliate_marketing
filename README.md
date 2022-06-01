# SMART CONTRACT AND BLOCKCHAIN APPLICATION IN AFFILIATE MARKETING

In order to increase the trust between vendors in Affiliate Marketing, a blockchain-based application was developed. It prevents manual alteration of the number of clicks made and increases the security or interaction between affiliates and publishers. Additionally, clicks are checked and validated
that it is not a result of automatic actions. The algorithm is developed and applied on a sample webpage. All the basic concepts of blockchain like proof of work, mining, consensus, generating and validating signature on transaction are implemented. 

## Instructions to run: 
```
In the ```config_peers.py``` add the mining peers. By default there are:
```
# store all url's running on the network here in string format, so that they can communicate
# for example: 'http://127.0.0.1:5000/'
peers = {'http://127.0.0.1:5000/', 'http://127.0.0.1:5001/'}
```
Open two terminals in the folder with the project. Use following commands to run instances of the application:   
For the first instance on port 5000:
```
set FLASK_APP=main.py
flask run --port 5000 --debugger --reload
```   
For the second instance on port 5001:   
```
set FLASK_APP=main.py
flask run --port 5001 --debugger --reload
```
There are two instances running on http://localhost:5000 and http://localhost:5001.

## How it works:

The main page running on http://localhost:<port_number> contains a few advertisement banners and their titles. After clicking on any of the banners, clicks information the “process_transaction”
method in the ‘main.py’ script is called and the click information, including the timestamp, IP address of the user and the unique name of the advertisement banner, is encrypted and added to the block. 

On the  http://localhost/unconfirmed_transactions webpage all transactions added to a block, which hasn‘t been validated and added to the blockchain yet are presented with corresponding descriptions.

When the number of made clicks reaches the defined amount (for testing purposes it is set to five), new block is broadcasted to peers, validated, and added to the blockchain. Block can be mined manually (with any number of transactions in it) by visiting http://localhost/mine. 

The whole blockchain and the total amount of made transactions can be seen on the http://localhost/chain. Each block stores total number of made clicks.

Additionally, the list of connected peers is presented in the http://localhost/peers. Alerts and information about the blockchain condition can be seen in the http://localhost/consensus. 