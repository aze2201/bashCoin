

updateNetworkInfo() {
	## this function will return message to all clients
	message=$1
	test=$(echo $message | jq . )
	if [ $? -eq 0 ]; then
		echo $message > $FSDATABASE/connections.data
	fi
	echo "add this message to broadcast message"
}


pingToBootNode() {
	## use python to see route exist. 
	## if route exit do nothing. it means any update can be reached.
	## if not exit Discover again Nodes by boot Peer. May be DNS
	echo "upingToBootNode"
}

discoverNodeByRootPeer() {
	## Find boot Peer ( may be DNS or Predefined REPO, or IP boot )
	## get Lowest Weight of Nodes and try to Connect
	## Update everyone
	echo "discoverNodeByRootPeer"
}
