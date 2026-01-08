class multi_map:
    def __init__(self):
        '''Create an empty Multimap'''
        self.inner = dict()

    def get(self, key):
        '''Return list of values associated with key'''
        return self.inner.get(key, [])

    def put(self, key, value):
        '''Adds value to the list of values associated with key'''
        value_list = self.get(key)
        if value not in value_list:
            value_list.append(value)
            self.inner[key] = value_list

    def put_all(self, key, values):
        for v in values:
            self.put(key, v)

    def remove(self, key, value):
        value_list = self.get(key)
        if value in value_list:
            value_list.remove(value)
            self.inner[key] = value_list
            return True
        return False

m = multi_map()
m.put('Belgium', 'Brussels')
m.put('Belgium', 'Ghent')
m.put('Belgium', 'Antwerp')
m.put('Belgium', 'Bruges')
m.put('Belgium', 'Leuven')
m.put('France', 'Paris')
m.put('France', 'Tours')
m.put_all('England',('London', 'Manchester', 'Moscow','Glasgow'))
m.remove('England', 'Moscow')
print(m.get('Belgium'))
print(m.get('England'))
