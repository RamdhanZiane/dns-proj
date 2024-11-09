#!/bin/bash

# Ensure bind user owns all required directories
chown -R bind:bind /etc/bind /var/cache/bind /var/lib/bind /var/run/named
chmod -R 755 /etc/bind /var/cache/bind /var/lib/bind /var/run/named

# Create and set permissions for config files
touch /etc/bind/zones.conf
touch /etc/bind/rndc.key
chown bind:bind /etc/bind/zones.conf /etc/bind/rndc.key
chmod 644 /etc/bind/zones.conf /etc/bind/rndc.key

# Configure bind
cat > /etc/bind/named.conf <<EOF
options {
    directory "/var/cache/bind";
    listen-on { 10.142.0.2; };
    listen-on-v6 { none; };
    allow-query { any; };
    recursion no;
    dnssec-validation auto;
    auth-nxdomain no;
};

include "/etc/bind/zones.conf";
EOF

chown bind:bind /etc/bind/named.conf
chmod 644 /etc/bind/named.conf

# Start named as bind user
exec su -s /bin/bash bind -c '/usr/sbin/named -g -c /etc/bind/named.conf'