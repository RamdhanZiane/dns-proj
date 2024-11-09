FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y bind9 bind9utils && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/run/named && \
    chown -R bind:bind /var/run/named && \
    chmod 775 /var/run/named

# Create initial zones.conf
RUN touch /etc/bind/zones.conf && \
    chown bind:bind /etc/bind/zones.conf

EXPOSE 53/udp 53/tcp

# Fix permissions and run named
CMD ["sh", "-c", "chown -R bind:bind /etc/bind /var/cache/bind /var/lib/bind && /usr/sbin/named -g -c /etc/bind/named.conf -u bind"]
