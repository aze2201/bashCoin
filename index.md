# Welcome to bashCoin Blockchain crypto currencty.
This project still under development. We will keep update about changes on project and documentation of API.


##About bashCoin.

**bashCoin** is cryto cyrrency which is built on top of the blochchain technology. Of course, it is not a hard to change project from crytocurreny to other concept. 


### Architecture of software

The Core [**bashCoin.sh**](https://github.com/aze2201/bashCoin/blob/main/bin/bashCoin.sh)  software is developed on bash 5.1. 

It can do:
- Mining next block.
- Validating pending transaction and adding to next block.
- Printing tranaction data to client for sign it.
- Adding client signed transaction to pending transaction.

Remain:
- new external Block validation.
- Choose longest Chain (to resolve conflict)


Newtorking

The bashCoin uses [Websocket](https://en.wikipedia.org/wiki/WebSocket) protocol to interact with other nodes and external 3rt party apps. The websocket protocol help to achieve bidirectional communication. As, it is standarized by **W3C** it is easy to find library for connection in all programming language.

Topology:
![internal client (bashCoin.sh) - server - external client](https://github.com/aze2201/bashCoin/blob/main/data/TopologyBashCoin_v1.png)


It can do:
- Find internal socket id which is executing bashCoin.sh
- Return result to who requested. 

Remain:
- Local broadcasting for notification (127.0.0.1)


```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/aze2201/bashCoin/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
