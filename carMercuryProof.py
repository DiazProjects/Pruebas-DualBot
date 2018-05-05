# Pruebas-DualBot
#--Titulo: Car with Raspberry Pi 3 y PWM
#--Description: Estas lineas de codigo nos permiten controlar el carrito cierto tiempo con un delay

#--Librerias--#
import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, request
app = Flask(__name__)

#--Otras definciones--#
GPIO.setmode(GPIO.BCM)

pins = {                                                                        #Estos son los pines a utilizar
    17 : {'name' : '30 cm', 'state' : GPIO.LOW},                                 #como referncias para saber si
    5 : {'name' : '50 cm', 'state' : GPIO.LOW},
    22 : {'name' : 'Back', 'state' : GPIO.LOW},                                 #avanzo, retrocedo, giro a la
    27 : {'name' : 'Right >>', 'state' : GPIO.LOW},                                 #derecha o giro a la izquierda
    4 : {'name' : '<< Left', 'state' : GPIO.LOW},
    12 : {'name' : 'LED', 'state' : GPIO.LOW}
   }

for pin in pins:                                                                #Aqui inicializo todos los pines a utilizar--#
                                                                                #--Pines de Referencia--#
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.LOW)
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, GPIO.LOW)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.LOW)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.LOW)
                                                                                #--Pines de PWM y Motores--#
    GPIO.setup(12, GPIO.OUT)
    GPIO.output(12, GPIO.LOW)
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, GPIO.LOW)
    GPIO.setup(23, GPIO.OUT)
    GPIO.output(23, GPIO.LOW)
    GPIO.setup(24, GPIO.OUT)
    GPIO.output(24, GPIO.LOW)
    GPIO.setup(25, GPIO.OUT)
    GPIO.output(25, GPIO.LOW)
                                                                                #--Aqui definimos el pwm a usar--#
pwm1 = GPIO.PWM(13,100)
pwm2 = GPIO.PWM(23,100)
pwm3 = GPIO.PWM(24,100)
pwm4 = GPIO.PWM(25,100)

#--Deficiones (DEF)--#
@app.route("/")
def main():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    templateData = {
        'pins' : pins
        }
    return render_template('main.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
    changePin = int(changePin)
    deviceName = pins[changePin]['name']
    if action == "on":
        if (deviceName == "30 cm"):                                             #Me muevo hacia adelante 20 centimetros
            GPIO.output(changePin, GPIO.HIGH)
            pwm1.start(0)
            pwm2.start(70)
            pwm3.start(0)
            pwm4.start(75)
            time.sleep(0.5)
            pwm1.start(0)
            pwm2.start(0)
            pwm3.start(0)
            pwm4.start(0)
            pwm1.stop()
            pwm2.stop()
            pwm3.stop()
            pwm4.stop()
            GPIO.output(changePin, GPIO.LOW)
	    message = "You advance " + deviceName
        if (deviceName == "50 cm"):                                         #Me muevo hacia adelante 50 centimetros
            GPIO.output(changePin, GPIO.HIGH)
            pwm1.start(0)
            pwm2.start(90)
            pwm3.start(0)
            pwm4.start(65)
            time.sleep(1.7)
            pwm1.start(0)
            pwm2.start(0)
            pwm3.start(0)
            pwm4.start(0)
            pwm1.stop()
            pwm2.stop()
            pwm3.stop()
            pwm4.stop()
            GPIO.output(changePin, GPIO.LOW)
    	    message = "You advance " + deviceName
        elif (deviceName == "Back"):                                            #Me muevo hacia atras
            GPIO.output(changePin, GPIO.HIGH)
            pwm1.start(70)
            pwm2.start(0)
            pwm3.start(70)
            pwm4.start(0)
            time.sleep(0.5)
            pwm1.start(0)
            pwm2.start(0)
            pwm3.start(0)
            pwm4.start(0)
            pwm1.stop()
            pwm2.stop()
            pwm3.stop()
            pwm4.stop()
            GPIO.output(changePin, GPIO.LOW)
	    message = "You went " + deviceName
        elif (deviceName == "Right >>"):                                        #Giro a la derecha
            GPIO.output(changePin, GPIO.HIGH)
            pwm1.start(0)
            pwm2.start(0)
            pwm3.start(70)
            pwm4.start(0)
            time.sleep(0.4)
            pwm1.start(0)
            pwm2.start(0)
            pwm3.start(0)
            pwm4.start(0)
            pwm1.stop()
            pwm2.stop()
            pwm3.stop()
            pwm4.stop()
            GPIO.output(changePin, GPIO.LOW)
	    message = "You moved to the " + deviceName
        elif (deviceName == "<< Left"):                                            #Giro a la izquierda
            GPIO.output(changePin, GPIO.HIGH)
            pwm1.start(70)
            pwm2.start(0)
            pwm3.start(0)
            pwm4.start(0)
            time.sleep(0.4)
            pwm1.start(0)
            pwm2.start(0)
            pwm3.start(0)
            pwm4.start(0)
            pwm1.stop()
            pwm2.stop()
            pwm3.stop()
            pwm4.stop()
            GPIO.output(changePin, GPIO.LOW)
            message = "You moved to the " + deviceName
        elif (deviceName == "LED"):
            GPIO.output(changePin, GPIO.HIGH)
            GPIO.output(12, GPIO.HIGH)
	    message = "Encendio " + deviceName
    if action == "off":                                                         #No hago nada
        GPIO.output(changePin, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
	GPIO.output(12, GPIO.LOW)
        message = "Unemployed"
    if action == "toggle":
        GPIO.output(changePin,not GPIO.input(changePin))
        message = "Toggled " + deviceName + "."

    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    templateData = {
        'message' : message,
        'pins' : pins
    }

    return render_template('main.html', **templateData)

#--El MAIN--#
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
