#!/usr/bin/env bash

systemctl stop dnsmasq
systemctl stop hostapd
systemctl disable hostapd
