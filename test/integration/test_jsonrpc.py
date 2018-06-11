import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from hashrentalcoind import hashrentalcoinDaemon
from hashrentalcoin_config import hashrentalcoinConfig


def test_hashrentalcoind():
    config_text = hashrentalcoinConfig.slurp_config_file(config.hashrentalcoin_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000c2df784fc6839acc754bcad234a2839e5effbdfc0ead7a2ec26eeee4785'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000c2df784fc6839acc754bcad234a2839e5effbdfc0ead7a2ec26eeee4785'

    creds = hashrentalcoinConfig.get_rpc_creds(config_text, network)
    hashrentalcoind = hashrentalcoinDaemon(**creds)
    assert hashrentalcoind.rpc_command is not None

    assert hasattr(hashrentalcoind, 'rpc_connection')

    # hashrentalcoin testnet block 0 hash == 00000c2df784fc6839acc754bcad234a2839e5effbdfc0ead7a2ec26eeee4785
    # test commands without arguments
    info = hashrentalcoind.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert hashrentalcoind.rpc_command('getblockhash', 0) == genesis_hash
