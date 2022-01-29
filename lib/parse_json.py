"""Read network json files.

Author(s): Tim McNamara
Created Date: 12-28-2021
Updated Date: ----------
Email: tmcnama2@cmu.edu
Status: Development

Read input json file, instantiate object for each device, and return objects in dictionary

Usage:
	network_data = parse_json(json_file='input.json')
"""

from json import load
from classes.Nodes import Nodes
from classes.Resistors import Resistors
from classes.Capacitors import Capacitors
from classes.Inductors import Inductors
from classes.Switches import Switches
from classes.VoltageSources import VoltageSources
from classes.InductionMotors import InductionMotors
from classes.Devices import Devices

def parse_json(json_file):
    with open(json_file, 'r') as f:
        json_data = load(f)

    devices = Devices()

    for ele_data in json_data['nodes']:
        devices.nodes.append(Nodes(
            ele_data['name'],
            ele_data['phase']
        ))

    for ele_data in json_data['resistors']:
        devices.resistors.append(Resistors(
            ele_data['name'],
            ele_data['from_node'], 
            ele_data['to_node'],
            ele_data['r']
        ))

    for ele_data in json_data['capacitors']:
        devices.capacitors.append(Capacitors(
            ele_data['name'],
            ele_data['from_node'], 
            ele_data['to_node'],
            ele_data['c']
        ))

    for ele_data in json_data['inductors']:
        devices.inductors.append(Inductors(
            ele_data['name'],
            ele_data['from_node'], 
            ele_data['to_node'],
            ele_data['l']
        ))

    for ele_data in json_data['switches']:
        devices.switches.append(Switches(
            ele_data['name'],
            ele_data['from_node'], 
            ele_data['to_node'],
            ele_data['t_open'],
            ele_data['t_close']
        ))

    for ele_data in json_data['voltage_sources']:
        devices.voltage_sources.append(VoltageSources(
            ele_data['name'],
            ele_data['vp_node'], 
            ele_data['vn_node'],
            ele_data['amp_ph_ph_rms'],
            ele_data['phase_deg'],
            ele_data['frequency_hz']
        ))

    for ele_data in json_data['induction_motors']:
        devices.induction_motors.append(InductionMotors(
            ele_data['name'],
            ele_data['phase_a_node'],
            ele_data['phase_b_node'],
            ele_data['phase_c_node'],
            ele_data['power_nom'],
            ele_data['v_nom'],
            ele_data['motor_freq'],
            ele_data['lm'],
            ele_data['rs'],
            ele_data['rr'],
            ele_data['lls'],
            ele_data['llr'],
            ele_data['j'],
            ele_data['tm'],
            ele_data['d_fric'],
            ele_data['n_pole_pairs']
        ))

    return devices


