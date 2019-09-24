from Partida import Partida
from Jugador import Jugador, TipoJugador

class NoGanadorException(Exception):
    pass

class Juego:
    def __init__(self, mn=1, mx=100):
        self.mn = mn
        self.mx = mx
        self._jugar = True
        self._jugadores = None
        self._ronda = 0
        
    def jugar(self, nombre):
        self._jugadores = (
            Jugador(nombre=nombre, tipo=TipoJugador.Persona, mn=self.mn, mx=self.mx),
            Jugador(nombre='PC',   tipo=TipoJugador.Maquina, mn=self.mn, mx=self.mx)
        )
        while self._jugar:
            self._jugar_ronda()

    def _jugar_ronda(self):
        tipo_partida = self._ronda % 2
        partida = Partida(nombre, tipo_partida, self._jugadores)
        self._ronda += 1
        print('Comienza la partida')
        while not partida.partida_terminada:
            partida.jugar_turno()
        print('La partida ha finalizado. Número de intentos: {}'.format(partida.intentos()))
        respuesta = input('¿Quieres jugar otra ronda? s/n: ')
        self._jugar = respuesta.lower() == 's'

    def ganador(self):
        if self._jugar:
            raise NoGanadorException('La partida no ha finalizado, todavía no hay ganador')
        else:
            if self._jugadores[0].puntos() > self._jugadores[1].puntos():
                return self._jugadores[1]
            elif self._jugadores[0].puntos() < self._jugadores[1].puntos():
                return self._jugadores[0]
            else:
                return None


if __name__ == '__main__':
    juego = Juego()

    print('En este juego se debe adivinar el número pensado por el oponente en el menor número de intentos posible')
    print('El número debe estar entre {} y {}, ambos incluidos'.format(juego.mn, juego.mx))
    nombre = input('Introduce tu nombre: ')
    juego.jugar(nombre)
    
    ganador = juego.ganador()
    if ganador is None:
        print('Ha habido un empate')
    else:
        print('{} ha ganado la partida'.format(ganador.nombre))