class Employee:

    raise_amount = 1.04
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
            self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amt(cls, amount):
        pass


emp_1 = Employee('Corey', 'Schafer', 50000)
emp_1.raise_amount = 1.05
print(emp_1.fullname())
print(emp_1.raise_amount)

emp_2 = Employee('Test', 'User', 60000)
print(emp_2.raise_amount)
