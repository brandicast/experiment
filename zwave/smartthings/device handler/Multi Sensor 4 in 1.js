/**
 *  Brandicast Muilti Sensor 4 in 1
 *
 *  Copyright 2020 Brandon Wu
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 */
metadata {
	definition (name: "Brandicast Muilti Sensor 4 in 1", namespace: "Brandicast", author: "Brandon Wu", cstHandler: true) {
		capability "Battery"
		capability "Contact Sensor"
		capability "Motion Sensor"
		capability "Tamper Alert"
		capability "Temperature Measurement"
		capability "Illuminance Measurement"
        capability "Refresh"
        capability "Polling"

		fingerprint mfr: "013C", prod: "0002", model: "000C", deviceJoinName: "Philio 4 in 1 Sensor", cc:"5E,72,86,59,73,5A,8F,98,7A", ccOut:"20", sec:"80,71,85,70,30,31,84"
	}


	simulator {
		// TODO: define status and reply messages here
                status "temperature report 72°F":
                         zwave.sensorMultilevelV2.sensorMultilevelReport(scaledSensorValue: 70.0, precision: 1, sensorType: 1, scale: 1).incomingMessage()
                status "sample": "xxxx"
                	
                reply "2001FF,delay 100,2502": "command: 2503, payload: FF"                   

	}

	tiles {
		// TODO: define your main and details tiles here
	}
}

def parse(String description) {
        def result = null
         log.debug "Received: '$description'"
        def cmd = zwave.parse(description, [0x60: 3])
        if (cmd) {
                result = zwaveEvent(cmd)
                log.debug "Parsed ${cmd} to ${result.inspect()}"
        } else {
                log.debug "Non-parsed event: ${description}"
        }
        return result
}


def test(){
	log.debug "test !"
}

def hello(){
	log.debug "Hello  !"
}


def zwaveEvent(physicalgraph.zwave.commands.basicv1.BasicReport cmd)
{
        def result = []
        result << createEvent(name:"switch", value: cmd.value ? "on" : "off")

        // For a multilevel switch, cmd.value can be from 1-99 to represent
        // dimming levels
        result << createEvent(name:"level", value: cmd.value, unit:"%",
                    descriptionText:"${device.displayName} dimmed ${cmd.value==255 ? 100 : cmd.value}%")

        result
}

def zwaveEvent(physicalgraph.zwave.commands.switchbinaryv1.SwitchBinaryReport cmd) {
        createEvent(name:"switch", value: cmd.value ? "on" : "off")
}

def zwaveEvent(physicalgraph.zwave.commands.switchmultilevelv3.SwitchMultilevelReport cmd) {
        def result = []
        result << createEvent(name:"switch", value: cmd.value ? "on" : "off")
        result << createEvent(name:"level", value: cmd.value, unit:"%",
                     descriptionText:"${device.displayName} dimmed ${cmd.value==255 ? 100 : cmd.value}%")
        result
}

def zwaveEvent(physicalgraph.zwave.commands.meterv1.MeterReport cmd) {
        def result
        if (cmd.scale == 0) {
                result = createEvent(name: "energy", value: cmd.scaledMeterValue,
                                     unit: "kWh")
        } else if (cmd.scale == 1) {
                result = createEvent(name: "energy", value: cmd.scaledMeterValue,
                                     unit: "kVAh")
        } else {
                result = createEvent(name: "power",
                                     value: Math.round(cmd.scaledMeterValue), unit: "W")
        }

        result
}

def zwaveEvent(physicalgraph.zwave.commands.meterv3.MeterReport cmd) {
        def map = null
        if (cmd.meterType == 1) {
                if (cmd.scale == 0) {
                        map = [name: "energy", value: cmd.scaledMeterValue,
                               unit: "kWh"]
                } else if (cmd.scale == 1) {
                        map = [name: "energy", value: cmd.scaledMeterValue,
                               unit: "kVAh"]
                } else if (cmd.scale == 2) {
                        map = [name: "power", value: cmd.scaledMeterValue, unit: "W"]
                } else {
                        map = [name: "electric", value: cmd.scaledMeterValue]
                        map.unit = ["pulses", "V", "A", "R/Z", ""][cmd.scale - 3]
                }
        } else if (cmd.meterType == 2) {
                map = [name: "gas", value: cmd.scaledMeterValue]
                map.unit =      ["m^3", "ft^3", "", "pulses", ""][cmd.scale]
        } else if (cmd.meterType == 3) {
                map = [name: "water", value: cmd.scaledMeterValue]
                map.unit = ["m^3", "ft^3", "gal"][cmd.scale]
        }
        if (map) {
                if (cmd.previousMeterValue && cmd.previousMeterValue != cmd.meterValue) {
                        map.descriptionText = "${device.displayName} ${map.name} is ${map.value} ${map.unit}, previous: ${cmd.scaledPreviousMeterValue}"
                }
                createEvent(map)
        } else {
                null
        }
}

def zwaveEvent(physicalgraph.zwave.commands.sensorbinaryv2.SensorBinaryReport cmd) {
        def result
        switch (cmd.sensorType) {
                case 2:
                        result = createEvent(name:"smoke",
                                value: cmd.sensorValue ? "detected" : "closed")
                        break
                case 3:
                        result = createEvent(name:"carbonMonoxide",
                                value: cmd.sensorValue ? "detected" : "clear")
                        break
                case 4:
                        result = createEvent(name:"carbonDioxide",
                                value: cmd.sensorValue ? "detected" : "clear")
                        break
                case 5:
                        result = createEvent(name:"temperature",
                                value: cmd.sensorValue ? "overheated" : "normal")
                        break
                case 6:
                        result = createEvent(name:"water",
                                value: cmd.sensorValue ? "wet" : "dry")
                        break
                case 7:
                        result = createEvent(name:"temperature",
                                value: cmd.sensorValue ? "freezing" : "normal")
                        break
                case 8:
                        result = createEvent(name:"tamper",
                                value: cmd.sensorValue ? "detected" : "okay")
                        break
                case 9:
                        result = createEvent(name:"aux",
                                value: cmd.sensorValue ? "active" : "inactive")
                        break
                case 0x0A:
                        result = createEvent(name:"門",
                                value: cmd.sensorValue ? "打開" : "關閉")
                        break
                case 0x0B:
                        result = createEvent(name:"tilt", value: cmd.sensorValue ? "detected" : "okay")
                        break
                case 0x0C:
                        result = createEvent(name:"motion",
                                value: cmd.sensorValue ? "active" : "inactive")
                        break
                case 0x0D:
                        result = createEvent(name:"glassBreak",
                                value: cmd.sensorValue ? "detected" : "okay")
                        break
                default:
                        result = createEvent(name:"sensor",
                                value: cmd.sensorValue ? "active" : "inactive")
                        break
        }
        result
}

def zwaveEvent(physicalgraph.zwave.commands.sensorbinaryv1.SensorBinaryReport cmd)
{
        // Version 1 of SensorBinary doesn't have a sensor type
        createEvent(name:"sensor", value: cmd.sensorValue ? "active" : "inactive")
}

def zwaveEvent(physicalgraph.zwave.commands.sensormultilevelv5.SensorMultilevelReport cmd)
{
        def map = [ displayed: true, value: cmd.scaledSensorValue.toString() ]
        log.debug "Multileve report is called"
        switch (cmd.sensorType) {
                case 1:
                        map.name = "溫度 (Temperature)"
                        map.unit = cmd.scale == 1 ? "F" : "C"
                        break;
                case 2:
                        map.name = "value"
                        map.unit = cmd.scale == 1 ? "%" : ""
                        break;
                case 3:
                        map.name = "亮度"
                        map.value = cmd.scaledSensorValue.toInteger().toString()
                        map.unit = "lux"
                        break;
                case 4:
                        map.name = "power"
                        map.unit = cmd.scale == 1 ? "Btu/h" : "W"
                        break;
                case 5:
                        map.name = "humidity"
                        map.value = cmd.scaledSensorValue.toInteger().toString()
                        map.unit = cmd.scale == 0 ? "%" : ""
                        break;
                case 6:
                        map.name = "velocity"
                        map.unit = cmd.scale == 1 ? "mph" : "m/s"
                        break;
                case 8:
                case 9:
                        map.name = "pressure"
                        map.unit = cmd.scale == 1 ? "inHg" : "kPa"
                        break;
                case 0xE:
                        map.name = "weight"
                        map.unit = cmd.scale == 1 ? "lbs" : "kg"
                        break;
                case 0xF:
                        map.name = "voltage"
                        map.unit = cmd.scale == 1 ? "mV" : "V"
                        break;
                case 0x10:
                        map.name = "current"
                        map.unit = cmd.scale == 1 ? "mA" : "A"
                        break;
                case 0x12:
                        map.name = "air flow"
                        map.unit = cmd.scale == 1 ? "cfm" : "m^3/h"
                        break;
                case 0x1E:
                        map.name = "loudness"
                        map.unit = cmd.scale == 1 ? "dBA" : "dB"
                        break;
        }
        createEvent(map)
}

// Many sensors send BasicSet commands to associated devices.
// This is so you can associate them with a switch-type device
// and they can directly turn it on/off when the sensor is triggered.
def zwaveEvent(physicalgraph.zwave.commands.basicv1.BasicSet cmd)
{
        createEvent(name:"sensor", value: cmd.value ? "active" : "inactive")
}

def zwaveEvent(physicalgraph.zwave.commands.batteryv1.BatteryReport cmd) {
        def map = [ name: "battery", unit: "%" ]
        if (cmd.batteryLevel == 0xFF) {  // Special value for low battery alert
                map.value = 1
                map.descriptionText = "${device.displayName} has a low battery"
                map.isStateChange = true
        } else {
                map.value = cmd.batteryLevel
        }
        // Store time of last battery update so we don't ask every wakeup, see WakeUpNotification handler
        state.lastbatt = new Date().time
        createEvent(map)
}

// Battery powered devices can be configured to periodically wake up and
// check in. They send this command and stay awake long enough to receive
// commands, or until they get a WakeUpNoMoreInformation command that
// instructs them that there are no more commands to receive and they can
// stop listening.
def zwaveEvent(physicalgraph.zwave.commands.wakeupv2.WakeUpNotification cmd)
{
        def result = [createEvent(descriptionText: "${device.displayName} woke up", isStateChange: false)]

        // Only ask for battery if we haven't had a BatteryReport in a while
        if (!state.lastbatt || (new Date().time) - state.lastbatt > 24*60*60*1000) {
                result << response(zwave.batteryV1.batteryGet())
                result << response("delay 1200")  // leave time for device to respond to batteryGet
        }
        result << response(zwave.wakeUpV1.wakeUpNoMoreInformation())
        result
}

def zwaveEvent(physicalgraph.zwave.commands.associationv2.AssociationReport cmd) {
        def result = []
        if (cmd.nodeId.any { it == zwaveHubNodeId }) {
                result << createEvent(descriptionText: "$device.displayName is associated in group ${cmd.groupingIdentifier}")
        } else if (cmd.groupingIdentifier == 1) {
                // We're not associated properly to group 1, set association
                result << createEvent(descriptionText: "Associating $device.displayName in group ${cmd.groupingIdentifier}")
                result << response(zwave.associationV1.associationSet(groupingIdentifier:cmd.groupingIdentifier, nodeId:zwaveHubNodeId))
        }
        result
}

// Devices that support the Security command class can send messages in an
// encrypted form; they arrive wrapped in a SecurityMessageEncapsulation
// command and must be unencapsulated
def zwaveEvent(physicalgraph.zwave.commands.securityv1.SecurityMessageEncapsulation cmd) {
        def encapsulatedCommand = cmd.encapsulatedCommand([0x98: 1, 0x20: 1])

        // can specify command class versions here like in zwave.parse
        if (encapsulatedCommand) {
                return zwaveEvent(encapsulatedCommand)
        }
}

// MultiChannelCmdEncap and MultiInstanceCmdEncap are ways that devices
// can indicate that a message is coming from one of multiple subdevices
// or "endpoints" that would otherwise be indistinguishable
def zwaveEvent(physicalgraph.zwave.commands.multichannelv3.MultiChannelCmdEncap cmd) {
        def encapsulatedCommand = cmd.encapsulatedCommand([0x30: 1, 0x31: 1])

        // can specify command class versions here like in zwave.parse
        log.debug ("Command from endpoint ${cmd.sourceEndPoint}: ${encapsulatedCommand}")

        if (encapsulatedCommand) {
                return zwaveEvent(encapsulatedCommand)
        }
}

def zwaveEvent(physicalgraph.zwave.commands.multichannelv3.MultiInstanceCmdEncap cmd) {
        def encapsulatedCommand = cmd.encapsulatedCommand([0x30: 1, 0x31: 1])

        // can specify command class versions here like in zwave.parse
        log.debug ("Command from instance ${cmd.instance}: ${encapsulatedCommand}")

        if (encapsulatedCommand) {
                return zwaveEvent(encapsulatedCommand)
        }
}

def zwaveEvent(physicalgraph.zwave.Command cmd) {
        createEvent(descriptionText: "${device.displayName}: ${cmd}")
}
/*
def on() {
        delayBetween([
                zwave.basicV1.basicSet(value: 0xFF).format(),
                zwave.basicV1.basicGet().format()
        ], 5000)  // 5 second delay for dimmers that change gradually, can be left out for immediate switches
}

def off() {
        delayBetween([
                zwave.basicV1.basicSet(value: 0x00).format(),
                zwave.basicV1.basicGet().format()
        ], 5000)  // 5 second delay for dimmers that change gradually, can be left out for immediate switches
}
*/

def refresh() {
        // Some examples of Get commands
        log.debug "Refresh is called"
        delayBetween([
                //zwave.switchBinaryV1.switchBinaryGet().format(),
                zwave.switchMultilevelV1.switchMultilevelGet().format(),
                //zwave.meterV2.meterGet(scale: 0).format(),      // get kWh
               // zwave.meterV2.meterGet(scale: 2).format(),      // get Watts
                zwave.sensorMultilevelV1.sensorMultilevelGet().format(),
                zwave.sensorMultilevelV5.sensorMultilevelGet(sensorType:1, scale:0).format(),  // get temp in Fahrenheit
                zwave.batteryV1.batteryGet().format(),
                zwave.basicV1.basicGet().format(),
        ], 1200)
}

// If you add the Polling capability to your device type, this command
// will be called approximately every 5 minutes to check the device's state
def poll() {
  		log.debug "Poll is called"
        zwave.basicV1.basicGet().format()
}

/*
// If you add the Configuration capability to your device type, this
// command will be called right after the device joins to set
// device-specific configuration commands.
def configure() {
        delayBetween([
                // Note that configurationSet.size is 1, 2, or 4 and generally
                // must match the size the device uses in its configurationReport
                zwave.configurationV1.configurationSet(parameterNumber:1, size:2, scaledConfigurationValue:100).format(),

                // Can use the zwaveHubNodeId variable to add the hub to the
                // device's associations:
                zwave.associationV1.associationSet(groupingIdentifier:2, nodeId:zwaveHubNodeId).format(),

                // Make sure sleepy battery-powered sensors send their
                // WakeUpNotifications to the hub every 4 hours:
                zwave.wakeUpV1.wakeUpIntervalSet(seconds:4 * 3600, nodeid:zwaveHubNodeId).format(),
        ])
}
*/