#Hi! 

#So here is what the problem is: 

#This could should control some neopixel led from a raspberry pi zero. In the first place it should turn the led on. After a defined amount of time the LED should start flashing red. Also it should play some random audio files in determined time intervalls (as reminder sounds). 

#There is a Button attached to the Pi. Whenever this Button is pressed, the code should stop every task it is executing and turn the LED of one by one, followed by green flashing LEDs and the output of one of the two „mission accomplished“ sounds. 
# At the moment when I execute the code the Button only works as I wish when it is pressed before the LEDs start blinking. 
#Hope you can help, I am going crazy

#Mo


import board
import neopixel
from gpiozero import Button
import time
import subprocess
import random
import threading

# Anzahl der NeoPixel-LEDs
NUM_LEDS = 21

# Pin-Konfiguration
pixel_pin = board.D18
button_pin = 13  # Verwende GPIO 13 (Pin 33) für den Knopf

# Konfiguration der NeoPixel
pixels = neopixel.NeoPixel(pixel_pin, NUM_LEDS, brightness=0.2, auto_write=False)

# Farbdefinitionen
RED = (255, 0, 0)
GREEN = (0, 255, 0)
OFF = (0, 0, 0)

# Blinkgeschwindigkeiten
BLINK_DURATION = 0.5

#Knopstatus

button_pressed = False
# Knopfkonfiguration
button = Button(button_pin, pull_up=True)  # pull_up=True, um den internen Pull-Up-Widerstand zu aktivieren

# Timer initialisieren
start_time = time.time()

# Verzeichnis mit den Sounddateien
audio_files = [
    "/home/drs/drs/sound/genosse.wav",
    "/home/drs/drs/sound/metal-slug-mission-complete.wav"
]
#Anderes Verzeichnis für Sound
audio_reminder = [
"/home/drs/drs/sound/reminder/berndbrot2.wav",
"/home/drs/drs/sound/reminder/berndbrot1.wav",
"/home/drs/drs/sound/reminder/brucewillis.wav",
"/home/drs/drs/sound/reminder/clauskleber.wav",
"/home/drs/drs/sound/reminder/dieterbohlen.wav",
"/home/drs/drs/sound/reminder/klassenfeind.wav",
"/home/drs/drs/sound/reminder/kohlzigarette.wav",
"/home/drs/drs/sound/reminder/lauterbachknecht.wav",
"/home/drs/drs/sound/reminder/lauterbachsekt.wav",
"/home/drs/drs/sound/reminder/merkel-gemeinsam.wav",
"/home/drs/drs/sound/reminder/merkel-wohlstand.wav",
"/home/drs/drs/sound/reminder/rotfront.wav"]
buzzer = "/home/drs/drs/sound/buzzer.wav"

# Funktion zum Blinken der LEDs
def blink_leds():
    while True:
        if button.is_pressed:
            break  # Wenn der Knopf gedrückt wurde, beende die Schleife
        # Rote LEDs einschalten
        pixels.fill(RED)
        pixels.show()
        time.sleep(0.5)

        # LEDs ausschalten
        pixels.fill(OFF)
        pixels.show()
        time.sleep(0.5)

# Funktion zum Abspielen der Audiodatei
def play_audio():
    while True:
        if button.is_pressed:
            break  # Wenn der Knopf gedrückt wurde, beende die Schleife
        subprocess.run(["aplay", buzzer])
        # Wähle zufällig eine Sounddatei aus der Liste
        selected_audio_file = random.choice(audio_reminder)
        # Abspielen der ausgewählten Sounddatei mit aplay
        subprocess.run(["aplay", selected_audio_file])
        subprocess.run(["aplay", buzzer])
        # Warte
        time.sleep(60)


try:

    # Alle LEDs einschalten
    pixels.fill(RED)
    pixels.show()

    while True:
        # Überprüfen, ob der Knopf gedrückt wurde
        if button.is_pressed:
            # Knopf wurde gedrückt, Abschaltprozedur starten
            for i in range(NUM_LEDS):
                pixels[NUM_LEDS -1 - i] = OFF
                pixels.show()
                time.sleep(0.1)
            for _ in range(3):
                pixels.fill(GREEN)
                pixels.show()
                time.sleep(0.5)
                pixels.fill(OFF)
                pixels.show()
                time.sleep(0.5)
            
            # Wähle zufällig eine Sounddatei aus der Liste
            selected_audio_file = random.choice(audio_files)
            # Abspielen der ausgewählten Sounddatei mit aplay
            subprocess.run(["aplay", selected_audio_file])
            
            break

        # Berechnen der vergangenen Zeit seit dem Skriptstart
        elapsed_time = time.time() - start_time
        print ("Vor if für Threads")
        # Überprüfen, ob die Zeit für das Blinken gekommen ist
        if elapsed_time >= 10 and not button.is_pressed:
            # Rote LEDs blinken (eigener Thread)
            led_thread = threading.Thread(target=blink_leds)
            led_thread.start()
            # Audio abspielen eigener Thread
            audio_thread = threading.Thread(target=play_audio)
            audio_thread.start()        
            print ("Ende Threads vor Break")

            break# Da die Bedingung erfüllt ist, brechen wir die Schleife ab
            print ("Ende Threads nach Break")
finally:
    # Abschaltprozedur
    pixels.fill(OFF)
    pixels.show()

