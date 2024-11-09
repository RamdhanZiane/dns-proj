#!/bin/bash
set -e

# Ensure proper permissions
chown -R bind:bind /var/run/named /var/cache/bind /var/lib/bind /etc/bind
chmod 755 /var/run/named /var/cache/bind /var/lib/bind /etc/bind

# Create required files if they don't exist
touch /etc/bind/zones.conf
chown bind:bind /etc/bind/zones.conf

# Start named in foreground with proper user
exec /usr/sbin/named -g -u bind -c /etc/bind/named.conf
