#!/bin/bash
# Create required files if they don't exist
touch /etc/bind/zones.conf


# Create required files if they don't exist
chown bind:bind /var/run/named

chmod 755 /var/run/named

mkdir -p /var/run/named
exec /usr/sbin/named -g -c /etc/bind/named.conf -u bind
chmod 755 /var/run/named

# Start named in foreground
exec /usr/sbin/named -g -c /etc/bind/named.conf -u bind


chown bind:bind /var/run/named
# Start named in foreground
# Ensure the session key directory exists