

updateNetworkInfo() {
	## this function will return message to all clients
	message=$1
	commandCode=$(mapFunction2Code ${FUNCNAME[0]})
	test=$(echo $message | jq . )
	if [ $? -eq 0 ]; then
		peers=$(echo $message | jq -r '.peers')
		echo $peers > $FSDATABASE/connections.data 
	fi
	echo "{\"command\":\"notification\",\"commandCode\":\"$commandCode\",\"messageType\":\"broadcast\",\"status\":\"0\", \"timeUTC\":\"$(date -u  +"%Y%m%d%H%M%S")\",\"peers\":$peers}"
}

discoverBootNodes() {
	bootBodeIP="161.97.69.136"
	echo $bootBodeIP
}

discoverSelfNode() {
	selfIp=$(curl http://checkip.amazonaws.com)
	echo $selfIp
}

pingToBootNode() {
	## use python to see route exist. 
	## if route exit do nothing. it means any update can be reached.
	## if not exit Discover again Nodes by boot Peer. May be DNS
	message=$(cat $FSDATABASE/connections.data| jq .)
	if [ $? -eq 0 ]; then
		python2 $ROOTDIR/findPath.py $message $selfIp $bootBodeIP
		ret=$(echo $?)
	fi
	exit $ret
}



