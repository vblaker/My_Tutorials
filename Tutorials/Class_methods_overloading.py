class Employee:

    raise_amount = 1.05

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@email.com'

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)
        print('Applied {}% raise'.format(self.raise_amount))

    def __repr__(self):
        return "Employee('{}', '{}', {})".format(self.first, self.last, self.pay)

    def __str__(self):
        return '{} - {}'.format(self.fullname(), self.email)

    def __add__(self, other):
        return self.pay + other.pay

    def __len__(self):
        return len(self.fullname())


class Developer(Employee):
    raise_amount = 1.10

    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang


class Manager(Employee):
    raise_amount = 1.15

    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
            print(f'Added {emp}')

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)
            print(f'Removed {emp}')

    def print_emps(self):
        for emp in self.employees:
            print('-->', emp.fullname())


if __name__ == '__main__':

    # print(help(Developer))
    dev_1 = Developer('Corey', 'Schafer', 50000, 'Python')
    dev_2 = Developer('Test', 'Employee', 60000, 'Java')

    mgr_1 = Manager('Sue', 'Smith', 90000, [dev_1])
    print(mgr_1.email)
    mgr_1.add_emp(dev_2)
    mgr_1.print_emps()
    mgr_1.remove_emp(dev_1)
    mgr_1.print_emps()

    # print(dev_1.pay)
    # dev_1.apply_raise()
    # print(dev_1.pay)

    # print(dev_1.email)
    # print(dev_1.prog_lang)

    # print(help(Developer))
