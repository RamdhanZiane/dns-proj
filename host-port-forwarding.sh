#!/bin/bash
# Redirect external DNS (port 53) to internal IP 10.142.0.2:53
iptables -t nat -A PREROUTING -p tcp -d 34.74.60.217 --dport 53 -j DNAT --to-destination 10.142.0.2:53
iptables -t nat -A PREROUTING -p udp -d 34.74.60.217 --dport 53 -j DNAT --to-destination 10.142.0.2:53

# Allow forwarding
iptables -A FORWARD -p tcp -d 10.142.0.2 --dport 53 -j ACCEPT
iptables -A FORWARD -p udp -d 10.142.0.2 --dport 53 -j ACCEPT
