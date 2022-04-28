//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    //We are doing everything in terms of WEI so if something is not natively in wei we will immedietly convert it
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    AggregatorV3Interface priceFeed;
    address[] public funders;

    //Runs the second the contract is deployed and creates the owner of the contract
    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    //You are probably wondering, where is the moeny coming in??? it comes from the msg.value
    function fund() public payable {
        uint256 minimumUSD = 50 * (10**18);
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to send more wei value sent : "
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    //We are using the chainlink oracle to find the price of ETH to USD
    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    //pricFeed.latestRoundData returns a tuple, so we initialized a tuple and then assined it to priceFeed...we can use blanks to let the compiler know that
    //we are ignoring those values at those indexes
    //answer is an int, so we need to cast it to a uint and it is return in gwei-- 1*10**8
    //price returned is in usd, but with a precision of 1* 10^18
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();

        //price is returned in 10**8 so, for consistency in our contract we conver to 10**18
        return uint256(answer * (10**10));
    }

    //Returns how much eth given to function is worth IN USD
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice(); //price is in wei so we will ned to convert to eth in next line
        uint256 ethPriceinUSD = (ethPrice * ethAmount) / (10**18);
        return ethPriceinUSD;
    }

    //Will return the fee in wei... $50 entrance fee at $2000 per eth
    // is 0.025eth or 0.025 * 10**18 wei which is returned
    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return ((minimumUSD * precision) / price) + 1;
    }

    //This is a modifier, you can add this on to functions and any function with this will run this ...
    //putting the require before the _; means that you run the statement before starting the function, and visa versa
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the Owner can Withdraw");
        _;
    }

    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);

        for (uint256 i = 0; i < funders.length; i++) {
            address funder = funders[i];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
