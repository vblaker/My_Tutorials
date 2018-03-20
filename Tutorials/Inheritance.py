class Parent:
    def print_last_name(self):
        print('Blaker')


class Child(Parent):
    def print_first_name(self):
        print('Vadim')

    def print_last_name(self):
        print('Function Override')


me = Child()
me.print_first_name()
me.print_last_name()
