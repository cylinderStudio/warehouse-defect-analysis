from os import getenv
import busio
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_connection_manager
import adafruit_requests
import time
import array
import math
import board
from digitalio import DigitalInOut, Direction
import audiobusio
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

# Get details from settings.toml
SSID = getenv("WIFI_SSID")
PASSWORD = getenv("WIFI_PASSWORD")
DB_URL = getenv("DB_URL")
DB_API_KEY = getenv("DB_API_KEY")

INSERT_URL = f"{DB_URL}/shipdock_environmental_data"

HEADERS = {
    "Content-Type": "application/json",
    "apikey": DB_API_KEY,
    "Authorization": f"Bearer {DB_API_KEY}"
}

if not SSID or not PASSWORD:
    raise RuntimeError("Wifi settings are unavailable or incorrect.")

# ESP32 connections
esp32_cs = DigitalInOut(board.CS1)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
pool = adafruit_connection_manager.get_radio_socketpool(esp)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
requests = adafruit_requests.Session(pool, ssl_context)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in ready/idle mode")

for ap in esp.scan_networks():
    print(f"SSID: {ap.ssid}, RSSI: {ap.rssi}")

# Accelerometer/Gyro/Temperature
i2c = board.I2C()
sensor = LSM6DSOX(i2c)

def c_to_f(val):
    temp = int((val * 9/5) + 32)
    return temp

# Helper functions to take multiple sound samples very quickly and average them for accurate readings
def mean(values):
    return sum(values) / len(values)

def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf) for sample in values
    )

    return math.sqrt(samples_sum / len(values))

def normalized_rms_as_dbs(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf) for sample in values
    )
    normalized_values = math.sqrt(samples_sum / len(values))
    decibels = (math.log(normalized_values, 10) * 20)
    return decibels

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 160)

while not esp.is_connected:
    try:
        esp.connect_AP(SSID, PASSWORD)
        print('Connected to access point.')
    except RuntimeError as e:
        print('Could not connect to access point. Retrying...', e)
        continue

while True: 
    led.value = True

    mic.record(samples, len(samples))
    magnitude = normalized_rms_as_dbs(samples)
    noise_level = magnitude
    time.sleep(1)

    temperature = c_to_f(sensor.temperature)
    time.sleep(1)

    payload = {
        "noise_level": noise_level,
        "temperature": temperature
    }

    response = requests.post(INSERT_URL, json=payload, headers=HEADERS)

    # 200 successful GET, 201 successful POST
    if response.status_code == 201:
        # print("Data inserted successfully.")
        pass
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    led.value = False
    time.sleep(60)
