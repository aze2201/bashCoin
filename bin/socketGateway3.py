#!/usr/bin/python
from websocket_server import WebsocketServer
import threading
import time
import json
import socket
import logging
import traceback


threads = []
clients = {}

#   {"command":"mine","appType":"wallet"} / {"command":"mine","appType":"miner","messageType":"direct"}
#   {"command":"notification","messageType":"direct"}
#   {"command":"checkbalance","ACCTNUM":"50416596951b715b7e8e658de7d9f751fb8b97ce4edf0891f269f64c8fa8e034","messageType":"direct"}
#   {"command":"listNewBlock","fromBlockID":70,"messageType":"direct"}
#   {"command":"getTransactionMessageForSign","messageType":"direct","SENDER":"50416596951b715b7e8e658de7d9f751fb8b97ce4edf0891f269f64c8fa8e034","RECEIVER":"b1bd54c941aef5e0096c46fd21d971b3a3cf5325226afb89c0a9d6845a491af6","AMOUNT":5,"FEE":3,"DATEEE":"202111121313"}



def client_left(client, server):
    msg = {'message':"client left"}
    try:
        clients.pop(client['id'])
    except:
        print ("Error in removing client %s" % client['id'])
    for cl in clients.values():
        server.send_message(cl, str(msg))

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
    locals=[]
    for i in clients:
        if clients[i]['address'][0]=='127.0.0.1':
            #result=i
            #return int(result)
            locals.append(i)
    return locals



def WhereBashCoin(jsonData,serchKey,valueIs,printKeyValue):
    ## This function return client ID of bashCoin.sh connection. It can be done by secret
    ## WhereBashCoin(clients,'destinationSocketBashCoin',<yes>,'id')
    for i in clients:
        if serchKey in jsonData[i]:
            if jsonData[i][serchKey]==str(valueIs):
                return jsonData[i][printKeyValue]


def msg_received(client, server, msg):
    # Handle messages routing between clients
    if msg != "":
        try:
            msg=json.loads(str(msg).encode('utf-8'))
            ## this is inital for communication_pipe client
            if 'destinationSocketBashCoin' in msg:
                client['destinationSocketBashCoin']=msg['destinationSocketBashCoin']
            if client['id'] in getRoot():
            ################################# MESAGE FROM LOCALHOST  #################################
                if 'destinationSocket' in msg:
                    # this message comes from bashCoin.sh. Becasue SH script sets destinationSocket.
                    destination=msg['destinationSocket']
                else:
                    if msg['messageType']=='broadcast':
                        ## MAKE THIT BY SECRET FILE CODE
                        # python3 wsdump.py  -r --text '{"command":"nothing","appType":"nothing","destinationSocketBashCoin":"yes"}' ws://127.0.0.1:8001
                        for i in clients:
                            if clients[i]['id'] != WhereBashCoin(clients,'destinationSocketBashCoin','yes','id'):
                                server.send_message(clients[i], str(msg).replace("u'","'").replace("'","\""))
                    else:
                        destination=WhereBashCoin(clients,'destinationSocketBashCoin','yes','id')
                        msg.update({'socketID':client['id']})
                cl = clients[int(destination)]
                print ("Iceriden cole "+str(cl)+" message: "+str(msg))
                server.send_message(cl, str(msg).replace("u'","'").replace("'","\""))
                #server.send_message(cl, str(msg))
            else:
            ################################### MESAGE FROM EXTERNAL to LOCAL ########################
                ## SECURITY: put command list from external to internal.
                if msg['command'] in ['help','notification','nothing','listNewBlock','getTransactionMessageForSign','checkbalance','pushSignedMessageToPending','price']:
                    # socketID is message originator always
                    msg.update({'socketID':client['id']})
                    if msg['messageType']=='direct':
                        ## MAKE THIT BY SECRET FILE CODE
                        server.send_message(clients[WhereBashCoin(clients,'destinationSocketBashCoin','yes','id')], str(msg).replace("u'","'").replace("'","\""))
                    if msg['messageType']=='broadcast':
                        ## THIS IS DANGER. NEED TO CONTROL MESSAGE CONTENTN not to Broadcast
                        for i in clients:
                            if clients[i]['id'] != msg['socketID']:
                                print ("mesage getmelidi bura: "+str(clients[i]))
                                server.send_message(clients[i], str(msg).replace("u'","'").replace("'","\""))

        except Exception as e:
            logging.error(traceback.format_exc())
            print ("Problem "+str(msg)+", and PROBLEM is "+str(e))


server = WebsocketServer(host='0.0.0.0',port=8001,loglevel=logging.DEBUG)
#certFile=open('/root/peer2peer/cert/yourkey-without-pass.pem').read()
#server = WebsocketServer(host='0.0.0.0',port=8001,key=certFile, cert="/root/peer2peer/cert/cert.pem",loglevel=logging.DEBUG)
server.set_fn_client_left(client_left1)
server.set_fn_new_client(new_client)
server.set_fn_message_received(msg_received)
server.run_forever()
