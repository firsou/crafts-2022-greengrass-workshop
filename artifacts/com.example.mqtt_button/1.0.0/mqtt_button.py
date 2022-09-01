import time
import traceback
import json
import RPi.GPIO as GPIO
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    PublishToIoTCoreRequest,
    SubscribeToIoTCoreRequest
)

#Setup the button GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

publishtopic = "raspberrypi/button"
message =  {
  "button": "BCM PIN 18 Triped",
  "timemillis": 000000000000
}

TIMEOUT = 10
qos = QOS.AT_LEAST_ONCE
subqos = QOS.AT_MOST_ONCE


ipc_client = awsiot.greengrasscoreipc.connect()


#button 4 callback
def button4pressed(channel):
    print('button pressed')

    message["timemillis"] = round(time.time() * 1000)

    msgstring = json.dumps(message)

    pubrequest = PublishToIoTCoreRequest()
    pubrequest.topic_name = publishtopic
    pubrequest.payload = bytes(msgstring, "utf-8")
    pubrequest.qos = qos
    operation = ipc_client.new_publish_to_iot_core()
    operation.activate(pubrequest)
    future = operation.get_response()
    future.result(TIMEOUT)

#Subscribe to the button state change event
GPIO.add_event_detect(18, GPIO.RISING, callback=button4pressed, bouncetime=200)

# Keep the main thread alive, or the process will exit.
while True:
    #time.sleep(10)
    pass



print("button event detect finished")
