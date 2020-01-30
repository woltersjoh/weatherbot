from SI1145 import SI1145
import BME280
si1145 = SI1145()

print(BME280.readTemperature())
print(BME280.readPressure())
print(BME280.readHumidity())

print(si1145.readUV())
print(si1145.readVisible())
print(si1145.readIR())
