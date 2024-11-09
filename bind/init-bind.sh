#!/bin/bash
# Create required files if they don't exist
touch /etc/bind/zones.conf
touch /etc/bind/rndc.key

# Ensure the session key directory exists
mkdir -p /var/run/named
chown bind:bind /var/run/named
chmod 755 /var/run/named

# Bind9 listens on internal IP only
cat <<EOF > /etc/bind/named.conf.options
options {
    directory "/var/cache/bind";

    // Listen on the internal Docker network IP
    listen-on { 10.142.0.2; };
    listen-on-v6 { none; };

    allow-query { any; };
    recursion no;

    dnssec-validation auto;

    auth-nxdomain no;    # conform to RFC1035
    listen-on { any; };
};
EOF

# Include zones configuration
cat <<EOF >> /etc/bind/named.conf
include "/etc/bind/zones.conf";
EOF

# Start named in foreground
exec /usr/sbin/named -g -c /etc/bind/named.conf -u bind