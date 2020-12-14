import datetime


class Employee:
    num_of_emps = 0
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        # self.email = first + '.' + last + '@company.com'
        self.email = f'{first}.{last}@company.com'
        Employee.num_of_emps += 1

    def fullname(self):
        # return '{} {}'.format(self.first, self.last)
        return f'{self.first} {self.last}'

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amount(cls, amount):
        cls.raise_amount = amount

    @classmethod
    def from_sting(cls, emp_str):
        first, last, pay = emp_str.split("-")
        return cls(first, last, pay)

    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True


my_date = datetime.datetime.today()
# my_date = datetime.datetime(2020, 12, 14)

# Call @static method via class
print(Employee.is_workday(my_date))

emp_1 = Employee('Corey', 'Schafer', 50000)

# Call @static method via class instance
print(emp_1.is_workday(my_date))

emp_1.raise_amount = 1.05
print(emp_1.fullname())
print(emp_1.raise_amount)
emp_1.apply_raise()
print(emp_1.raise_amount)
print(emp_1.pay)

Employee.set_raise_amount(1.05)

emp_2 = Employee('Test', 'User', 60000)
print(emp_2.raise_amount)
