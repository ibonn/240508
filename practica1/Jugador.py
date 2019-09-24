from random import randint

class TipoJugador:
    Maquina = 0
    Persona = 1

class Jugador:
    
    def __init__(self, mn=1, mx=100, nombre='machine', tipo=TipoJugador.Maquina):
        self.nombre = nombre
        self.tipo = tipo
        self._puntos = 0
        self._mn = mn
        self._mx = mx
        self.reset()

    def fallo(self):
        self._puntos += 1

    def puntos(self):
        return self._puntos

    def reset(self):
        self.num_min = self._mn
        self.num_max = self._mx

    def pensar(self):
        if self.tipo == TipoJugador.Maquina:
            self.numero_pensado = randint(self._mn, self._mx)
        else:
            n = int(input('Introduce el número que quieres que el oponente adivine: '))
            while n < self._mn or n > self._mx:
                print('Por favor introduce un número en el rango [{}, {}]'.format(self._mn, self._mx))
                n = int(input('Introduce el número que quieres que el oponente adivine: '))
            self.numero_pensado = n

    def proponer(self):
        if self.tipo == TipoJugador.Maquina:
            n = randint(self.num_min, self.num_max)
            print('{} propone el número {}'.format(self.nombre, n))
            return n
        else:
            print('Intenta adivinar un número entre {} y {}'.format(self.num_min, self.num_max))
            n = int(input('Introduce un número: '))
            while n < self._mn or n > self._mx:
                print('Por favor introduce un número en el rango [{}, {}]'.format(self._mn, self._mx))
                n = int(input('Introduce un número: '))
            return int(n)
            
    def comprobar(self, num):
        num = int(num)
        if num > self.numero_pensado:
            return -1
        elif num < self.numero_pensado:
            return 1
        else:
            return 0