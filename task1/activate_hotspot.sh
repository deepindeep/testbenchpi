#!/usr/bin/env bash

systemctl enable hostapd
systemctl start dnsmasq
systemctl start hostapd