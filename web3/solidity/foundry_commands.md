
### deploy ###

forge -> compile and interacte with contract 
cast -> interact with deployed contracts
anvil -> deploy a local blockchain
forge fmt --> to format the solidity code

forge create <contract > --rpc-url <url > --private-key <private key>
 
forge script <contract path> --rpc-url <url> --account <key name> --sender <wallet address> --broadcast -vvvv {key name-> get when casted, wallet address -> public address in wallet, script --> runs the specified script }

### casting the private key ###
cast wallet import defaultkey --interactive   {cast your  private key once so every time it will be used as default}
cast wallet list { gives all keys u stored}

cast --to-base <hex> dec { converts hex into decimal values }

### interacting with deployed contract ###
forge inspect <contract name> abi {gives the abi}

cast send <contract address> "<function name(types of args)>" <args> --rpc-url <url > --pricate-key <private key>
cast call <contract address> "<function name(types of args)>" <args> --rpc-url <url > --pricate-key <private key>  { call for view functions }
cast send 0x5fbdb2315678afecb367f032d93f642f64180aa3 "setNumber(uint256)" 123 --rpc-url http://127.0.0.1:8545  --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

### test ###

forge test --mt <testname> -vvvv 
forge test --fork-url <chain url >

### storage ###
cast storage <contract address> <storage slot> { can access the storage};
`
forge inspect <contract name > storageLayout

cast sig "<function name(types)>" {gives the selector}
cast --calldata-decode "<function name(types)>" <call data of function> 