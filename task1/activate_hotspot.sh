#!/usr/bin/env bash

systemctl stop dnsmasq
systemctl stop hostapd

for line in '/^#interface\swlan0$/s/^#//' '/^#\tstatic\sip_address=192.168.4.1\/24$/s/^#//' '/^#\tnohook\swpa_supplicant$/s/^#//'
do
sed -i $line /etc/dhcpcd.conf
done

for line in '/^#interface=wlan0$/s/^#//' '/^#dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h$/s/^#//'
do
sed -i $line /etc/dnsmasq.conf
done

systemctl enable hostapd
systemctl start dnsmasq
systemctl start hostapd