import socket
import os
import time
import threading

#Buffer size
buffer_size = 1024

#Lists
clients = []
clients_1 = []
servers = []
message_list =[]

class Server(threading.Thread):
    def __init__(self, server_socket, received_data, client_address):
        super(Server, self).__init__()
        self.server_socket = server_socket
        self.received_data = received_data
        self.client_address = client_address
    

    # Override run method
    def run(self):
        # Message to be sent to client
        message = 'Hi ' + self.client_address[0] + ':' + str(self.client_address[1]) + '. This is server ' + str(os.getpid())
        # Send message to client
        self.server_socket.sendto(str.encode(message), self.client_address)
        #print('Sent to client: ', message)

def client_handler():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Server application IP address and port
    server_address = socket.gethostbyname("")
    server_port = 10001
    server_addr=(server_address,server_port)
    #servers.append(server_addr)
    
    # Bind socket to address and port
    server_socket.bind((server_address, server_port))
    print('Server up and running at {}:{}'.format(server_address, server_port))

    while True:
        try:
            # Receive message from client
            data, address = server_socket.recvfrom(buffer_size)
            recv_1 = (data.decode()).split(':')[0]
            recv_2 = (data.decode()).split(':')[1]
            recv_3 = (data.decode()).split('>>')[0]
            
            
            print (time.ctime(time.time()) + "> " + str(recv_1) + ": " + str(recv_2))
           
            c = 'left the chat' 
            d = 'Hi. A Server already existing. My IP is'
            message1 = str(recv_1) + ": " + str(recv_2)
            message2 = 'S>>'+str(recv_1) + ": " + str(recv_2)
            message_list.append(message1)
            print(message_list)
            
            if address not in clients and recv_1!=d and recv_3!='S':
                clients.append(address)  
                print('Client list: ',clients)
                t = Server(server_socket, data, address)
                t.start()
                t.join()
            elif address not in servers and recv_1==d:
                servers.append(address)
                print('Server1 list: ',servers)
            else:
                pass
            
            if c == recv_2:
                clients.remove(address)
                #clients_1.remove(address)
                #print(clients)
                #print(clients_1)
            
               
            for client in clients:
                if client!=address:# tried this for broadcasting to others not c1
                    #message1 = str(recv_1) + ": " + str(recv_2)
                    #message_list.append(message1)
                    #print(message_list)
                    server_socket.sendto(message1.encode(), client)
            
            for server in servers:
                server_socket.sendto(message2.encode(), (server,10001))
                             
        except:
            pass
  
    
def broadcast():
   # Listening port
   BROADCAST_PORT = 5973
   BROADCAST_IP = '192.168.1.255'
   
   # Local host information
   MY_HOST = socket.gethostname()
   MY_IP = socket.gethostbyname("")
   
   # Create a UDP socket
   listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   # Set the socket to broadcast and enable reusing addresses
   listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
   listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   # Bind socket to address and port
   listen_socket.bind((MY_IP, BROADCAST_PORT))
   
   print("Listening to broadcast messages")

   while True:
      
           data, addr = listen_socket.recvfrom(buffer_size)
           recv_3 = (data.decode()).split(':')[1]
           a = 'I want to join the chat.'
           b = 'I want to join the server_group.'
          
           if a == recv_3:
               client_addr = addr
               if client_addr not in clients_1:
                   message = MY_IP + ' send a broadcast'
                   # Send message on broadcast address
                   listen_socket.sendto(str.encode(message), (client_addr))
                   clients_1.append(client_addr)
           if b == recv_3:
               server_addr = addr[0]
               #clients_1.append(client_addr)
               #print (clients_1)
               if server_addr not in servers:
                   servers.append(server_addr)
                   print('Server list:',servers)
                   listen_socket.sendto(str.encode('Hi. A Server already existing. My IP is: '+MY_IP), (server_addr,10001))
          

    

def broadcast_s():
    # Local host information
    MY_HOST = socket.gethostname()
    MY_IP = socket.gethostbyname("")
    
    
    # Create a UDP socket
    sendserver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set the socket to broadcast and enable reusing addresses
    sendserver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sendserver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Broadcast address and port
    BROADCAST_IP = '192.168.1.255'
    BROADCAST_PORT = 5973

    # Send broadcast message
    message = MY_IP + ':I want to join the server_group.'
    # Send message on broadcast address
    sendserver_socket.sendto(str.encode(message), (BROADCAST_IP, BROADCAST_PORT))


    

if __name__ == "__main__":
    
    #t=threading.Timer(1,broadcast)
    #client_handler()
    threading.Thread(target=broadcast_s).start()
    threading.Thread(target=broadcast).start()
    #t.start()
    threading.Thread(target=client_handler).start()

        


