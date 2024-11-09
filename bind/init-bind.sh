#!/bin/bash
# Create required files if they don't exist
touch /etc/bind/zones.conf

# Ensure the session key directory exists
mkdir -p /var/run/named
chown bind:bind /var/run/named
chmod 755 /var/run/named

# Start named in foreground
exec /usr/sbin/named -g -c /etc/bind/named.conf -u bind