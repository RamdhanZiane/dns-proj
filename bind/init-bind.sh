#!/bin/bash
# Create required files if they don't exist
touch /etc/bind/zones.conf
touch /etc/bind/rndc.key

# Ensure the session key directory exists
mkdir -p /var/run/named
chown bind:bind /var/run/named
chmod 755 /var/run/named

# Bind9 listens on internal IP only
echo "options {
    listen-on { 10.142.0.2; };
    // ...existing options...
};" > /etc/bind/named.conf.options

# Start named in foreground
exec /usr/sbin/named -g -c /etc/bind/named.conf -u bind