mapFunction2Code () {
        ######################################################################################################
        #                       2021.11.22
        # This function designed to return function code.
        # this function will be used on Notification. in "notification" command bashCoin.sh don't do anything.
        # because of command bashCoin return command itself on result. 
        # But code will help us to execute some action.

        funcName=$1
        case "$funcName" in 
                mine)
                                code=100
                                ;;
                mineGenesis)
                                code=101
                                ;;
                checkAccountBal)
                                code=200
                                ;;
                getTransactionMessageForSign)
                                code=201
                                ;;
                pushSignedMessageToPending)
                                code=202
                                ;;
                AddBlockFromNetwork)
                                code=302
                                ;;
                listNewBlock)
                                code=300
                                ;;
                provideBlocks)
                                code=301
                                ;;

                *)
                                code=000
                                ;;
        esac
        echo $code
}
