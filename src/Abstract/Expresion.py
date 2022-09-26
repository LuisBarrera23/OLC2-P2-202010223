from abc import ABC, abstractmethod

from src.Abstract.RetornoType import RetornoType

class Expresion(ABC):
    @abstractmethod
    def obtener3D(self,entorno) -> RetornoType:
        pass