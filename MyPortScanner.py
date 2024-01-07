import socket  # Portlarla etkileşime girebilmek için gereken kütüphanedir.
import threading  # Aynı anda birden çok işlem yapabilmeyı sağlar.
import time  # İşlemin kaç saniyede tamamlandığını ölçmeyi sağlar. (isteğe bağlı)
from colorama import Fore  # Yazıları renklendirebilmeyi sağlar. (isteğe bağlı)

# Kullanıcıdan hedef domain adresini alır
HOST = input(f"{Fore.LIGHTWHITE_EX}Domain ismi : ")


# Alınan Domain adresinin geçerli olup olmadığını kontrol eder
def valid_ip():
    try:
        socket.gethostbyname(HOST)
        return True
    except socket.error:
        return False


# Eğer adres geçerliyse HOST_IP değişkenine atar, geçersizse adresin tekrar girilmesi istenir
while True:
    if valid_ip() == 1:
        HOST_IP = socket.gethostbyname(HOST)
        print("Public IP : {}{}{}".format(Fore.LIGHTGREEN_EX, HOST_IP, Fore.LIGHTWHITE_EX))
        break
    else:
        HOST = input(f"{Fore.LIGHTWHITE_EX}Geçersiz domain, Tekrar girin : ")


# Port üzeinde çalışan uygulamayı tespit etmeyi amaçlar
def get_service(port):
    try:
        service = socket.getservbyport(port)
        return service
    except (socket.error, OSError):
        return f"{Fore.LIGHTRED_EX}]{Fore.LIGHTWHITE_EX}"


# Port üzerinde çalışan uygulamanın versiyonunu tespit etmeyi amaçlar
def get_version(port):
    try:
        with socket.create_connection((HOST_IP, port), timeout=0.5) as s:
            data = s.recv(1024)
            version = data.decode('utf-8').strip()
            return f"Version: {version}"
    except (socket.timeout, socket.error, OSError):
        return f"{Fore.LIGHTRED_EX}]{Fore.LIGHTWHITE_EX}"


# Belirli bir portun açık olup olmadığını kontrol eder. Servis ve versiyon fonksiyonları burada kullanılır
def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST_IP, port))
        try:
            service_info = get_service(port)
            version_info = get_version(port)
            print(
                f"{Fore.LIGHTWHITE_EX}port {Fore.LIGHTGREEN_EX}{port}{Fore.LIGHTWHITE_EX} açık- {service_info} - {version_info}")
        except:
            print("port {} açık ".format(port))
    except:
        pass


def port_input():
    portfirst, portlast = "", ""
    splitler = ["-", " ", ","]


# Kullanıcıdan port ya da port aralığı alır, ve sınır koyar
    while True:
        port = input("Taranacak port ya da port aralığı (1-65535) : ")
        if any(split_char in port for split_char in splitler):
            portfirst, portlast = next((port.split(split_char) for split_char in splitler if split_char in port),
                                       (port, port))
            portfirst, portlast = int(portfirst), int(portlast)
            if portfirst <= 0 or portlast >= 65536:
                print(f"Aralık minimum {Fore.LIGHTRED_EX}1{Fore.LIGHTWHITE_EX} ve maximum {Fore.LIGHTRED_EX}65535{Fore.LIGHTWHITE_EX} olabilir.")
            else:
                break
        else:
            port = int(port)
            break


# Aralık şeklinde verildiyse aynı anda birden çok scan_port fonksiyonu başlatır. Tek port ise tek işlemde bitirir
    if portfirst and portlast is not None:
        start_time = time.time()
        try:
            for i in range(portfirst, portlast + 1):
                thread = threading.Thread(target=scan_port, args=[i])
                thread.start()
            end_time = time.time()
            time.sleep(2)
            print("İşlem {:.2f} saniye sürdü.".format(end_time - start_time))
        except:
            print("İşlem durduruldu.")
    else:
        scan_port(port)


port_input()
