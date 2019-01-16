from socket import *
import thread

BUFF = 1024
HOST = "192.168.1.150"
PORT = 1911
sysconfig='''fox a 0 -1 fox hello
{
fox.version=s:1.0.1
id=i:122
hostName=s:10.17.40.40
hostAddress=s:10.17.40.40
app.name=s:Station
app.version=s:3.8.213
vm.name=s:Java HotSpot(TM) Client VM
vm.version=s:1.5.0_81-b06
os.name=s:QNX
os.version=s:6.4.1
station.name=s:Honeywell
lang=s:en
timeZone=s:EST5EDT;-18000000;3600000;02:00:00.000,wall,march,8,on or after,sunday,undefined;02:00:00.000,wall,november,1,on or after,sunday,undefined
hostId=s:Qnx-NPM6-0000-16A3-8210
vmUuid=s:11e8e9a6-0b40-571a-0000-00000000a096
brandId=s:FacExp
sysInfo=o:bog 61[<bog version="1.0">
<p m="b=baja" t="b:Facets" v=""/>
</bog>
]
authAgentTypeSpecs=s:fox:FoxUsernamePasswordAuthAgent
};;
'''

def gen_response():
	global sysconfig
	return sysconfig

def response(clientsock, addr):
	while 1:
		data = clientsock.recv(BUFF)
		if not data: break
		print repr(addr) + ' recv:' +repr(data)
		clientsock.send(gen_response())
		print repr(addr) + 'sent: ' +repr(gen_response())
		if "close" == data.rstrip(): break
	clientsock.close()
	print addr, "connection closed " 

if __name__=='__main__':
	ADDR = (HOST,PORT)
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serversock.bind(ADDR)
	serversock.listen(5)
	while 1:
		print 'waiting for connection... on port ', PORT
		clientsock, addr = serversock.accept()
		print '...connected from: ', addr
		thread.start_new_thread(response, (clientsock, addr))
