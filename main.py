from funciones import *

salir=0
comunidad=""
direccion=""
puerto=""
version=""
lista=[0]
while (salir != 4):
    print ("Opciones:\n1)Agregar agente\n2)Eliminar agente\n3)Estado de los agentes\n4)Salir\n5)Guardar agentes en txt\n6)Leer agentes de txt\n7)Generar reporte pdf\n8)FTP\n9)Telnet\n")
    try:
        salir = int(input("\nIngrese la opcion deseada: "))
    except:
        print("XXXXIngrese una opcion valida:XXXX")
    if (salir==1):
        comunidad=input("Ingresa el nombre de la comunidad: ")
        direccion=input("Ingresa la direccion del agente: ")
        version=input("Ingresa el SO del agente: ")
        puerto=input("Ingresa el puerto del agente: ")
        agregarElemento(lista,comunidad,direccion,version,puerto)
        imprimirLista(lista)
    if(salir==2):
        direccion=input("Ingresa la direccion del agente a eliminar: ")
        eliminarAgente(lista,direccion)
        imprimirLista(lista)
    if(salir==3):
        estadoAgente(lista)
    if (salir== 5):
        guardarAgentes(lista)
    if (salir == 6):
        lista=leerAgentes(lista)
    if (salir == 7):
        reporte(lista)
    if (salir==8):
        clienteFTP()
    if (salir==9):
        clienteTelnet()
