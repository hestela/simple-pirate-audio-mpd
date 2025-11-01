#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "$SCRIPT_DIR/bt-addr"
if [ -z "$addr" ]; then
	echo "ERROR $0: create file $SCRIPT_DIR/bt-addr"
	echo "with contents: addr=YO:UR:BT:AD:DR"
	exit 1
fi

bt_conn_dev=$(bluetoothctl devices Connected)
if [ -z "$bt_conn_dev" ]; then
	# TODO add a retry
	bluetoothctl connect "$addr"
fi

mpd_status=$(systemctl is-active --user mpd.service)
if [ "$mpd_status" != "active" ]; then
	systemctl --user restart mpd.service
fi
