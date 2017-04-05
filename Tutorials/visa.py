import pyvisa

rm = pyvisa.ResourceManager()
equipment_list = rm.list_resources()
print(equipment_list)
inst = rm.open_resource('GPIB0::5::INSTR')
print(inst.query("*IDN?"))
