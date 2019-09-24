class Partida:
    def __init__(self, nombre, tipo, jugadores):
        self.partida_terminada = False

        if tipo == 1:
            self.jugador1 = jugadores[0]
            self.jugador2 = jugadores[1]
        else:
            self.jugador1 = jugadores[1]
            self.jugador2 = jugadores[0]

        self.jugador1.pensar()
    
    def jugar_turno(self):
        num = self.jugador2.proponer()
        comp = self.jugador1.comprobar(num)

        if comp < 0:
            print('El número es menor')
            self.jugador2.num_max = num
            self.jugador2.fallo()
        elif comp > 0:
            print('El número es mayor')
            self.jugador2.num_min = num
            self.jugador2.fallo()
        else:
            print('Has acertado')
            self.partida_terminada = True
            self.jugador2.reset()

    def intentos(self):
        return self.jugador2.puntos()
        