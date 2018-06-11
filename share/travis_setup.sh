#!/bin/bash
set -evx

mkdir ~/.hashrentalcoincore

# safety check
if [ ! -f ~/.hashrentalcoincore/.hashrentalcoin.conf ]; then
  cp share/hashrentalcoin.conf.example ~/.hashrentalcoincore/hashrentalcoin.conf
fi
