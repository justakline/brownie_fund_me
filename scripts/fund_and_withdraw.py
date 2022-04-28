from brownie import FundMe
from scripts.helpful_scripts import *

def fund():
    fund_me = FundMe[-1] #Get the most recent contract deployed

    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    fund_me.fund({"from" :account, "value": entrance_fee})

def withdraw():
    fund_me = FundMe[-1] #Get the most recent contract deployed
    account = get_account()
    # print(f"Amount before withdraw: {fund_me.}")
    fund_me.withdraw({"from":account})
    print("withdrew")

def main():
    fund()
    withdraw()




##Staring Price = 1  Decimals = 0  
# 
# 1  00 0000 0000 0000 0000 0000000000 = starting price* *10**18  * 10*10
##Staring Price = 1  Decimals = 10  
# 
# 100 0000 0000 0000 0000 0000000000 = starting price* *10**18  * 10*10

# 1 00000000 0000000000