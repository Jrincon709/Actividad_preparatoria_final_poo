from abc import ABC, abstractmethod

from cifradorMensajes.modelo.errores import ErrorContenido, ContieneNoAscii, ContieneNumero, SinLetras, DobleEspacio, \
    NoTrim


class ReglaCifrado(ABC):
    def __init__(self,token):
        self.token = token


    def mensaje_valido(self,mensaje):
        pass


    def encriptar(self,mensaje):
        pass


    def desencriptar (self,mensaje):
        pass

    def encontrar_numeros_mensaje(self, mensaje):
        return [i for i, char in enumerate(mensaje) if char.isdigit()]

    def encontrar_no_ascii_mensaje(self,mensaje):
        return [i for i, char in enumerate(mensaje) if not (32 <= ord(char) <= 126)]


class Cifrador:
    def __init__(self, agente):
        self.agente = agente

    def encriptar(self, mensaje):
        return self.agente.encriptar(mensaje)

    def desencriptar(self, mensaje):
        return self.agente.desencriptar(mensaje)

class ReglaCifradoTraslacion(ReglaCifrado):

    def mensaje_valido(self,mensaje):
        numeros = self.encontrar_numeros_mensaje(mensaje)
        mensajeno_ascii = self.encontrar_no_ascii_mensaje(mensaje)

        if numeros or mensajeno_ascii:
            errores = []
            if numeros:
                for num_pos in numeros:
                    errores.append(f"Error en posición {num_pos}: Número encontrado: {mensaje[num_pos]}")
                raise ContieneNumero("\n".join (errores))
            if mensajeno_ascii:
                for ascii_pos in mensajeno_ascii:
                    errores.append (f"Error en posición {ascii_pos}: Carácter no ASCII encontrado: {mensaje[ascii_pos]}")
                raise ContieneNoAscii ("\n".join (errores))

        if all(char in ['@', '_', '#', '$', '%'] for char in mensaje):
            raise SinLetras()

        if "  " in mensaje:
            raise DobleEspacio()

        if set(mensaje) == {' '}:
            raise NoTrim()

        return True

    def encriptar(self, mensaje):
        if self.mensaje_valido(mensaje):
            mensaje = mensaje.lower
            mensaje_cifrado =""
            for char in mensaje:
                if char.isalpha():
                    nuevo_caracter = chr((ord(char)-ord("a")+self.token)%26 +ord("a"))
                    mensaje_cifrado += nuevo_caracter
                else:
                    mensaje_cifrado += char

            return mensaje_cifrado


    def desencriptar(self,mensaje):
        mensaje = mensaje.lower()
        mensaje_descifrado = ""
        for char in mensaje:
            if char.isalpha():
                nuevo_caracter = chr((ord(char)-ord("a")- self.token)%26 + ord("a"))
                mensaje_descifrado += nuevo_caracter
            else:
                mensaje_descifrado += char
        return mensaje_descifrado

    class ReglaCifradoNumerico (ReglaCifrado):

        def mensaje_valido(self,mensaje):
            numeros = self.encontrar_numeros_mensaje(mensaje)

            if numeros:
                errores= []
                if numeros:
                    for num_pos in numeros:
                        errores.append (f"Error en posición {num_pos}: Número encontrado: {mensaje[num_pos]}")
                    raise ContieneNumero ("\n".join (errores))

            if mensaje.startswith(" ") or mensaje.endswith(" "):
                raise ErrorContenido ("El mensaje no puede tener espacios al inicio o al final.")

            if "  " in mensaje:
                raise DobleEspacio()

            return True

        def encriptar(self,mensaje):
            if self.mensaje_valido(mensaje):
                mensaje = mensaje.lower()
                mensaje_encriptado = ""

                for char in mensaje:
                    if char.isalpha():
                        nuevo_caracter = ord(char)* self.token
                        mensaje_encriptado += str(nuevo_caracter) +" "
                return mensaje_encriptado.rstrip()

        def desencriptar(self,mensaje):
            valores = mensaje.split()
            mensaje_original = ""
            for valor in valores:
                valor_numerico = int(valor)
                caracter_original = chr(valor_numerico//self.token)
                mensaje_original += caracter_original
            return mensaje_original

