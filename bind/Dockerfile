FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y bind9 bind9utils && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/cache/bind && \
    mkdir -p /var/lib/bind && \
    chown -R bind:bind /var/cache/bind && \
    chown -R bind:bind /var/lib/bind && \
    chown -R bind:bind /etc/bind

EXPOSE 53/udp 53/tcp

CMD ["/usr/sbin/named", "-g", "-c", "/etc/bind/named.conf", "-u", "bind"]
