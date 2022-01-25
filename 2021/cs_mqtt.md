# Case study: containerized MQTT

[![hackmd-github-sync-badge](https://hackmd.io/sLzw_8Q1QFqnoY13kiyAag/badge)](https://hackmd.io/sLzw_8Q1QFqnoY13kiyAag)



:::info

You can execute the code either in your computer or online:
* online. Create an account in https://repl.it
        ![](https://i.imgur.com/oW5EJIc.png)
* in your computer. You must have python3 installed and the `paho-mqtt` library:

```
$ sudo pip3 install paho-mqtt
```



The documentation of the MQTT Paho API is here: https://www.eclipse.org/paho/clients/python/docs/ 
:::

> The code of this section is in [the code directory](https://github.com/pmanzoni/phdunimed/tree/main/code/flask-master). 

## Programming MQTT

In this part we will use a **public broker**. There are various public brokers (also called `sandboxes`) in the Internet. For example:
* `iot.eclipse.org` (https://iot.eclipse.org/projects/sandboxes/)
* `test.mosquitto.org` (http://test.mosquitto.org/)
* `broker.hivemq.com` (https://www.hivemq.com/public-mqtt-broker/)


An extensive list is available here:  https://github.com/mqtt/mqtt.github.io/wiki/public_brokers


A local broker can be run as a container, too. Mosquitto has an official image here:
https://hub.docker.com/_/eclipse-mosquitto

![](https://i.imgur.com/WgKPEna.png)

The simplest form to execute the broker is: 
```
docker run -it -p 1883:1883 eclipse-mosquitto:1.6
```

the more complete form is, as indicated in the docker hub:
```
docker run -it -p 1883:1883 -p 9001:9001 -v mosquitto.conf:/mosquitto/config/mosquitto.conf -v /mosquitto/data -v /mosquitto/log eclipse-mosquitto
```


### A simple subscriber

File: `sisub.py` cointains the code of a simple python subscriber. This code connects to a public broker and subscribes to topic `$SYS/#`.

Let's see:
:::info
https://repl.it/@pmanzoni/sisubbase
:::

### A simple producer

File: `sipub.py` cointains the code of a simple python producer. This code connects to a public broker and periodically publishes random values to topic `"PMtest/rndvalue"`

Let's see:
:::info
https://repl.it/@pmanzoni/sipubtest
:::

To check whether this is working we can use the previous code `sisub.py` ... with a [slight modification.](https://repl.it/@pmanzoni/sisubforsipub#main.py)




## Getting data from TTN

[The Things Network uses MQTT](https://www.thethingsnetwork.org/docs/applications/mqtt/index.html)to publish device activations and messages, but also allows you to publish a message for a specific device in response.

We will now use MQTT to get information from TTN as we did in the InfluxDB case. The basic data we need is the following:

``` 
Broker: eu.thethings.network
Username: lopy2ttn
Password: ttn-account-v2.TPE7-bT_UDf5Dj4XcGpcCQ0Xkhj8n74iY-rMAyT1bWg
Topic: +/devices/+/up
``` 

As a first example we will modify the code of sisub.py to get the raw information from TTN

Let's see:
:::info
https://repl.it/@pmanzoni/sisubttn1
:::

The structure of the raw message is: 
:::success
```
{
  "app_id": "lopy2ttn",
  "dev_id": "lopysense2",
  "hardware_serial": "70B3D5499269BFA7",
  "port": 2,
  "counter": 12019,
  "payload_raw": "Qbz/OEJCrHhBybUc",
  "payload_fields": {
    "humidity": 48.668426513671875,
    "lux": 25.21343231201172,
    "temperature": 23.624618530273438
  },
  "metadata": {
    "time": "2020-11-18T11:30:55.237000224Z",
    "frequency": 868.3,
    "modulation": "LORA",
    "data_rate": "SF12BW125",
    "airtime": 1482752000,
    "coding_rate": "4/5",
    "gateways": [
      {
        "gtw_id": "eui-b827ebfffe7fe28a",
        "timestamp": 3107581196,
        "time": "2020-11-18T11:30:55.204908Z",
        "channel": 1,
        "rssi": 1,
        "snr": 11.2,
        "rf_chain": 0,
        "latitude": 39.48262,
        "longitude": -0.34657,
        "altitude": 10
      },
      {
        "gtw_id": "eui-b827ebfffe336296",
        "timestamp": 661685116,
        "time": "",
        "channel": 1,
        "rssi": -83,
        "snr": 7.5,
        "rf_chain": 0
      },
      {
        "gtw_id": "itaca",
        "timestamp": 2391735892,
        "time": "2020-11-18T11:30:55Z",
        "channel": 0,
        "rssi": -117,
        "snr": -13,
        "rf_chain": 0
      }
    ]
  }
}
```
:::

Now we can sligtly modify the code to get a specific piece of information:

:::info
https://repl.it/@pmanzoni/sisubttn2
:::

To get sometthing like this:
```
Got this temperature value:
22.88459014892578
from these gateways:
eui-b827ebfffe336296 -82
eui-b827ebfffe7fe28a 3
itaca -114
```

OK, so know what if we want to "containerize" this app so that simply running as: 

:::warning
docker run -t pmanzoni/subttn
:::

we will get the result above? 
Which is the content of the Dockerfile?
Which are the steps to follow?

