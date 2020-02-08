# server data = conn.recv(500000)
import socket,pickle,os,time,os.path
from concurrent.futures import ThreadPoolExecutor, as_completed
# os.chdir(".\\abc")
# os.chdir(".")
s = socket.socket()
s.bind(("192.168.1.3", 5123))
s.listen(5)
conn, addr = s.accept()
def slanje(poruka):
    conn.send(pickle.dumps(poruka))
def fajlulistu(fajl,velicina):
    with ThreadPoolExecutor(max_workers=10) as executor:
        fajl = open(".\\"+fajl,"rb")
        lista = []
        blok = fajl.read(velicina)
        while(blok):
            # print("blok")
            lista.append(blok)
            blok =  fajl.read(velicina)
        fajl.close()
        print("Fajl je u listi.")
        return lista
def fajlusoket(lista):
    with ThreadPoolExecutor(max_workers=5) as executor:
        conn.send(lista[0])
        for i in range(1, len(lista)):
            conn.send(lista[i])
        time.sleep(0.5)
        conn.send(str.encode("c"))
    print("fajl je poslat")
while(True):
    data = conn.recv(80000)
    data = pickle.loads(data)
    if("Zahtev" in data):
        if(data["Zahtev"] == "Log"):
            print(data)
            slanje({"Odgovor":"Meni","1":"Primam fajl","3":"Exit"})
        elif (data["Zahtev"] == "Primam fajl"):
            print(data)
            recnik = {"Odgovor": "Lista sa fajlovima"}
            lista = os.listdir(".")
            for i in range(0,len(lista)):
                if(os.path.isfile(".\\"+lista[i])):
                    recnik.setdefault(str(i), lista[i])
            time.sleep(0.3)
            slanje(recnik)
            # lista = os.listdir(".")
            # for i in range(1, len(lista)):
            #     recnik.setdefault(str(i), lista[i])
            # slanje(recnik)
            # break
        elif (data["Zahtev"] == "Exit"):
            print(data)
            slanje({"Odgovor":"Exit"})
            break
    elif("ZahtevF" in data):
        if(data["ZahtevF"] in os.listdir(".")):
            velicina = int(os.path.getsize(".\\"+data["ZahtevF"])/150)
            slanje({"Odgovor": "Primam fajl","Ime fajla":data["ZahtevF"],"V":velicina})
            time.sleep(2)
            lista = fajlulistu(data["ZahtevF"],velicina)
            fajlusoket(lista)


            # break
# data = conn.recv(5000000)
# lista = []
# while(len(data)!=1):
#     lista.append(data)
#     data = conn.recv(5000000)
# print("lista je gotova(server)")
#
# file = open("fajl.mp4", "wb")
# for i in lista:
#     file.write(i)
#
# file.close()

# konkretna implementacija
# while(True):
#     data = conn.recv(1024)
#     print(pickle.loads(data))


