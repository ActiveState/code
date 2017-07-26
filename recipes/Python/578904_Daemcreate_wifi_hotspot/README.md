## Daemon to create a wifi hotspot on linux

Originally published: 2014-07-08 04:45:27
Last updated: 2014-07-08 04:45:27
Author: Prahlad Yeri

This recipe is based on Hotspotd, a small linux daemon to create a wifi hotspot on linux. It depends on hostapd for AP provisioning and dnsmasq to assign IP addresses to devices.\n\nHotspotd works by creating a virtual NAT (Network address transation) table between your connected device and the internet using iptables.