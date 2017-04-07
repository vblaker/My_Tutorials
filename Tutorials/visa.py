import pyvisa

rm = pyvisa.ResourceManager()
equipment_tuple = rm.list_resources()
print(equipment_tuple)
equipment_list = list(equipment_tuple)
print('There are %d items on the list' % len(equipment_list), equipment_list)

for equipment in equipment_list:
    if 'GPIB' in equipment:
        instrument = rm.open_resource(equipment)
        print(instrument.query("*IDN?"), end="")
    else:
        print('Equipment %s is not queried' % equipment)