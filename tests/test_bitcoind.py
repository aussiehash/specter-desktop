import logging
from cryptoadvance.specter.helpers import which

def test_bitcoinddocker_running(caplog, docker, request):
    caplog.set_level(logging.INFO)
    caplog.set_level(logging.DEBUG,logger="cryptoadvance.specter")
    requested_version = request.config.getoption("--bitcoind-version")
    if docker:
        from cryptoadvance.specter.bitcoind import BitcoindDockerController
        my_bitcoind = BitcoindDockerController(rpcport=18999, docker_tag=requested_version) # completly different port to not interfere
    else:
        try:
            which("bitcoind")
        except:
            # Skip this test as bitcoind is not available
            # Doesn't make sense to print anything as this won't be shown
            # for passing tests
            return
        from cryptoadvance.specter.bitcoind import BitcoindPlainController
        # This doesn't work if you don't have a bitcoind on the path
        my_bitcoind = BitcoindPlainController() # completly different port to not interfere    
    #assert my_bitcoind.detect_bitcoind_container() == True
    rpcconn = my_bitcoind.start_bitcoind(cleanup_at_exit=True)
    requested_version = request.config.getoption("--bitcoind-version")
    assert my_bitcoind.version() == requested_version
    assert rpcconn.get_cli() != None
    assert rpcconn.get_cli().ipaddress != None
    rpcconn.get_cli().getblockchaininfo()
    # you can use the testcoin_faucet:
    random_address = "mruae2834buqxk77oaVpephnA5ZAxNNJ1r"
    my_bitcoind.testcoin_faucet(random_address, amount=25, mine_tx=True)
    my_bitcoind.stop_bitcoind()


    