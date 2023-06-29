from web3 import Web3
from solcx import compile_source, install_solc

install_solc()

compiled_solidity = compile_source('''// SPDX-License-Identifier: MIT

pragma solidity >=0.4.20;

contract HelloWorld {

    string public message;

    constructor() {
        message = "Hello World";
    }

    function setMessage(string memory _message) public {
        message = _message;
    }

    function ShowMessage() view public returns (string memory){
        return message;
    }

}''', output_values = ['abi','bin'])

contract_id, contract_interface = compiled_solidity.popitem()

w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

w3.eth.default_account = w3.eth.accounts[0]

abi = contract_interface['abi']

bincode = contract_interface['bin']

helloworld = w3.eth.contract(abi = abi, bytecode = bincode)

transaction_hash = helloworld.constructor().transact()

print(transaction_hash)

transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

helloworld_contract = w3.eth.contract(address = transaction_receipt.contractAddress, abi = abi)

print(helloworld_contract.functions.ShowMessage().call())

tx_hash_set_bye = helloworld_contract.functions.setMessage('bye').transact()

by_receipt = w3.eth.wait_for_transaction_receipt(tx_hash_set_bye)

print(helloworld_contract.functions.ShowMessage().call())