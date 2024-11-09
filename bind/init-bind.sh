#!/bin/bash

# Start named directly (already running as bind user)
exec /usr/sbin/named -g -c /etc/bind/named.conf