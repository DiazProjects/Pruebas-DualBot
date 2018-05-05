# Pruebas-DualBot
import serial, time

# Arduino
Arduino=serial.Serial("/dev/ttyACM0",baudrate=9600,timeout=5)
Arduino.flushInput()

def separar(data):
    if "Distancia" in data:
        label = data.split(":")
        dist = float(label[1])
        print "Distancia US: " + str(dist)

#-------------------------------------------------------------------- MAIN
if __name__ == "__main__":
    print('Inicializando Sensor ... ')
    while(True):
        try:
                data_Arduino=Arduino.readline()
                separar(data_Arduino)
        except KeyboardInterrupt:
                print "Algo va mal :( "
                break
