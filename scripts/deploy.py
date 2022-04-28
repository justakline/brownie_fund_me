from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import *


def deploy_fund_me():
    account = get_account()
    #Publish source allows you to see the details of the contract on etherscan

    #We can't pull from chainlink when on the local ganache
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRORMENTS:
        #We are saying, lets pull the address of chainlink for whatever networks we are on
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else: #It is a local chain so use mocks
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    fund_me = FundMe.deploy(price_feed_address, {"from":account}, publish_source = config["networks"][network.show_active()].get("verify"))
    
    
    # fund_me.wait(1)
    print("Contract Deployed to " + str(fund_me.address))
    return fund_me



def main():
    deploy_fund_me()