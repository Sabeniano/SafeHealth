import _thread
import utime
import tm1637
from time import sleep, time, ticks_diff, ticks_ms
from credentials import credentials
from networking import connect_to_wifi
from micropy.micropyGPS import MicropyGPS
from machine import ADC, Pin, I2C, SoftI2C, UART
from mqtt_communication import connect_mqtt_client, check_mqtt_connection

tilt_pin = Pin(4, Pin.IN)  # Define the pin to which the tilt sensor is connected
tm = tm1637.TM1637(clk=Pin(18), dio=Pin(19))
adc = ADC(Pin(34))

adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB)

PRODUCT_ID = credentials["productid"]
wlan = connect_to_wifi()

send_data_flag = False
gps_from_thread = None
tilt_from_thread = None
promille_from_thread = None
mqtt_client = None  # Define mqtt_client as a global variable

def gps_thread(sleep_timer):
    uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, timeout=5000, rxbuf=1024)
    global gps_from_thread
    gps = MicropyGPS()
    while True:
        buf = uart.readline()
        if buf:
            for char in buf:
                gps.update(chr(char))

        formattedLat = gps.latitude_string()    
        formattedLat = formattedLat[:-3]
        formattedLon = gps.longitude_string()
        formattedLon = formattedLon[:-3]

        gps_in_use = gps.satellites_in_use

        if formattedLat != "0.0" and formattedLon != "0.0":
            gps_from_thread = formattedLat+","+formattedLon
            print("From gps_thread: {}".format(gps_from_thread))
        sleep(sleep_timer)

def send_data_thread(sleep_timer, use_fake_gps_data=False): #def send_data_thread(sleep_timer)
    global gps_from_thread, tilt_from_thread, mqtt_client, promille_from_thread
    while True:
        gps_data = gps_from_thread
        tilt_data = tilt_from_thread
        promille_data = promille_from_thread
        print("GPS Data:", gps_data, "Tilt Data:", tilt_data)
        
        if (gps_data is not None and len(gps_data) > 7) or use_fake_gps_data:#if gps_data is not None and len(gps_data) > 7:
            if use_fake_gps_data and (gps_data is None or len(gps_data) <= 7):			#delete
                gps_data = "55.69196,12.55397"  													#delete
                tilt_data = tilt_data if tilt_data is not None else "0.0"			#delete
            
            payload = f"{PRODUCT_ID} {gps_data} {tilt_data} {promille_data}"
            mqtt_client.publish('gps_data_topic', payload)
            print("Sent data!: " +payload)
        else:
            print("No signal from GPS")
        sleep(sleep_timer)  # Sleep for 60 seconds
                
def start_tilt_detection():

    alert_triggered = False  # Flag to track if the alert has been triggered
    alarm_start_time = 0  # Variable to store the start time of the alarm

    def tilt_detected(pin):
        nonlocal alert_triggered, alarm_start_time
        global tilt_from_thread
        if not alert_triggered:  # Check if the alert has already been triggered
            tilt_from_thread = "1"  # Update tilt state
            print(tilt_from_thread)  # Output a message when tilt is detected
            alert_triggered = True  # Set the flag to indicate the alert has been triggered
            alarm_start_time = time()  # Record the start time of the alarm
        elif tilt_pin.value():  # Check if object is upright
            tilt_from_thread = "0"  # Update tilt state
            print(tilt_from_thread)  # Output a message when object is upright
            alert_triggered = False  # Reset the flag when object is upright

    tilt_pin.irq(trigger=Pin.IRQ_RISING, handler=tilt_detected)  # Interrupt when tilt is detected

    while True:
        sleep(1)
        

def alkohol_thread():
    # Kalibreringsværdier
    min_sensor_value = 0  # Minimum sensorværdi (ingen alkohol)
    max_sensor_value = 600  # Maksimal sensorværdi (højt alkoholniveau)
    min_promille = 0  # Promille ved minimum sensorværdi (ingen alkohol)
    max_promille = 4  # Promille ved maksimal sensorværdi (højt alkoholniveau)
    global promille_from_thread
    t=0
    
    timeLastToggle = 0


    while True:
        sensor_value = adc.read()
    
        # Anvend lineær interpolering for at konvertere sensorværdi til promille
        promille = min_promille + (sensor_value - min_sensor_value) * (max_promille - min_promille) / (max_sensor_value - min_sensor_value)
        promille_string = str(promille).replace('.', '')
        truncated_promille = promille_string[:4]
    
        # Udskriv promilleniveauet
        print("Promille:", promille)
    
        tm.write([0, 0, 0, 0])
        tm.show(truncated_promille)
        promille_from_thread = promille
        sleep(5)

def main_loop():
    global mqtt_client
    if wlan is None:
        print("Failed to connect to WiFi. Restarting...")
        machine.reset()
    else:
        mqtt_client = connect_mqtt_client()
        if mqtt_client:
            _thread.start_new_thread(gps_thread, (1,))
            _thread.start_new_thread(send_data_thread, (20, True)) # Send data every 60 seconds
            _thread.start_new_thread(start_tilt_detection, ())
            _thread.start_new_thread(alkohol_thread, ())
        else:
            print("Failed to connect to MQTT server.")
    while True:
        sleep(1)

main_loop()
