let fs = require('fs');

let pancakeSwapAbi =  [
    {"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},
    ];
let tokenAbi = [
    {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    ];

const Web3 = require('web3');

let pancakeSwapContract = "0x10ED43C718714eb63d5aA57B78B54704E256024E".toLowerCase();
const web3 = new Web3("https://bsc-dataseed1.binance.org");


// Calculates the exchange rate of 1 Token for BNB
async function calcSell( tokensToSell, tokenAddres){
    const web3 = new Web3("https://bsc-dataseed1.binance.org");

    let tokenRouter = await new web3.eth.Contract( tokenAbi, tokenAddres );
    let tokenDecimals = await tokenRouter.methods.decimals().call();
    
    tokensToSell = setDecimals(tokensToSell, tokenDecimals);
    let amountOut;
    try {
        let router = await new web3.eth.Contract( pancakeSwapAbi, pancakeSwapContract );
        amountOut = await router.methods.getAmountsOut(tokensToSell, [tokenAddres , BNB.address]).call();
        amountOut =  web3.utils.fromWei(amountOut[1]);
    } catch (error) {}
    
    if(!amountOut) return 0;
    return amountOut;
}

// Returns price of 1 BNB/USDT
async function calcBNBPrice(){
    const web3 = new Web3("https://bsc-dataseed1.binance.org");
    let bnbToSell = web3.utils.toWei("1", "ether") ;
    let amountOut;
    try {
        let router = await new web3.eth.Contract( pancakeSwapAbi, pancakeSwapContract );
        amountOut = await router.methods.getAmountsOut(bnbToSell, [BNB.address , USDT.address]).call();
        amountOut =  web3.utils.fromWei(amountOut[1]);
    } catch (error) {}
    if(!amountOut) return 0;
    return amountOut;
}

function setDecimals( number, decimals ){
    number = number.toString();
    let numberAbs = number.split('.')[0]
    let numberDecimals = number.split('.')[1] ? number.split('.')[1] : '';
    while( numberDecimals.length < decimals ){
        numberDecimals += "0";
    }
    return numberAbs + numberDecimals;
}

class Token {
    constructor(name, symbol, address, priceBNB=0, priceUSD=0){
        this.name = name;
        this.symbol = symbol;
        this.address = address;
        this.priceBNB = priceBNB;
        this.priceUSD = priceUSD;
    }
}

//Add a Binance token you would like to track:
let BNB  = new Token('Binance Coin', 'BNB' , '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', 1   );
let USDT = new Token('USDT'        , 'USDT', '0x55d398326f99059fF775485246999027B3197955', 0, 1);
let CGC  = new Token('Catgirl Coin', 'CGC' , '0x79eBC9A2ce02277A4b5b3A768b1C0A4ed75Bd936'      );

//Add the token to this list to update
let tokens = [BNB, USDT, CGC];

/*
This script communicates with the smart contract deployed by pancakeswap and calls the main function that was built to retrive the token prices
*/
(async () => {

    let bnbPrice = await calcBNBPrice()
    BNB.priceUSD = bnbPrice;
    let tokens_to_sell = 1;
    // Starting Iteration at 1 to skip the base Token (BNB)
    for (let i = 1; i < tokens.length; i++){
        tokens[i].priceBNB = await calcSell(tokens_to_sell, tokens[i].address)/tokens_to_sell;
        tokens[i].priceUSD = tokens[i].priceBNB*bnbPrice;
    }

    console.log(JSON.stringify(tokens));

    fs.writeFile('tokens.json', JSON.stringify(tokens), function (err) {
        if (err) return console.log(err);
      });

})();