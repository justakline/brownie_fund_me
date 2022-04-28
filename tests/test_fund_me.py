from scripts.helpful_scripts import *
from brownie import FundMe, exceptions
from scripts.deploy import *
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from" : account, "value" : entrance_fee})
    tx.wait(1)

    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    tx2 = fund_me.withdraw({"from":account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


#Pytest skip can be used for skiping tests for specidic reasons, like if not on a locla blockchain
def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRORMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    #This is saying that I want whats in this to fail and that is good... it wont throw an exception and will pass the test
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from" : bad_actor})
