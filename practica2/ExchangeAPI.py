import json
import requests

class ExchangeAPI:
    def __init__(self, url='https://api.exchangeratesapi.io', base='EUR'):
        self.url = url
        self.base = base
        self.start_at = None
        self.end_at = None
        self.rates = None

    def _request(self, p, **q):
        if len(q) == 0:
            response = requests.get('{}/{}?base={}'.format(self.url, p, self.base))
        else:
            args = '&'.join(['='.join(x) for x in q.items()])
            response = requests.get('{}/{}?{}&base={}'.format(self.url, p, args, self.base))
        if response.status_code == 200:
            data = json.loads(response.text)
            if 'start_at' in data:
                self.rates = data['rates']
                self.start_at = data['start_at']
                self.end_at = data['end_at']
            else:
                self.rates = {data['date']: data['rates']}
                self.start_at = data['date']
                self.end_at = data['date']
        else:
            raise Exception('Ha ocurrido un error en la conexión: {}'.format(response.status_code))

    def get_rates(self, base=None, start=None, end=None):
        if start is None and end is None:
            self._request('latest')
            
        elif start is not None and end is not None:
            if start == end:
                self._request(start)
            else:
                self._request('history', start_at=start, end_at=end)

        else:
            raise Exception('')

    def convert(self, val, from_curr, to_curr=None, date=None):
        if to_curr is None:
            to_curr = self.base

        if date is None:
            date = self.start_at

        if to_curr != self.base:
            raise Exception()
        else:
            if date in self.rates:
                if from_curr in self.rates[date]:
                    return val / self.rates[date][from_curr]
                else:
                    raise Exception('Divisa desconocida: {}'.format(from_curr))
            else:
                raise Exception('La fecha debe estar entre {} y {}: {}'.format(self.start_at, self.end_at, date))

if __name__ == '__main__':
    import time
    import pandas as pd

    exchange = ExchangeAPI()

    print('Obteniendo las tasas de cambio...')
    exchange.get_rates()
    print('Cargando el fichero "savings"...')
    savings = pd.read_csv('savings.csv')
    print('Cargando el fichero "ahorros.csv"...')
    evolucion = pd.read_csv('ahorros.csv')
    total = 0

    for x, row in savings.iterrows():
        total += exchange.convert(row['cantidad'], row['codigo'])
    print('Tienes un total de {} euros'.format(total))

    fila = pd.DataFrame([[time.strftime('%Y-%m-%d'), total]], columns=['fecha', 'total'])
    evolucion = evolucion.append(fila)
    evolucion.to_csv('ahorros.csv', index=False)