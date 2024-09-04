
from types import NoneType
from flask import Flask, render_template, send_from_directory
from web3 import Web3, HTTPProvider
import json
import os
from eth_account import Account
from gevent import pywsgi

app = Flask(__name__)
ETH_PROVIDER = "https://mainnet.infura.io/v3/37817291b672499cb230df7589cf4b18"
w3 = Web3(HTTPProvider(ETH_PROVIDER))


contractAddress = "0xf85F49EBF37CbEdA4A64B432c7645967088BCF2e"
contractAddress = w3.to_checksum_address(contractAddress)


@app.route("/")
def index():
    return render_template("Demo.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/source")
def getSource():
    global content
    with open("contract.txt", "r") as f:
        content = f.read()
    return render_template("index.html", content=content)


@app.route("/<address>")
def check(address):
    abi = """[
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "yours",
                        "type": "uint256"
                    }
                ],
                "name": "respond",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "_add",
                        "type": "address"
                    }
                ],
                "name": "check",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]"""

    # 创建合约实例
    contract_instance = w3.eth.contract(address=contractAddress, abi=abi)
    address = w3.to_checksum_address(address)  # 确保地址是 checksum 格式

    # 判断是否完成挑战
    isComplete = contract_instance.functions.check(address).call()

    if isComplete:
        flag = "SYC{Privt3_bs1_n1#_4f3}"
        return render_template("index.html", content=flag)
    else:
        message = "you have not solved the challenge, try again"
        return render_template("index.html", content=message)


if __name__ == "__main__":
    app.run(debug=True)
