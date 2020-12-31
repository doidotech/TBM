#!/bin/bash
#-------------------------------------------------------------------------------
#   Copyright (c) 2020 DOIDO Technologies
#
#   Author   : Walter
#   Version  : 1.0.0
#   Location : github
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script gets the bitcoins sync status and echos a word representing the  
# current status.
#-------------------------------------------------------------------------------

# load code software version
source /home/admin/_version.info

## get basic info
source /home/admin/raspiblitz.info 2>/dev/null
source /mnt/hdd/raspiblitz.conf 2>/dev/null

# for oldnodes
if [ ${#network} -eq 0 ]; then
  network="bitcoin"
  litecoinActive=$(sudo ls /mnt/hdd/litecoin/litecoin.conf 2>/dev/null | grep -c 'litecoin.conf')
  if [ ${litecoinActive} -eq 1 ]; then
    network="litecoin"
  else
    network=`sudo cat /home/admin/.network 2>/dev/null`
  fi
  if [ ${#network} -eq 0 ]; then
    network="bitcoin"
  fi
fi

# for oldnodes
if [ ${#chain} -eq 0 ]; then
  chain="test"
  isMainChain=$(sudo cat /mnt/hdd/${network}/${network}.conf 2>/dev/null | grep "#testnet=1" -c)
  if [ ${isMainChain} -gt 0 ];then
    chain="main"
  fi
fi

# set datadir
bitcoin_dir="/home/bitcoin/.${network}"
lnd_dir="/home/bitcoin/.lnd"
lnd_macaroon_dir="/home/bitcoin/.lnd/data/chain/${network}/${chain}net"

# Bitcoin blockchain
btc_path=$(command -v ${network}-cli)
if [ -n ${btc_path} ]; then
  btc_title=$network
  blockchaininfo="$(${network}-cli -datadir=${bitcoin_dir} getblockchaininfo 2>/dev/null)"
  if [ ${#blockchaininfo} -gt 0 ]; then
    btc_title="${btc_title} (${chain}net)"

    # get sync status
    block_chain="$(${network}-cli -datadir=${bitcoin_dir} getblockcount 2>/dev/null)"
    block_verified="$(echo "${blockchaininfo}" | jq -r '.blocks')"
    block_diff=$(expr ${block_chain} - ${block_verified})

    progress="$(echo "${blockchaininfo}" | jq -r '.verificationprogress')"
    sync_percentage=$(echo $progress | awk '{printf( "%.2f%%", 100 * $1)}')

    if [ ${block_diff} -eq 0 ]; then    # fully synced
      sync="OK"
      echo $sync
    elif [ ${block_diff} -eq 1 ]; then   # fully synced
      sync="OK"
      echo $sync
    elif [ ${block_diff} -le 10 ]; then   # <= 2 blocks behind
      sync="NOT"
      echo $sync
    else
      sync="NOT"
      echo $sync
    fi

  else
    btc_line2="NOT RUNNING"
    echo $btc_line2
  fi
fi

