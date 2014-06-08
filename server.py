import socket
from dnslib import A, DNSHeader, DNSRecord, DNSQuestion, RR

ctr = 1

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0',8053))

while True:
    data, client = server.recvfrom(2048)

    request = DNSRecord.parse(data)
    qname = request.q.qname
    _id = request.header.id

    print 'got request from:', client[0], 'qname:', qname

    a = 10
    b = (ctr / (255 * 255 + 255))
    c = (ctr / 255) % 255
    d = (ctr % 255)

    resp_ip = "%s.%s.%s.%s" % (a, b, c, d)

    reply = DNSRecord(DNSHeader(id=_id, qr=1, aa=1, ra=1),
            q=request.q,
            a=RR(qname, rdata=A(resp_ip)))

    print 'sending response:', resp_ip

    server.sendto(reply.pack(), client)

    ctr += 1
