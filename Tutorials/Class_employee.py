class Employee:
    raise_amount = 1.05

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    @property
    def email(self):
        # return '{} {}'.format(self.first, self.last)
        return f'{self.first}.{self.last}@email.com'

    @property
    def fullname(self):
        # return '{} {}'.format(self.first, self.last)
        return f'{self.first} {self.last}'

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)
