#!/bin/bash
# Create required files if they don't exist
touch /etc/bind/zones.conf

# Start named in foreground
exec /usr/sbin/named -g -c /etc/bind/named.conf -u bind
