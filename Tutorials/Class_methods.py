class Employee:

    num_of_employees = 0
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

        Employee.num_of_employees += 1

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
            self.pay = int(self.pay * self.raise_amount)
            print('Applied {}% raise'.format(self.raise_amount))

    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amount = amount

    @classmethod
    def from_string(cls, emp_string):
        first, last, pay = emp_string.split('-')
        return cls(first, last, pay)

    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False    #False means it wasn't a Saturday or Sunday
        return True         #True means it WAS a Saturday or Sunday

print('Number of Employees is {}'.format(Employee.num_of_employees))

# Set instance variables
emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Test', 'User', 60000)

emp_1.raise_amount = 1.05
print(emp_1.fullname())
print(emp_1.raise_amount)
print(emp_1.apply_raise())
print(emp_1.pay)


print(emp_2.raise_amount)

Employee.raise_amount = 1.06

# Set class variables
Employee.set_raise_amt(1.05)

print('Number of Employees is {}'.format(Employee.num_of_employees))

# Use strings to create new employee object using class method
emp_str_1 = 'John-Doe-70000'
emp_str_2 = 'Steve-Smith-30000'
emp_str_3 = 'Jane-Doe-90000'

new_emp_1 = Employee.from_string(emp_str_1)

#Working with static methods
import datetime
my_date = datetime.date(2017, 3, 13)
print('This day was weekday: {}'.format(Employee.is_workday(my_date)))





if __name__ == '__main__':
    pass
