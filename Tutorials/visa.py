import pyvisa

rm = pyvisa.ResourceManager()
equipment_tuple = rm.list_resources()
print(equipment_tuple)
equipment_list = list(equipment_tuple)
print('There are %d items on the list' % len(equipment_list), equipment_list)

#any('GPIB' in equipment_list for equipment in equipment_list)

i = 0
for equipment in equipment_list:
    if 'GPIB' in equipment:
        instrument = rm.open_resource(equipment)
        print(instrument.query("*IDN?"), end="")
        i = i + 1
    else:
        print('Equipment %s is not queried' % equipment)
        del equipment_list[i]

print('\nNew equipment list is:', equipment_list)
equipment_tuple = tuple(equipment_list)