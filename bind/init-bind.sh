#!/bin/bash
# Create required files if they don't exist
touch /etc/bind/zones.conf

# Set permissions for /run/named
mkdir -p /run/named
chown -R bind:bind /run/named
chmod 775 /run/named

# Start named in foreground
exec /usr/sbin/named -g -c /etc/bind/named.conf -u bind
