#!/usr/bin/python
from websocket_server import WebsocketServer
import threading
import time
import json
import socket
import logging

import subprocess

threads = []
clients = {}

def client_left(client, server):
    msg = {'message':"client left"}
    try:
        clients.pop(client['id'])
    except:
        print ("Error in removing client %s" % client['id'])
    for cl in clients.values():
        server.send_message(cl, str(msg))
    #server.send_message(clients[1],str(clients))

def client_left1(client, server):
    msg = "Client (%s) left" % client['id']
    try:
        clients.pop(client['id'])
    except:
        print ("Error in removing client %s" % client['id'])
    #for cl in clients.values():
    msg={"command":"removeClient","socketID":client['id']}
    destination=getRoot()
    print ("destination is : "+str(destination))
    msg.update({'socketID':client['id']})
    for cl in clients:
        if cl == int(destination):
            cl = clients[cl]
            server.send_message(cl, str(msg).encode('utf-8'))


# new client i gonder servere
def new_client(client, server):
    msg = "New client (%s) connected" % client['id']
    msg=clients
    #for cl in clients.values():
        #server.send_message(cl, msg)
        #print "Bu da client type: "+str(type(cl))+", and client: "+str(cl)
    clients[client['id']] = client
    print ("Connect olanlar: "+str(clients))

def getRoot():
    result=''
    for i in clients:
        if clients[i]['address'][0]=='127.0.0.1':
            result=i
    #return int(result)
    return 1



def message_received(client, server, message):
    cl = clients[client['id']]
    try:
        json.loads(message)
        msg=json.loads(str(message).encode('utf-8'))
        if msg['command'] == 'listNewBlock':
            ## {'command':'listNewBlock','status':'0','error':'0', 'result':{'blockList': ["17.blk.solved","16.blk.solved","15.blk.solved"]}
            # {"command":"listNewBlock","afterPostedBlockID":"14"}
            lastPostedBlockID=msg['afterPostedBlockID']
            res = subprocess.run(['./bashCoin.sh', 'listNewBlock', lastPostedBlockID], capture_output=True, text=True)
            res=res.stdout.replace("\'", "\"")
            #res=json.loads(str(res).encode('utf-8'))
            server.send_message(cl, str(res))
        if msg['command']=='downloadBlocks':
            print ('Download blocks with Base64, FUTURE CHANGE TO SFTP by Public KEY add')
        if msg['command']=='gossipBlockInfo':
            print ('read Data, put to TEMP, VALIDATE blocks, VALIDATE transaction inside and sign, ADD to BLOCKCHAIN')
        if msg['command'] == 'nodeList':
            # THIS IS FOR CLIENTS
            #server.send_message(cl, str(clients))
            emptyList={'addresses':[]}
            for i in clients:
                emptyList['addresses'].append(clients[i]['address'][0])
            emptyList['status']='0'
            emptyList['command']='nodeList'
            server.send_message(cl, str(emptyList).encode('utf-8'))
        if msg['command']=='getPublisedhInfo':
            if msg['typeOfInfo']=='getPublishedBlock':
                print ('execute Add block')
            if msg['command']=='getPublishedTransaction':
                print ('this message will push directly to blk files. ! from coming, May be Node info also in BLK file?')
    except Exception as err:
        server.send_message(cl, str(message).encode('utf-8'))

#server = WebsocketServer(host='0.0.0.0',port=8001)
server = WebsocketServer(host='0.0.0.0',port=8001,key="/root/peer2peer/cert/key.pem", cert="/root/peer2peer/cert/cert.pem",loglevel=logging.DEBUG)
server.set_fn_client_left(client_left1)
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.run_forever()
