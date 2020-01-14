#!/usr/bin/env python3
#
# BSD 2-Clause License

from serial.tools import list_ports

from fastboot import fastboot_proto

def show_ports():
    # to verify if there is no serial port
    portinfos = list_ports.comports()
    ports = [x.device for x in portinfos]
    print(ports)
    print([x.device for x in list_ports.comports()])

def tcp_server(port):
    import socket
    import sys
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', port)
    print('bind port %d' % port)
    sock.bind(server_address)

    sock.listen(1)

    connection_no = 0;
    
    while True:

        # Wait for a connection
        print('wait connection')
        connection, client_address = sock.accept()
        try:
            #print("connected with %s" % client_address)
            no = connection_no;
            connection_no = connection_no + 1
            print("connected %d" % no)
            fb = fastboot_proto(connection)
            while fb.proc_cmd():
                pass
        
        except ConnectionResetError:
            del fb
        
        finally:
            # Clean up the connection
            connection.close()
            
if __name__ == "__main__" :
    #show_ports()

    tcp_server(5005)
