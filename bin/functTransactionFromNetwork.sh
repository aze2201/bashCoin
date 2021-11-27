validateTransactionMessage() {
        ## ADD EACH TRANSCATION ACCOUNT CHECK (historical )
        txMessage=$1
        randomFolder=$RANDOM
        tempFolder="$tempRootFolder/$randomFolder"
        mkdir $tempFolder
        echo ${txMessage}| awk -v FS=':' '{print $1":"$2":"$3":"$4":"$5":"$6}' > $tempFolder/${randomFolder}_transaction.msg
        echo ${txMessage}| awk -v FS=':' '{print $7}'| base64 -d > $tempFolder/${randomFolder}_transaction.pub
        echo ${txMessage}| awk -v FS=':' '{print $8}'| base64 -d > $tempFolder/${randomFolder}_transaction.sig
        openssl dgst -verify $tempFolder/${randomFolder}_transaction.pub -keyform PEM -sha256 -signature $tempFolder/${randomFolder}_transaction.sig -binary $tempFolder/${randomFolder}_transaction.msg > /dev/null
}


pushSignedMessageToPending() {
    ##########################################################################################
    ## from WALLET                                                                          ##
    ## 1. need to get message                                                               ##
    ## 2. add TX:Hash sha256 (message)                                                      ##
    ## 3. Sign and send back                                                                ##
    ##########################################################################################
    commandCode=$(mapFunction2Code ${FUNCNAME[0]})
    fromSocket=$(echo ${jsonMessage}  | jq -r '.socketID')
    commandCode=$(mapFunction2Code ${FUNCNAME[0]})
    forReciverData=$(echo ${jsonMessage} | jq -r '.result' | jq -r '.forReciverData')
    forSenderData=$( echo ${jsonMessage} | jq -r '.result' | jq -r '.forSenderData')
    ## here we can validate it first before pushing to Pending Transaction
    validateTransactionMessage $forReciverData && validateTransactionMessage $forSenderData
    echo "$forReciverData" >> blk.pending      && echo "$forSenderData"  >> blk.pending
    if [ $? -eq 0 ]; then
        echo "{'command':'pushSignedMessageToPending',\"commandCode\":\"$commandCode\",'status':0,\"messageType\":\"direct\",\"destinationSocket\":$fromSocket,\"commandCode\":\"$commandCode\"}"
        echo "{'command':'notification','status':0,\"commandCode\":\"$commandCode\",\"messageType\":\"broadcast\",\"exceptSocket\":$fromSocket,\"commandCode\":\"$commandCode\"}"
    fi
}

