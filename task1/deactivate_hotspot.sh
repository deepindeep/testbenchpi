#!/usr/bin/env bash

for line in '/^interface\swlan0$/s/^/#/' '/^\tstatic\sip_address=192.168.4.1\/24$/s/^/#/' '/^\tnohook\swpa_supplicant$/s/^/#/'
do
sed -i $line /etc/dhcpcd.conf
done
systemctl stop dnsmasq
systemctl stop hostapd
systemctl disable hostapd
