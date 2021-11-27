#!/usr/bin/python
from websocket_server import WebsocketServer
import threading
import time
import json
import socket
import logging

import subprocess
import hashlib
import datetime

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
    return result


## LOCAL NETWORK ALWAYS BROADCASTING
def message_received1(client, server, message):
    selfID=getRoot()
    cl = clients[client['id']]
    try:
        message['time']
        message=json.loads(message)
        clients[client['id']]['account']=message['account']
        print ("musteriler: "+str(clients))
        #destination=getRoot()
        if cl['address'][0] != '127.0.0.1' :
            server.send_message(clients[selfID], str(message).encode("utf-8"))
        else:
            for  i in clients:
                if clients[i]['address'][0] != '127.0.0.1':
                    server.send_message(clients[i], str(message).encode("utf-8"))
    except Exception as err:
        print ("nothing")
        #server.send_message(cl, str(message).encode("utf-8"))

def message_received2(client, server, message):
    selfID=getRoot()
    cl = clients[client['id']]
    try:
        message=json.loads(message)
        ## WHOEVER SENDS it goes to "REMOTE" LOCAL NODE
        if cl['address'][0] != '127.0.0.1' :
            message['fromID']=client['id']
            server.send_message(clients[selfID], str(message).encode("utf-8"))
        else:
            ################################################################################################### 
            # if message type is not broadcast then send only to someone. Client dont know to whom to send
            # SAMPLE: {"command":"listNewBlock","afterPostedBlockID":"14","messageType":"direct","fromID":"4"}
            ###################################################################################################
            if message['messageType'] != 'broadcast':
                server.send_message(clients[message['fromID']], str(message).encode("utf-8"))
            ################################################################################################### 
            # if message type is broadcast then send to all external connected
            # SAMPLE: {"command":"listNewBlock","afterPostedBlockID":"14","messageType":"broadcast"}
            ###################################################################################################
            else:
                for  i in clients:
                    if clients[i]['address'][0] != '127.0.0.1':
                        server.send_message(clients[i], str(message).encode("utf-8"))
    except Exception as err:
        print ("ERRIR is "+str(err))
        #server.send_message(cl, str(message).encode("utf-8"))

def message_received(client, server, message):
    selfID=getRoot()
    cl = clients[client['id']]
    print ("address is cl "+str(cl))
    try:
        message=json.loads(message)
        ## WHOEVER SENDS it goes to "REMOTE" LOCAL NODE
        if message['messageType'] == 'direct' and cl['address'][0] != '127.0.0.1':
            message['fromID']=client['id']
            server.send_message(clients[selfID], str(message).encode("utf-8"))
        if message['messageType'] == 'direct' and cl['address'][0] == '127.0.0.1':
            server.send_message(clients[message['fromID']], str(message).encode("utf-8"))
        ## not too much mandatory
        #if message['messageType'] == 'broadcast' and cl['address'][0] != '127.0.0.1':
        #    for i in clients:
        #        if clients[i]['address'][0] != cl['address'][0] and clients[i]['address'][1] != cl['address'][1]:
        #            server.send_message(clients[i], str(message).encode("utf-8"))
        if message['messageType'] == 'broadcast' and cl['address'][0] == '127.0.0.1':
            for i in clients:
                    if  clients[i]['address'][0] != '127.0.0.1' :
                        server.send_message(clients[i], str(message).encode("utf-8"))
        if message['messageType']=='toID':
            Id=message['ID']
            server.send_message(clients[Id], str(message).encode("utf-8"))
    except Exception as err:
        print ("ERROR is "+str(err))
        server.send_message(cl, str(message).encode("utf-8"))


# server = WebsocketServer(host='0.0.0.0',port=8001)
server = WebsocketServer(host='0.0.0.0',port=8002,key="/root/peer2peer/cert/key.pem", cert="/root/peer2peer/cert/cert.pem",loglevel=logging.DEBUG)
server.set_fn_client_left(client_left1)
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.run_forever()
