from pymodbus.client.sync import ModbusSerialClient as ModbusClientRtu
from influxdb import InfluxDBClient
import time
import json

dalayTime = 0.5
UnitNo = 1
ph = 3

volt_add = [0, 0x00A4, 0, 0x00AA]
pf_add = [0, 0x00C2, 0, 0x00C5]
current_add = [0, 0x00B4, 0, 0x00BC]
kW_add = [0, 0x008C, 0, 0x0092]
kWh_add = 0x00CC
temp_add = 0x01A2

rtu = ModbusClientRtu(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'O', baudrate = 9600)
dbClient = InfluxDBClient(host='192.168.1.192', port=8086, database='inhousedb')
previous_time = time.time() 

def task():
    try:
        volt = rtu.read_holding_registers(volt_add[ph], 1, unit= UnitNo)
        volt = volt.registers[0]/10
        print("volt : " + str(volt))
        pf = rtu.read_holding_registers(pf_add[ph], 1, unit= UnitNo)
        pf = pf.registers[0]/1000
        print("pf : " + str(pf))
        current = rtu.read_holding_registers(current_add[ph], 1, unit= UnitNo)
        current = current.registers[0]/100
        print("current : " + str(current))
        kW = rtu.read_holding_registers(kW_add[ph], 1, unit= UnitNo)
        kW = kW.registers[0]/100
        print("kW : " + str(kW))
        kWh = rtu.read_holding_registers(kWh_add, 1, unit= UnitNo)
        kWh = kWh.registers[0]/100
        print("kWh : " + str(kWh))
        temp = rtu.read_holding_registers(temp_add, 1, unit= UnitNo)
        temp = temp.registers[0]/10
        print("temp : " + str(temp))
    except Exception as err:
        print(err)

    try:
        pwm1 = [{"measurement": "pwm1",

        "tags": 
            {
            # "unit": xiaomiTemp.units
            },
        "fields":
            {
                "volt": volt,
                "pf": pf,
                "current": current,
                "kW": kW,
                "kWh": kWh,
                "temp": temp
            }
        }]
        dbClient.write_points(pwm1)
    except Exception as err:
      print(err)

while True:

    if time.time()-previous_time >= 10:
        previous_time = time.time()
        task()