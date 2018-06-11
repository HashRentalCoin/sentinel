import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from hashrentalcoin_config import hashrentalcoinConfig


@pytest.fixture
def hashrentalcoin_conf(**kwargs):
    defaults = {
        'rpcuser': 'hashrentalcoinrpc',
        'rpcpassword': 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEF10',
        'rpcport': 10773,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    hashrentalcoin_config = hashrentalcoin_conf()
    creds = hashrentalcoinConfig.get_rpc_creds(hashrentalcoin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'hashrentalcoinrpc'
    assert creds.get('password') == 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEF10'
    assert creds.get('port') == 7883

    hashrentalcoin_config = hashrentalcoin_conf(rpcpassword='s00pers33kr1t', rpcport=7883)
    creds = hashrentalcoinConfig.get_rpc_creds(hashrentalcoin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'hashrentalcoinrpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 7883

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', hashrentalcoin_conf(), re.M)
    creds = hashrentalcoinConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'hashrentalcoinrpc'
    assert creds.get('password') == 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEF10'
    assert creds.get('port') == 7883


# ensure hashrentalcoin network (mainnet, testnet) matches that specified in config
# requires running hashrentalcoind on whatever port specified...
#
# This is more of a hashrentalcoind/jsonrpc test than a config test...
