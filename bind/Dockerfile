FROM ubuntu:20.04

# Install BIND9 and necessary utilities
RUN apt-get update && apt-get install -y bind9 bind9utils bind9-doc dnsutils && rm -rf /var/lib/apt/lists/*

# Create necessary directories with correct permissions
RUN mkdir -p /var/run/named \
    && chown -R bind:bind /var/run/named \
    && chmod 755 /var/run/named \
    && mkdir -p /var/cache/bind \
    && chown -R bind:bind /var/cache/bind \
    && chmod 755 /var/cache/bind \
    && mkdir -p /var/lib/bind \
    && chown -R bind:bind /var/lib/bind \
    && chmod 755 /var/lib/bind \
    && mkdir -p /etc/bind \
    && chown -R bind:bind /etc/bind \
    && chmod 755 /etc/bind

# Copy configuration files
COPY named.conf /etc/bind/
COPY named.conf.options /etc/bind/
COPY zones.conf /etc/bind/

# Generate rndc key
RUN rndc-confgen -a -r /dev/urandom

# Copy initialization script
COPY init-bind.sh /bind/init-bind.sh

# Set permissions for config and init script
RUN chown -R bind:bind /etc/bind && chmod 644 /etc/bind/*.conf \
    && chown bind:bind /bind/init-bind.sh \
    && chmod +x /bind/init-bind.sh

# Expose ports for DNS and rndc
EXPOSE 53/tcp
EXPOSE 53/udp
EXPOSE 953/tcp

USER bind

ENTRYPOINT ["/bind/init-bind.sh"]
