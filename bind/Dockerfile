FROM ubuntu/bind9:latest

# Create required directories with correct permissions
RUN mkdir -p /var/run/named /var/cache/bind /var/lib/bind /etc/bind \
    && chown -R bind:bind /var/run/named /var/cache/bind /var/lib/bind /etc/bind \
    && chmod 755 /var/run/named /var/cache/bind /var/lib/bind /etc/bind

# Copy configuration files
COPY named.conf /etc/bind/
COPY named.conf.options /etc/bind/
COPY named.conf.local /etc/bind/

# Set proper permissions for config files
RUN chown bind:bind /etc/bind/named.conf* \
    && chmod 644 /etc/bind/named.conf*

EXPOSE 53/tcp
EXPOSE 53/udp

# Use custom entrypoint script
COPY init-bind.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/init-bind.sh

CMD ["/usr/local/bin/init-bind.sh"]
