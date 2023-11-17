from abc import ABC, abstractmethod


class ErrorContenido(ABC, Exception):
    def __init__(self,detalles):
        self.detalles = detalles


class ContieneNumero (ErrorContenido):
    def __init__(self,detalles):
        super().__init__(detalles)
    def __str__(self):
        return f"Error de contenido : {self.detalles}"

class ContieneNoAscii (ErrorContenido):
    def __init__(self,detalles):
        super().__init__(detalles)
    def __str__(self):
        return f"Error de contenido : {self.detalles}"


class ErrorFormato(ABC,Exception):
    def __str__(self):
        pass

class DobleEspacio(ErrorFormato):
    def __str__(self):
        return f"Error de Formato: Doble Espacio Detectado"

class NoTrim(ErrorFormato):
    def __str__(self):
        return f"Error de Formato: El mensaje no puede consistir únicamente de espacios"

class SinLetras(ErrorFormato):
    def __str__(self):
        return f"Error de Formato:Sin letras en el mensaje"


