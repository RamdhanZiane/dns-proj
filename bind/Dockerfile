FROM ubuntu/bind9:latest

# Create necessary directories with correct permissions
RUN mkdir -p /var/run/named \
    && chown -R bind:bind /var/run/named \
    && chmod 775 /var/run/named \
    && mkdir -p /var/cache/bind \
    && chown -R bind:bind /var/cache/bind \
    && chmod 775 /var/cache/bind \
    && mkdir -p /var/lib/bind \
    && chown -R bind:bind /var/lib/bind \
    && chmod 775 /var/lib/bind \
    && mkdir -p /etc/bind \
    && chown -R bind:bind /etc/bind \
    && chmod 775 /etc/bind

COPY named.conf /etc/bind/
COPY named.conf.options /etc/bind/
COPY zones.conf /etc/bind/

RUN chown -R bind:bind /etc/bind && chmod 644 /etc/bind/*

EXPOSE 53/tcp
EXPOSE 53/udp

CMD ["/usr/sbin/named", "-g", "-c", "/etc/bind/named.conf", "-u", "bind"]
