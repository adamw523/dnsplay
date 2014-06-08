import socket
from dnslib import A, DNSHeader, DNSRecord, DNSQuestion, RR

ctr = 252

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0',8053))

while True:
    # Wait for client connection
    data, client = server.recvfrom(8192)
    # Parse and print request

    request = DNSRecord.parse(data)
    qname = request.q.qname
    _id = request.header.id

    print 'got request qname:', qname

    c = (ctr / 255)
    d = (ctr % 255)

    resp_ip = "24.112.%s.%s" % (c, d)

    reply = DNSRecord(DNSHeader(id=_id, qr=1, aa=1, ra=1),
            q=request.q,
            a=RR(qname, rdata=A(resp_ip)))

    print 'sending response', resp_ip

    server.sendto(reply.pack(), client)

    ctr += 1
