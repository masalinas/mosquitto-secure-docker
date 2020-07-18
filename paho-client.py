import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client("test", transport='websockets')
client.username_pw_set(username="underground", password="underground")
client.tls_set('./certs/ca.crt')
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 9002, 60)

client.publish("test", "Hello SSL Mosquitto")

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
#client.loop_forever()
