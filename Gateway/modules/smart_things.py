import sys
import json

sys.path.append("..")
from helpers.iotdb_smartthings import smartthings as st

#
# https://github.com/dpjanes/iotdb-smartthings for SmartThings wrapper
# David Janes
# IOTDB.org
# 2014-01-31
# see Gateway/helpers/ for more details
# Calls the wrapper cleanly, acting as the module face to user-applications.
# In this case, calls wrapper but combines its functions to create richer functions

devices = [ # smart devices types supported by wrapper
    "switch", "motion", "acceleration", "contact",
    "temperature", "battery", "acceleration", "threeAxis", "humidity"
]

smartthings = st.SmartThings("")
smartthings.load_settings(filename = "helpers/iotdb_smartthings/smartthings.json")
smartthings.request_endpoints()

def list_types(): # list types as above (line 15)
    return json.dumps({"types": devices})

def list_devices(): # for each type in (line 15) gets all devices of kind in network
    devices_available = {}
    for device_type in devices:
        devices_of_type = smartthings.request_devices(device_type)

        for device in devices_of_type:
            if device["label"] not in devices_available:
                devices_available[device["label"]] = {"id": device["id"], "type": device["type"], "value": device["value"]}

    return json.dumps(devices_available)

def find_of_type(device_type): # get available devices of a specified type
    """device_type: e.g. switch, motion, acceleration, contact,
    temperature, battery, acceleration, threeAxis, humidity"""

    devices_of_type = smartthings.request_devices(device_type)
    devices_available = {}

    if device_type in devices:
        for device in devices_of_type:
            if device["label"] not in devices_available:
                devices_available[device["label"]] = {"type": device["type"], "value": device["value"]}

        return json.dumps(devices_available)

    else:
        return json.dumps({"error": "{} does not exist in device type, see list_types".format(device_type)})

def toggle_switch(device_id_or_label):
    """device_id_or_label: Use list_devices(), returned label or id field are usable as arg here"""
    device_type = "switch"

    devices = smartthings.request_devices(device_type)
    devices = filter(lambda d: device_id_or_label in [ d.get("id"), d.get("label"), ], devices)

    for device in devices:
        if device_type in device["type"]:
            smartthings.device_request(device, {"switch": -1})
            return json.dumps({"success": "device {} toggled".format(device_id_or_label)})
        else:
            return json.dumps({"error": "Device {} is not of type {}".format(device_id_or_label, device_type)})

    return json.dumps({"error": "Device {} is not found".format(device_id_or_label)})


def device_state(device_name):
    """device_name: e.g. Hue white lamp 1"""
    for device_type in devices:
        ds = smartthings.request_devices(device_type)
        ds = filter(lambda d: device_name in [ d.get("id"), d.get("label"), ], ds) # adapted from original

        for d in ds:
            key = list(d["value"].keys())[-1]
            value = d["value"][key]
            return json.dumps({key: value})

def get_mac():
    return "0"
