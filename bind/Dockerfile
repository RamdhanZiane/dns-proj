FROM ubuntu:20.04

# Install BIND9 and necessary utilities
RUN apt-get update && apt-get install -y bind9 bind9utils bind9-doc dnsutils && rm -rf /var/lib/apt/lists/*

# Create necessary directories with proper permissions
RUN mkdir -p /var/run/named \
    /var/cache/bind \
    /var/lib/bind \
    /etc/bind \
    && chown -R bind:bind /var/run/named /var/cache/bind /var/lib/bind /etc/bind \
    && chmod 775 /var/run/named /var/cache/bind /var/lib/bind /etc/bind

# Copy configuration files
COPY named.conf /etc/bind/
COPY named.conf.options /etc/bind/
COPY zones.conf /etc/bind/

# Generate rndc key
RUN rndc-confgen -a \
    && chown bind:bind /etc/bind/rndc.key \
    && chmod 640 /etc/bind/rndc.key

# Copy and set permissions for initialization script
COPY init-bind.sh /bind/
RUN chmod 755 /bind/init-bind.sh \
    && chown bind:bind /bind/init-bind.sh

# Set permissions for config files
RUN chown -R bind:bind /etc/bind \
    && chmod 644 /etc/bind/*.conf

EXPOSE 53/tcp 53/udp 953/tcp

# Don't switch to bind user here - will be handled in init script
ENTRYPOINT ["/bind/init-bind.sh"]
