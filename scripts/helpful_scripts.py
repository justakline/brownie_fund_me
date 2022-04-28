from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3


DECIMALS = 10
STARTING_PRICE = 2000 * (10**8) #starting price of usd/eth ... the 10**8 is used for the function, DO NOT CHANGE

FORKED_LOCAL_ENVIRORMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRORMENTS = ["development", "ganache-local"]

def get_account():
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRORMENTS) or network.show_active() in FORKED_LOCAL_ENVIRORMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks")
        if(len(MockV3Aggregator) <= 0):
            MockV3Aggregator.deploy(DECIMALS,STARTING_PRICE, {"from" :get_account()})
        