# Welcome to bashCoin Blockchain crypto currencty.
This project still under development. We will keep update about changes on project and documentation of API.


## About bashCoin.

**bashCoin** is cryto cyrrency which is built on top of the blochchain technology. Of course, it is not a hard to change project from crytocurreny to other concept. 


### Architecture of software

1. **bashCoin.sh**

The Core [**bashCoin.sh**](https://github.com/aze2201/bashCoin/blob/main/bin/bashCoin.sh)  software is developed on bash 5.1. 

It can do:
- Mining next block.
- Validating pending transaction and adding to next block.
- Printing tranaction data to client for sign it.
- Adding client signed transaction to pending transaction.

Remain:
- new external Block validation.
- Choose longest Chain (to resolve conflict)


2. **socketGateway3.py**
 
[**socketGateway3.py**](https://github.com/aze2201/bashCoin/blob/main/bin/socketGateway3.py) is SOCKET server.
The bashCoin uses [Websocket](https://en.wikipedia.org/wiki/WebSocket) protocol to interact with other nodes and external 3rt party apps. The websocket protocol help to achieve bidirectional communication. As, it is standarized by **W3C** it is easy to find library for connection in all programming language.

Topology:

![Alt text](https://github.com/aze2201/bashCoin/blob/main/data/TopologyBashCoin_v1.png?raw=true)


It can do:
- Find internal socket id which is executing bashCoin.sh from external and internal.
- Return the result to requested Client ID (As local executer also is socket client, Server don't trank session).
- SSL support by Peer Node Key-Pair

Remain:
- Local broadcasting for notification (127.0.0.1).
- External broadcasting about new BLOCK and Transaction.
- Block content provide (base64).
- PEM password autofill for next session.


```markdown
# Start project


> git clone https://github.com/aze2201/bashCoin.git

# start server
> cd bashCoin/bin
> python3 socketGateway3.py

# start local client. this app will send data to bashCoin.sh file.
# open new session
> cd bashCoin/bin
> exec 3<> communicate_pipe
cat communicate_pipe - | python3 wsdump.py  -r --text '{"command":"nothing","appType":"nothing","destinationSocketBashCoin":"yes"}' ws://127.0.0.1:8001 | while read line; do   
  res=$(echo ${line} | grep "{" | grep "}");  
  if [ $? -eq 0 ]; then     
    line=$(echo -e ${line});
    echo "$line" >> ../log/line.log
    cmd="./bashCoin.sh  '${line}' > communicate_pipe"; 
    echo $cmd >> ../log/command.log   
    eval $cmd;
  fi; 
done

## start another client
> python wsdump.py wss://127.0.0.1:8001
# send below JSON message to get Balance
> {"command":"checkbalance","ACCTNUM":"50416596951b715b7e8e658de7d9f751fb8b97ce4edf0891f269f64c8fa8e034"}

{"command": "checkbalance", "status": "0", "destinationSocket": "3", "result": {"publicKeyHASH256": "50416596951b715b7e8e658de7d9f751fb8b97ce4edf0891f269f64c8fa8e034", "balance": "46"}}

```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).



### Author: Fariz Muradov

