

def extract():
	import socket
	h_name = socket.gethostname()
	IP_addres = socket.gethostbyname(h_name)
	return [h_name,IP_addres]

if __name__ == '__main__':
	l=extract()
	print("Host Name is:" + l[0])
	print("Computer IP Address is:" + l[1])
