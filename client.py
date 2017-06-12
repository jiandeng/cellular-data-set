import sys, socket, random, datetime


so = socket.socket()

print 'connecting ...',
begin = datetime.datetime.now()
so.connect(('tcp.druidtech.cn', 9528))
end = datetime.datetime.now()
print 'connected in {}'.format(end - begin)

data = 'A' * 1023 + '\n'
for i in range(5):
    print 'sending ...',
    begin = datetime.datetime.now()
    so.sendall(data)
    end = datetime.datetime.now()
    print 'sent in {}'.format(end - begin)
    print 'receiving ...',
    begin = datetime.datetime.now()
    d = so.recv(1024)
    end = datetime.datetime.now()
    print 'received in {}'.format(end - begin)
    #  print d

