
listNewBlock() {
        commandCode=$(mapFunction2Code ${FUNCNAME[0]})
        fromSocket=$(echo ${jsonMessage}  | jq -r '.socketID')
        fromBlockID=$(echo ${jsonMessage}  | jq -r '.fromBlockID')
        lastBlockInLocal=$(ls -1 $BLOCKPATH| grep "solved$\|blk$"| sort -n -k 1 | tail -n 1| awk -v FS='.' '{print $1}')
        listMissingBlocksID=$(echo $lastBlockInLocal-$fromBlockID | bc)
        if [ $listMissingBlocksID -ge 0 ]; then
                listMissingBlocks=$(ls -1 $BLOCKPATH | grep "solved$\|blk$"| sort -nr -k 1 | head -$listMissingBlocksID)
                #echo "{\"command\":\"listNewBlock\",\"destinationSocket\":\"$fromSocket\",\"status\":\"0\",\"result\":{\"blockList\": [\"blk.pending\",\""$(echo ${listMissingBlocks}| awk 'BEGIN { OFS = "\",\"" } { $1 = $1; print }')\""]}}"
                echo "{\"command\":\"listNewBlock\",\"commandCode\":\"$commandCode\",\"destinationSocket\":\"$fromSocket\",\"status\":\"0\",\"result\":{\"blockList\": [\""$(echo ${listMissingBlocks}| awk 'BEGIN { OFS = "\",\"" } { $1 = $1; print }')\""]}}"
        fi
}


validateNetworkBlockHash() {
        folder=$1
        curr=$(pwd)
        #[ -z $flagByPassFolder ] && flagByPassFolder=1 || flagByPassFolder=0
        flagByPassFolder=1
        cd $folder
        # Check that there are blocks to validate
        getLastBlockToAdd=$(ls -1 $BLOCKPATH| sort -n| tail -n 1)
        for i in `ls -1 *solved| sort -n| tail -n +1`; do
                        if [ "$flagByPassFolder" == "1" ]; then
                            h=$BLOCKPATH/$getLastBlockToAdd
                            flagByPassFolder=0
                        else
                            h=`ls -1 | grep solved$ | sort -n| grep -B 1 $i | head -1`
                        fi
                        PREVHASH=`md5sum $h | cut -d" " -f1`
                        j=`ls -1 | egrep "solved$|blk$" | sort -n| grep -A 1 $i | head -2| grep -v $i | tail -1`
                        CALCHASH=`sed "2c$PREVHASH" $i | md5sum | cut -d" " -f1`
                        REPORTEDHASH=`sed -n '2p' $j`
                        [[ $CALCHASH != $REPORTEDHASH ]] && 
                        #echo "Hash mismatch!  $i has changed!  Do not trust any block after and including $i" && 
                        echo "{\"command\": \"AddBlockFromNetwork\",\"commandCode\":\"$commandCode\",\"messageType\":\"direct\",\"destinationSocket\": \"$fromSocket\",\"status\": \"2\",\"message\":\"Hash mismatch!  $i has changed!  Do not trust any block after and including $i\"}"
                        #exit 1
        done
        cd $curr
}

checkBlockSignature() {
    blockFile=$1
    baseBlockName=$(echo $blockFile| rev | awk -v FS='/' '{print $1}'| rev)
    tempD=$tempRootFolder/$RANDOM
    mkdir $tempD
    cat $blockFile | grep BlockSignPublicKey | awk -v FS=':' '{print $2}'|sed "s/ //"|base64 -d > $tempD/$baseBlockName.pub
    cat $blockFile | grep BlockSignSIGNATURE | awk -v FS=':' '{print $2}'|sed "s/ //"|base64 -d > $tempD/$baseBlockName.sign 
    sed -e '/BlockSignSIGNATURE/,$d' $blockFile > $tempD/$baseBlockName.raw 
    openssl dgst -verify $tempD/$baseBlockName.pub -keyform PEM -sha256 -signature $tempD/$baseBlockName.sign  -binary $tempD/$baseBlockName.raw  > /dev/null
}

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

provideBlocks() {
        commandCode=$(mapFunction2Code ${FUNCNAME[0]})
        fromSocket=$(echo ${jsonMessage}  | jq -r '.socketID')
        blockMessage="["
        for i in $(echo $jsonMessage  | jq -r '.blockList'| jq -c '.[]'| sed "s/\"//g"); do
                blockBase64=$(cat ${BLOCKPATH}/$i | base64 | tr '\n' ' ' | sed 's/ //g')
                blockMessage=$(echo "$blockMessage\"$blockBase64\",")
        done
        # remove last comma
        ${var::${#var}-1}
        blockMessage=$(echo ${blockMessage::${#blockMessage}-1})
        blockMessage=$(echo "$blockMessage]")
        #echo $blockMessage
        #echo "{\"command\": \"provideBlocks\",\"messageType\":\"direct\",\"destinationSocket\": \"$fromSocket\",\"status\": \"0\",\"result\":{\"blockList\":$blockMessage}}"
        echo "{\"command\": \"provideBlocks\",\"commandCode\":\"$commandCode\",\"messageType\":\"direct\",\"destinationSocket\": \"$fromSocket\",\"status\": \"0\",\"result\":{\"blockList\":$blockMessage}}"

        # Get list and parse JSON
        # if 30% then provide message to download full copy (optional)
}

AddBlockFromNetwork() {
        commandCode=$(mapFunction2Code ${FUNCNAME[0]})
        # get file by BASE64 format.
        fromSocket=$(echo ${jsonMessage}  | jq -r '.socketID')
        #
        blocksTeamp=$tempRootFolder/block_$RANDOM
        mkdir -p $blocksTeamp
        count=0
        ERROR=0
        for newBloks in  $(echo $jsonMessage | jq -r '.result' | jq -r '.blockList' | jq -c .[]);
        do
                let " count = $count + 1 "
                echo $newBloks |sed "s/\"//g"| base64 -d > $blocksTeamp/$count.solved
                BlockID=$(cat $blocksTeamp/$count.solved| grep BLOCKID | awk -v FS=':' '{ print $2}'| sed "s/ //g")
                [ ${#BlockID} -ne 0 ] && mv $blocksTeamp/$count.solved $blocksTeamp/$BlockID || mv $blocksTeamp/$count.solved $blocksTeamp/$count.tmp.unsolved && BlockID="$count.tmp.unsolved" && continue
                [ $(echo ${BlockID}| awk -v FS='.' '{print $3}') == "solved" ] && checkBlockSignature $blocksTeamp/$BlockID.solved
                if [ $? -eq 0 ]; then
                    cat $blocksTeamp/$BlockID |  grep '^TX' |while read line; do
                        validateTransactionMessage $line
                        if [ $? -ne 0 ]; then
                            echo "{\"command\":\"AddBlockFromNetwork\",\"messageType\":\"direct\",status\":"2",\"message\":\"Cheating in chain, transaction issue in $BlockID.solved\"}"
                            let " ERROR = $ERROR + 1 "
                            break
                        fi
                    done
                else
                    echo "{\"command\":\"AddBlockFromNetwork\",\"messageType\":\"direct\",\"status\":"2",\"message\":\"Cheating in chain, block sign issue\"}"
                    let " ERROR = $ERROR + 1 "
                    break
                fi
        done
        if [ $ERROR -gt 0 ]; then
            exit 1
        else
            maxIDcurrent=$(ls -1 $blocksTeamp | grep "\.solved$" | sort -n | awk -v FS='.blk.solved' '{print $1+1}' )
            mv $blocksTeamp/1.tmp.unsolved $blocksTeamp/$maxIDcurrent.blk
            firstFileNetwID=$(ls -1 $blocksTeamp| sort -n| grep "solved$\|blk$" | head -1| awk -v FS='.blk' '{print $1}')
            lastFileCurrIDplus1=$(ls -1 $BLOCKPATH| grep solved|sort -n| tail -n 1| awk -v FS='.blk.solved' '{print $1+1}')
            if [ $firstFileNetwID == $lastFileCurrIDplus1 ]; then
                #echo "{\"command\":\"AddBlockFromNetwork\",\"messageType\":\"direct\",\"status\":"0",\"destinationSocket\":\"$fromSocket\"}"
                validateNetworkBlockHash "$blocksTeamp"
                mv $blocksTeamp/*blk* $BLOCKPATH/
                echo "{\"command\":\"AddBlockFromNetwork\",\"messageType\":\"direct\",\"status\":"0",\"destinationSocket\":\"$fromSocket\"}"
                # BROADCAST to others about this ifo
                echo "{\"command\":\"AddBlockFromNetwork\",\"messageType\":\"direct\",\"status\":"0",\"message\":\"got new block\",\"destinationSocket\":\"$fromSocket\"}"
                echo "{\"command\":\"notification\",\"commandCode\":\"$commandCode\",\"messageType\":\"broadcast\",\"status\":"0",\"message\":\"got new block\"}"

            else
                echo "{\"command\":\"AddBlockFromNetwork\",\"messageType\":\"direct\",\"status\":"2",\"destinationSocket\":\"$fromSocket\",\"message\":\"Folder:$blocksTeamp, firstFileNetwID=$firstFileNetwID and lastFileCurrIDplus1=$lastFileCurrIDplus1 Chain ID $BlockID is not matching\"}"
            fi
        fi
}