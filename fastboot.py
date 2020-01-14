#!/usr/bin/env python3
#
# BSD 2-Clause License

from parse import *

# fastboot protocol
#
# https://android.googlesource.com/platform/system/core/+/refs/heads/master/fastboot/

class fastboot_proto:

    def __init__(self, conn):
        self.conn = conn
        print("fastboot parser init")

        self.conn.send("FB01".encode())

        # handshake - check version, disconnect if not match
        bites = self.conn.recv(4)
        msg = bites.decode()
        ver = parse("FB{:o}", msg)
        if ver[0] != 1:
            raise(Exception("unsupported version"))
            self.conn.close()
        else:
            print("hankshake succeeded")

    def fetch_data(self):
    
        bites = self.conn.recv(8)
        size = 0;
        for b in bites:
            size = size * 256 + b

        print("recv size %d" % size)
        bites = self.conn.recv(size)
        return bites

    def send_data(self, msg):
        
        bites = msg.encode()
        l = len(msg)
        arr = bytearray(8)
        
        i = 8
        while l > 0:
            i = i - 1
            arr[i] = l % 256
            l = l // 256
        
        self.conn.send(arr)
        self.conn.send(msg.encode())

    def proc_cmd_getvar(self, var):
    
        print("getvar %s" % var)
        
        if var == "has-slot:img1":
            self.send_data("OKAY")
        elif var == "max-download-size":
            self.send_data("OKAY8192")
        else:
            self.send_data("FAILUnknown variable")

    def proc_cmd_download(self, length):

        bites = length.encode()
        size = 0;
        for b in bites:
            if b >= 97:
                b = b - 97 + 10
            elif b >= 65:
                b = b - 65+ 10
            else:
                b = b - 48
            size = size * 16 + b

        print("total download size %d" % size)
        self.send_data("OKAY" + length)

        if True:
            left = size
            while left > 0:
                bites = self.fetch_data()
                if len(bites) > left:
                    raise(Exception("received more than expected"))
                left = left - len(bites)
        else:
            left = size
            while left > 0:
                if left > 128:
                    bites = self.conn.recv(128)
                else:
                    bites = self.conn.recv(left)
                left = left - len(bites)
    
        self.send_data("OKAY")
        print("download done")

    def proc_cmd_flash(self, partition):

        print("flash %s" % partition)
        self.send_data("OKAY")

    def proc_cmd_erase(self, partition):

        print("erase %s" % partition)
        self.send_data("OKAY")

    def proc_cmd(self):

        bites = self.fetch_data()
        msg = bites.decode()

        # getvar:%s
        # download:%08x
        # upload
        # flash:%s
        # erase:%s
        # boot
        # continue
        # reboot
        # reboot-bootloader

        if msg[:7] == "getvar:":
            self.proc_cmd_getvar(msg[7:])
        elif msg[:9] == "download:":
            self.proc_cmd_download(msg[9:])
        elif msg[:6] == 'erase:':
            self.proc_cmd_erase(msg[6:])
        elif msg[:6] == 'flash:':
            self.proc_cmd_flash(msg[6:])
        else:
            print(msg)
            self.send_data("FAILunknown command")
            
        return True