def hell_func(greeting, name='You'):
    return '{} {}'.format(greeting, name)

# print(hell_func('Hi', name='John'))


courses = ['Math', 'Art']
info = {'name': 'John', 'age': 22}


def student_info(*args, **kwargs):
    print(args)
    print(kwargs)


# student_info('Math', 'Art', name='John', age=22)
student_info(*courses, **info)
