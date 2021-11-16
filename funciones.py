from io import open
import os
from pysnmp.hlapi import *
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import telnetlib
from ftplib import FTP

def agregarElemento (lista,comunidad,direccion,version,puerto):
    if(lista[0]==0):
        lista.pop()
    lista.extend([direccion,comunidad,version,puerto])

def guardarAgentes(lista):
    try:
        archivo = open("agentes.txt", "w")
        i = 0
        while i < len(lista):
            a = lista[i]
            archivo.write(a + "\n")
            i += 1
        archivo.close()
        print("\nAgentes guardados\n")
    except:
        print("No fue posible guardar los agentes")

def leerAgentes(lista):
    try:
        archivo = open("agentes.txt", "r")
        lista = archivo.read().split("\n")
        lista.pop()
        archivo.close()
        print(lista, "Numero de agentes monitorizados:",len(lista)/4)
        return lista
    except:
        print("No se pudo leer los agentes")

def imprimirLista (lista):
    print(lista[:])

def eliminarAgente (lista,direccion):
    try:
        dex=lista.index(direccion)
        dex2=dex+3
        i=int(dex)
        i=(i/4)+1
        try:
            archivo="agente"+str(int(i))
            os.remove("Reporte de agentes.pdf")
        except:
            print("No hay archivos")
        while (dex<=dex2):
            lista.pop(dex2)
            dex2-=1
    except:
       print("No hay agentes")

def consultaSNMP(comunidad,host,oid,puerto):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, puerto)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        resultado=errorIndication
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split()[2]
    return resultado

def consultaSNMP2(comunidad,host,oid,puerto):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, puerto)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        resultado=errorIndication
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split()[14]
    return resultado

def estadoAgente (lista):
    tamaño=int(len(lista))/4
    print("Número de agentes monitorizados",tamaño)
    i=0
    j=0
    while (i<tamaño):
        resultado=consultaSNMP(lista[j+1],lista[j],'1.3.6.1.2.1.1.1.0',int(lista[j+3]))
        if(str(resultado)=="No SNMP response received before timeout"):
            print("Estado del agente",i+1,": down")
        else:
            print("Estado del agente",i+1,": up")
            resultado=consultaSNMP(lista[j+1],lista[j],'1.3.6.1.2.1.2.1.0',lista[j+3])
            print("El número de interfaces de red del agente",i+1,"son:", resultado)
        i+=1
        j+=4

def generarPDF (lista):
    j=0
    c=canvas.Canvas("Reporte de agentes.pdf", pagesize=A4)
    h=A4
    i=0
    path="/home/mint2/Documentos/Practica_2/IMG/"
    while i < len(lista)/4:
        print(lista[j + 2])
        k=400*i
        if lista[j+2] == "windows":
            c.drawImage("Windows.jpeg", 20, h[1] -60 - k, width=50, height=50)
            text = c.beginText(50, h[1] - 80-k)
            text.textLines(
                "\n\n\nNombre: " + str(consultaSNMP(lista[j + 1], lista[j], '1.3.6.1.2.1.1.5.0', lista[j + 3])) + "   "
                + "Version: " + str(consultaSNMP(lista[j + 1], lista[j], '1.3.6.1.2.1.1.2.0', lista[j + 3])) + "    "
                + "   SO: " + str(consultaSNMP2(lista[j + 1], lista[j], '1.3.6.1.2.1.1.1.0', lista[j + 3])) + "\n"
                + "Ubicacion: " + str(consultaSNMP(lista[j + 1], lista[j], '1.3.6.1.2.1.1.6.0', lista[j + 3])) + "\n"
                + "Puerto: " + str(lista[j + 3]) + " Tiempo de Actividad: " + str(
                    consultaSNMP(lista[j + 1], lista[j], '1.3.6.1.2.1.1.3.0', lista[j + 3])) + "\n"
                + "Comunidad: " + str(lista[j + 1]) + " IP: " + str(lista[j]))
            c.drawText(text)
            i+=1
            j+=4
        else:
            c.drawImage("mint.png", 20, h[1] - 60 - k, width=50, height=50)
            text = c.beginText(50, h[1] - 80 - k)
            text.textLines(
                "\n\n\nNombre: " + str(consultaSNMP(lista[j + 1], lista[j], '1.3.6.1.2.1.1.5.0', lista[j + 3])) + "   "
                + "Version: " + str(consultaSNMP(lista[j + 1], lista[j], '1.3.6.1.2.1.1.2.0', lista[j + 3])) + "    "
                + "   SO: " + str(consultaSNMP(lista[j + 1], lista[j], '1.3.6.1.2.1.1.1.0', lista[j + 3])) + "\n"
                + "Ubicacion: " + str(consultaSNMP(lista[j + 1], lista[j], '1.3.6.1.2.1.1.6.0', lista[j + 3])) + "\n"
                + "Puerto: " + str(lista[j + 3]) + " Tiempo de Actividad: " + str(
                    consultaSNMP(lista[j + 1], lista[j], '1.3.6.1.2.1.1.3.0', lista[j + 3])) + "\n"
                + "Comunidad: " + str(lista[j + 1]) + " IP: " + str(lista[j]))
            c.drawText(text)
            i+=1
            j+=4
    c.showPage()
    c.save()

def reporte(lista):
    generarPDF(lista)

def clienteTelnet():
    Host = input("Ingrese el host:\t")
    user = input("Ingresa tu usuario:\t")
    password = input("Ingresa tu contrasenia:\t")

    tn = telnetlib.Telnet(Host)
    tn.read_until(b"User:")
    tn.write(user.encode('ascii')+b"\n")
    tn.read_until(b"Password:")
    tn.write(password.encode('ascii')+b"\n")
    tn.write(b"enable\n")
    tn.write(b"conf\n")
    try:
       aux = "n"
       while aux != "s":
           aux = input("Configurar\n1-Hostname\n2-Ip address interface\n3-Conexion entre redes (rip)\n4-Guardar configuracion\nSalir (s)\n")
           if aux == "1":
               aux = input("Ingresa el nombre del host (Sin espacios)\t")
               tn.write(b"h " + aux.encode('ascii') + b"\n")
           if aux == "2":
               while aux != "n":
                   aux = input("Ingresa la interfaz ethernet (valor numerico)\t")
                   tn.write(b"int eth eth" + aux.encode('ascii') + b"\n")
                   aux = input("Ingresa la ip (valor numerico)\t")
                   tn.write(b"ip add " + aux.encode('ascii') + b"/24\n")
                   tn.write(b"n sh\n")
                   tn.write(b"exit\n")
                   aux = input("Configurar otra interfaz (s/n)\t")
           if aux == "3":
               while aux != "n":
                   tn.write(b"route rip \n")
                   aux = input("Ingresa la red\t")
                   tn.write(b"net " + aux.encode('ascii') + b"/24 \n")
                   aux = input("Ingresa la red\t")
                   tn.write(b"net " + aux.encode('ascii') + b"/24 \n")
                   tn.write(b"red con\n")
                   tn.write(b"exit\n")
                   aux = input("Configurar otra par de redes (s/n)\t")
           if aux == "4":
               tn.write(b"copy ru st\n")
       tn.write(b"exit\n")
       tn.close()
    except:
       print("No se logro la operacion\n")
       tn.close()

def clienteFTP():
    host = input("Ingresa el host:\t")
    user = input("Ingresa el usuario:\t")
    password = input("Ingresa la contrasenia:\t")
    st=0

    try:
        c = FTP(host)
        c.login(user, password)
        print("Conexion establecida")
    except:
        print("Conexión fallida")

    c.retrlines("LIST")

    while st != 3:
        st = int(input("Selecciona la operación a realizar\n1)Enviar el archivo (put)\n2)Obtener el archivo (get)\n3)Salir\n "))
        if st==2 :
            try:
                fich = open("/home/mint2/Documentos/Practica_4/RRD/startup-configR" + host, "wb")
                c.retrbinary("RETR startup-config", fich.write)
                fich.close()
                print("Elemento recuperado")
            except:
                print("Operacion fallida")
        if st == 1:
            try:
                fich = open("/home/mint2/Documentos/Practica_4/RRD/startup-configR" + host, "rb")
                c.storbinary("STOR startup-config", fich)
                fich.close()
                print("Elemento recuperado")
            except:
                print("Operacion fallida")
    c.quit()
