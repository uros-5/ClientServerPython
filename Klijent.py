
# klijent  data = s.recv(500000)
import socket,pickle,os,time
from concurrent.futures import ThreadPoolExecutor, as_completed
# os.chdir(".\\abc")
s = socket.socket()
s.connect(("192.168.1.3", 5123))


def slanje(poruka):
    s.send(pickle.dumps(poruka))
def ispisLista(lista):
    for i in lista:
        if(i!="Odgovor"):
            print(i+". "+lista[i])

slanje({"Zahtev": "Log"})
while (True):
    data = s.recv(80000)
    data = pickle.loads(data)
    if ("Odgovor" in data):
        if (data["Odgovor"] == "Meni"):
            ispisLista(data)
            poruka = ""
            while (True):
                try:
                    opcija = int(input(">>>"))
                    time.sleep(0.3)
                    poruka = {"Zahtev": data[str(opcija)]}
                    break
                except:
                    if (opcija == 1):
                        print(opcija)
                    continue
            slanje(poruka)
        elif (data["Odgovor"] == "Lista sa fajlovima"):
            ispisLista(data)
            poruka = ""
            while (True):
                try:
                    opcija = int(input(">>>"))
                    time.sleep(0.3)
                    poruka = {"ZahtevF": data[str(opcija)]}
                    break
                except:
                    if (opcija == 1):
                        print(opcija)
                    continue
            slanje(poruka)
            print("Poslata je opcija za fajl.")
            # break
        elif (data["Odgovor"] == "Exit"):
            print("Aplikacija je ugasena.")
            break
        elif (data["Odgovor"] == "Primam fajl"):

            imefajla = data["Ime fajla"]
            print("Klijent je tu.")
            with ThreadPoolExecutor(max_workers=5) as executor:
                v = data["V"]
                data = s.recv(v)
                lista = []
                while(len(data)!=1):
                    lista.append(data)
                    data = s.recv(v)
                print("Duzina liste je :" + str(len(lista)))
                file = open(imefajla, "wb")
                for i in lista:
                    file.write(i)
                print("Primljen je fajl.")
                file.close()
                slanje({"Zahtev": "Log"})
                # break


# fajl = open("nesto.mp4","rb")
# lista = []
# blok = fajl.read(500000)
# while(blok):
#     # print("blok")
#     lista.append(blok)
#     blok =  fajl.read(500000)
# fajl.close()
# print("Fajl je u listi.")
#
# s.send(lista[0])
#
# for i in range(1,len(lista)):
#     s.send(lista[i])
# time.sleep(0.5)
# s.send(str.encode("c"))

# konkretna implementacija
# while(True):
#     data = conn.recv(1024)
#     print(pickle.loads(data))


