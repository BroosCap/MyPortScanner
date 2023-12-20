import socket

def portScanner():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    splitler = ["-"," ",","]
    host = input("Taramak istediğiniz IP : ")
    port = input("Taranacak port yada port aralığı : ")
    open_ports = []
    portfirst, portlast = "",""
    if any(split_char in port for split_char in splitler):
        portfirst, portlast = next((port.split(split_char) for split_char in splitler if split_char in port), (port, port))
        portfirst, portlast = int(portfirst), int(portlast)
    else:
        port = int(port)

    if portfirst and portlast is not None:
        for port in range(portfirst, portlast+1):
            if s.connect_ex((host, port)):
                continue
            else:
                open_ports.append(port)
                print(f"{port}  portu AÇIK")
        s.close()
        print("Eğer hiçbir port gözükmüyorsa hedef ip nin filtrelendiği düşünülebilir.\nBunun sonucu olarak gizli mod gereklidir.(gelecek)")
    else:
        if s.connect_ex((host, port)) == 0:
            open_ports.append(port)
            print(f"{port} portu AÇIK")
        else:
            print(f"{port} portu KAPALI")
portScanner()
