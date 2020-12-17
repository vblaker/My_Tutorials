class Employee:
    num_of_emps = 0
    raise_amount = 1.04

    def __init__(self, first, last):
        self.first = first
        self.last = last
        # self.email = first + '.' + last + '@company.com'
        # self.email = f'{first}.{last}@company.com'
        Employee.num_of_emps += 1

    # @property method allows us to define a method by access it if it was an attribute
    @property
    def email(self):
        # return '{} {}'.format(self.first, self.last)
        return f'{self.first}.{self.last}@email.com'

    @property
    def fullname(self):
        # return '{} {}'.format(self.first, self.last)
        return f'{self.first} {self.last}'

    @fullname.setter
    def fullname(self, name):
        first, last = name.split(' ')
        self.first = first
        self.last = last

    @fullname.deleter
    def fullname(self):
        print('Delete Name!')
        self.first = None
        self.last = None


emp_1 = Employee('John', 'Smith')
emp_1.first = 'Jim'

print(emp_1.first)
print(emp_1.email)
print(emp_1.fullname)

del emp_1.fullname
