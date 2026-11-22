"""Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import logging
import re
from typing import Optional

# ---------------------------------------------------------------------
# Registro de eventos y errores
# ---------------------------------------------------------------------

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",)

logger = logging.getLogger("SoftwareFJ")


# ---------------------------------------------------------------------
# Excepciones personalizadas
# ---------------------------------------------------------------------

class SistemaError(Exception):
    """Excepción base del sistema."""


class ValidacionError(SistemaError):
    """Datos o parámetros que no cumplen las reglas."""


class NoEncontradoError(SistemaError):
    """El objeto solicitado no existe."""


class OperacionNoPermitidaError(SistemaError):
    """La operación no está permitida para el estado actual."""


class ServicioNoDisponibleError(SistemaError):
    """El servicio no está disponible."""


class ReservaError(SistemaError):
    """Error relacionado con una reserva."""


# ---------------------------------------------------------------------
# Entidad abstracta
# ---------------------------------------------------------------------

class Entidad(ABC):
    def __init__(self, identificador: str):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValidacionError("El identificador es obligatorio.")
        self._id = identificador.strip()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def descripcion(self) -> str:
        pass

# ---------------------------------------------------------------------
# Cliente
# ---------------------------------------------------------------------

class Cliente(Entidad):
    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValidacionError("El nombre debe contener al menos 2 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not isinstance(valor, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor.strip()):
            raise ValidacionError("El correo electrónico no tiene un formato válido.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not isinstance(valor, str) or not re.fullmatch(r"[0-9+\-\s]{7,18}", valor.strip()):
            raise ValidacionError("El teléfono debe contener entre 7 y 18 caracteres numéricos válidos.")
        self._telefono = valor.strip()

    def descripcion(self) -> str:
        return f"Cliente {self.id}: {self.nombre} | {self.correo} | {self.telefono}"


# ---------------------------------------------------------------------
# Servicios: abstracción, herencia y polimorfismo
# ---------------------------------------------------------------------

class Servicio(Entidad, ABC):
    IMPUESTO = 0.19  # IVA de ejemplo configurable para el ejercicio

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre del servicio es obligatorio.")
        if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ValidacionError("La tarifa base debe ser un número mayor que cero.")
        if not isinstance(disponible, bool):
            raise ValidacionError("La disponibilidad debe ser verdadera o falsa.")
        self.nombre = nombre.strip()
        self.tarifa_base = float(tarifa_base)
        self.disponible = disponible

    @abstractmethod
    def validar_parametros(self, duracion: float, **kwargs):
        pass

    @abstractmethod
    def calcular_costo(self, duracion: float, descuento: float = 0.0,
                       incluir_impuesto: bool = True, **kwargs) -> float:
        pass

    @abstractmethod
    def descripcion(self) -> str:
        pass

    def _costo_final(self, subtotal: float, descuento: float, incluir_impuesto: bool) -> float:
        if not 0 <= descuento <= 100:
            raise ValidacionError("El descuento debe estar entre 0 y 100.")
        if not isinstance(incluir_impuesto, bool):
            raise ValidacionError("incluir_impuesto debe ser booleano.")
        total = subtotal * (1 - descuento / 100)
        if incluir_impuesto:
            total *= (1 + self.IMPUESTO)
        return round(total, 2)


class ReservaSala(Servicio):
    def validar_parametros(self, duracion: float, **kwargs):
        if duracion <= 0 or duracion > 12:
            raise ValidacionError("La reserva de sala debe durar entre 0 y 12 horas.")
        capacidad = kwargs.get("personas", 1)
        if not isinstance(capacidad, int) or capacidad < 1 or capacidad > 100:
            raise ValidacionError("La cantidad de personas debe estar entre 1 y 100.")

    def calcular_costo(self, duracion: float, descuento: float = 0.0,
                       incluir_impuesto: bool = True, **kwargs) -> float:
        self.validar_parametros(duracion, **kwargs)
        personas = kwargs.get("personas", 1)
        recargo = 1.0 if personas <= 10 else 1.25
        return self._costo_final(self.tarifa_base * duracion * recargo, descuento, incluir_impuesto)

    def descripcion(self) -> str:
        return f"Sala: {self.nombre} | tarifa/hora: ${self.tarifa_base:.2f}"


class AlquilerEquipo(Servicio):
    def validar_parametros(self, duracion: float, **kwargs):
        if duracion <= 0 or duracion > 30:
            raise ValidacionError("El alquiler debe durar entre 1 y 30 días.")
        cantidad = kwargs.get("cantidad", 1)
        if not isinstance(cantidad, int) or cantidad < 1 or cantidad > 20:
            raise ValidacionError("La cantidad de equipos debe estar entre 1 y 20.")

    def calcular_costo(self, duracion: float, descuento: float = 0.0,
                       incluir_impuesto: bool = True, **kwargs) -> float:
        self.validar_parametros(duracion, **kwargs)
        cantidad = kwargs.get("cantidad", 1)
        return self._costo_final(self.tarifa_base * duracion * cantidad, descuento, incluir_impuesto)

    def descripcion(self) -> str:
        return f"Equipo: {self.nombre} | tarifa/día: ${self.tarifa_base:.2f}"


class AsesoriaEspecializada(Servicio):
    def validar_parametros(self, duracion: float, **kwargs):
        if duracion <= 0 or duracion > 8:
            raise ValidacionError("La asesoría debe durar entre 1 y 8 horas.")
        especialidad = kwargs.get("especialidad", "General")
        if not isinstance(especialidad, str) or len(especialidad.strip()) < 3:
            raise ValidacionError("Debe indicar una especialidad válida.")

    def calcular_costo(self, duracion: float, descuento: float = 0.0,
                       incluir_impuesto: bool = True, **kwargs) -> float:
        self.validar_parametros(duracion, **kwargs)
        complejidad = kwargs.get("complejidad", "media")
        factores = {"basica": 1.0, "media": 1.25, "alta": 1.6}
        if complejidad not in factores:
            raise ValidacionError("La complejidad debe ser basica, media o alta.")
        return self._costo_final(self.tarifa_base * duracion * factores[complejidad],
                                 descuento, incluir_impuesto)

    def descripcion(self) -> str:
        return f"Asesoría: {self.nombre} | tarifa/hora: ${self.tarifa_base:.2f}"


# ---------------------------------------------------------------------
# Reserva
# ---------------------------------------------------------------------

class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva(Entidad):
    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio,
                 duracion: float, **parametros):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente):
            raise ValidacionError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ValidacionError("La reserva requiere un servicio válido.")
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool):
            raise ValidacionError("La duración debe ser numérica.")
        servicio.validar_parametros(float(duracion), **parametros)
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio {servicio.nombre} no está disponible.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = float(duracion)
        self.parametros = parametros
        self.estado = EstadoReserva.PENDIENTE
        self.total: Optional[float] = None

    def confirmar(self):
        if self.estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")
        self.estado = EstadoReserva.CONFIRMADA
        logger.info("Reserva %s confirmada.", self.id)

    def cancelar(self):
        if self.estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
            raise OperacionNoPermitidaError("No se puede cancelar una reserva cancelada o procesada.")
        self.estado = EstadoReserva.CANCELADA
        logger.info("Reserva %s cancelada.", self.id)

    def procesar(self, descuento: float = 0.0, incluir_impuesto: bool = True):
        if self.estado is not EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError("La reserva debe estar confirmada antes de procesarse.")
        try:
            self.total = self.servicio.calcular_costo(
                self.duracion, descuento, incluir_impuesto, **self.parametros
            )
            if self.total < 0:
                raise ValueError("El cálculo produjo un total negativo.")
            self.estado = EstadoReserva.PROCESADA
            logger.info("Reserva %s procesada. Total: %.2f", self.id, self.total)
            return self.total
        except Exception as exc:
            logger.exception("Error procesando reserva %s.", self.id)
            raise ReservaError(f"No fue posible procesar la reserva {self.id}.") from exc

    def descripcion(self) -> str:
        total = f"${self.total:.2f}" if self.total is not None else "Pendiente de cálculo"
        return (f"Reserva {self.id} | {self.cliente.nombre} | {self.servicio.nombre} | "
                f"{self.estado.value} | Total: {total}")


