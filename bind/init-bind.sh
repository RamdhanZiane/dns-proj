#!/bin/bash

# Ensure proper permissions on startup
chown -R bind:bind /var/cache/bind /var/run/named /var/lib/bind /etc/bind
chmod 775 /var/cache/bind /var/run/named /var/lib/bind
chmod 644 /etc/bind/*.conf

# Start named as bind user
exec su -s /bin/bash bind -c '/usr/sbin/named -g -c /etc/bind/named.conf'