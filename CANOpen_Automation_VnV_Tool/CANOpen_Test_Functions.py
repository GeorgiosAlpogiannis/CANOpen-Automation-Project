import clr
import sys
import time
import re
import Pars
import Main
from Main import *
import struct
import random
import DS402_Test_Functions
from DS402_Test_Functions import *
import Misc_Test_Functions
from Misc_Test_Functions import *
# Import .dll and connection setup
sys.path.append(r"./Output/RoboLabViewUtils")
clr.AddReference("RoboLabViewUtils")
from Roboteq.LabView.Utils import RoboController, RoboControllerBaudRate, RoboException

# Apply_config_and_restart
def apply_config_and_restart(controller,test_nr,t_wait,test_passes,test_fails,handle):
    test_name = "Apply Configuration and Restart"
    print_separator(test_name)
    passed = True
    result_init = controller.GetConfig("otl", 1)
    print(f"Configuration read result: {result_init}")
    # Write a value to a variable
    controller.SetConfig("otl", 1, 84)

    # Save the configuration to the controller
    controller.SetMaintenance("eesav", 0, 0)
    time.sleep(1)
    controller_reboot(controller,handle)
    time.sleep(t_wait)
    attempts = 1
    result_mid = 0
    write_fail = True
    while (attempts < Pars.attempts) and write_fail:
        try:
            result_mid = controller.GetConfig("otl", 1)
        except RoboException as e:
            print("Get Config failure. Attempting once more. Total # of attempts is", attempts)
            controller_reboot(controller,handle)
            time.sleep(0.1)  # Wait a bit after the reset command
        print(f"Configuration read result: {result_mid}")
        if result_mid > 0:
            write_fail = False
        attempts += 1
        time.sleep(t_wait)  # Wait a bit after the restart command
    print("attempts is", attempts, "write_fail is", write_fail)

    try:
        controller.SetMaintenance("eerst", 0, 321654987)
    except RoboException as e:
        print("Reset command not deployed successfully. Waiting before reconnecting.")
        time.sleep(0.1)  # Wait a bit after the reset command

        # Reconnect to the controller with the default settings
    try:
        controller.Disconnect()  # Ensure disconnected before attempting to reconnect
        # Use default baud rate for reconnection
        baud_rate_name = RoboControllerBaudRate.Baud_250K
        controller.Connect(handle, baud_rate_name, 1)
        print("Successfully reconnected to the controller after reset.")
    except Exception as e:
        print(f"Failed to reconnect after reset: {e}")
        passed = False
        return  # Exit if reconnection fails

        # Check if the configuration value has been reset to its original value
    result_fin = controller.GetConfig("otl", 1)
    print(f"Configuration read result after reset: {result_fin}")
    if result_fin == result_init and result_mid == 84:
        print("Setting has been reset to Defaults successfully")
        passed = True
        [test_passes,test_fails] = print_test_result(test_name, passed,test_nr,test_passes,test_fails)
    else:
        print("Setting has not been reset to Defaults successfully")
        passed = False
        [test_passes,test_fails] = print_test_result(test_name, passed,test_nr,test_passes,test_fails)
    test_nr +=1
    return(test_nr,test_passes,test_fails)

# Apply_calib_change_and_restart
def calibration_retention(controller,test_nr,t_wait,test_passes,test_fails,handle):
    test_name = "Apply Calibration change, save and Reboot"
    ZPAC_test_value = 50
    print_separator(test_name)
    passed = True
    result_init = controller.GetConfig("zpac", 1)
    print(f"Configuration read result: {result_init}")
    # Write a value to a variable
    controller.SetConfig("zpac", 1, ZPAC_test_value)

    # Save the configuration to the controller
    controller.SetMaintenance("eesav", 0, 0)
    controller.SetMaintenance("clsav", 0, 321654987)
    controller_reboot(controller,handle)
    time.sleep(t_wait)
    attempts = 1
    result_mid = 0
    write_fail = True
    while (attempts < Pars.attempts) and write_fail:
        try:
            result_mid = controller.GetConfig("zpac", 1)
        except RoboException as e:
            print("Get Config failure. Attempting once more. Total # of attempts is", attempts)
            controller_reboot(controller,handle)
            time.sleep(0.1)  # Wait a bit after the reset command
        print(f"Configuration read result: {result_mid}")
        if result_mid > 0:
            write_fail = False
        attempts += 1
        time.sleep(t_wait)  # Wait a bit after the restart command
    print("attempts is", attempts, "write_fail is", write_fail)

    if result_mid == ZPAC_test_value:
        print("Calibration retained successfully, ZPAC = ",result_mid)
        passed = True
        [test_passes,test_fails] = print_test_result(test_name, passed,test_nr,test_passes,test_fails)
    else:
        print("Calibration was not retained successfully, ZPAC = ",result_mid)
        passed = False
        [test_passes,test_fails] = print_test_result(test_name, passed,test_nr,test_passes,test_fails)
    #restore ZPAC
    controller.SetConfig("zpac", 1, result_init)
    # Save the configuration to the controller
    controller.SetMaintenance("eesav", 0, 0)
    controller.SetMaintenance("clsav", 0, 321654987)
    test_nr +=1
    return(test_nr,test_passes,test_fails)


# First test, Heartbeat change, V3.1
def manage_heartbeat(controller, value,test_nr,test_passes,test_fails) :
    test_name = "Heartbeat Change"
    print_separator(test_name)
    # Read the current heartbeat rate
    current_heartbeat = controller.GetConfig("CHB", 0)

    if current_heartbeat is not None:
        print(f"Current heartbeat rate: {current_heartbeat}")
    else:
        print("Failed to read the current heartbeat rate.")
    # Set the new heartbeat rate
    controller.SetConfig("CHB",0, value)
    new_heartbeat = controller.GetConfig("CHB", 0)
    print(f"Confirmed heartbeat rate: {new_heartbeat}")
    if new_heartbeat == value:
        [test_passes,test_fails] = print_test_result(test_name, True,test_nr,test_passes,test_fails)
    else:
        [test_passes,test_fails] = print_test_result(test_name, False,test_nr,test_passes,test_fails)

    # Execute the "EES" command
    controller.SetCommand("EESAV", 0, 0)
    print("EESAV command executed.")
    test_nr +=1
    return(test_nr,test_passes,test_fails)

# Baud rates test, Baud rate change V3.1
def try_baud_rates(controller,test_nr,node_id,test_passes,test_fails,handle):
    test_name = "Baud Rate Change"
    print_separator(test_name)
    passed = True
    baud_rate_command_values = {
        RoboControllerBaudRate.Baud_1M: 0,
        RoboControllerBaudRate.Baud_800K: 1,
        RoboControllerBaudRate.Baud_500K: 2,
        RoboControllerBaudRate.Baud_125K: 4,
        RoboControllerBaudRate.Baud_250K: 3,#return to default

    }
    # Process each baud rate
    for baud_rate_name, command_value in baud_rate_command_values.items():
        print(f"Setting baud rate to {baud_rate_name}")
        # Set the baud rate
        controller.SetConfig("CBR", 0, command_value)
        # Save the setting
        controller.SetCommand("EES", 0, 0)
        try:
            controller.SetCommand("RST", 0, 0)
        except RoboException as e:
            # Handle the exception
            time.sleep(0.5)
        # Try to reconnect with the new baud rate
        try:
            # Ensure disconnected before attempting to reconnect
            controller.Disconnect()
            # Attempt to connect with the new settings
            controller.Connect(handle, baud_rate_name, 1)
            print(f"Successfully set and connected with {baud_rate_name}")
        except Exception as e:
            print(f"Failed to set and connect using {baud_rate_name}: {e}")
            passed = False
        if command_value != 4 :
            print("Proceeding to next baud rate...\n")
    [test_passes,test_fails] = print_test_result(test_name, passed,test_nr,test_passes,test_fails)
    test_nr +=1
    return(test_nr,test_passes,test_fails)


# Third test, Change node id V3.1
def change_node_id(controller, new_node_id,test_nr,test_passes,test_fails,handle):
    test_name = "Change Node ID"
    print_separator(test_name)
    try:
        # Set the new node ID
        controller.SetCommand("CNOD", 0, new_node_id)
    except Exception as e:
        print("Node ID changed successfully.")

    # time.sleep(2)
    # Attempt to reconnect with the new node ID
    try:
        # Ensure disconnected before attempting to reconnect
        controller.Disconnect()
        # Attempt to reconnect. Adjust these parameters as necessary.
        controller.Connect(handle, RoboControllerBaudRate.Baud_250K, new_node_id)
        print(f"Successfully reconnected with new node ID {new_node_id}.")
        [test_passes,test_fails] = print_test_result(test_name, True,test_nr,test_passes,test_fails)
    except Exception as e:
        print(f"Failed to reconnect with new node ID {new_node_id}: {e}")
        [test_passes,test_fails] = print_test_result(test_name, False,test_nr,test_passes,test_fails)
    test_nr +=1
    return(test_nr,test_passes,test_fails)

## Change PDO Mapping Test
def change_pdo_mapping(controller, pdo_type, sub_index, value,test_nr,test_passes,test_fails):
    """
    Changes the mapping of a TPDO or RPDO.

    Args:
    controller (RoboController): The controller instance to interact with.
    pdo_type (str): 'TPDO' or 'RPDO' indicating which PDO type to modify.
    sub_index (int): The sub-index of the PDO object to change.
    value (int): The new value to map to the PDO object.
    """
    print_separator(f"Change {pdo_type} Mapping Tests")

    # Construct the command key based on pdo_type
    command_key = "tpdm" if pdo_type == "TPDO" else "rpdm"

    # Set new mapping value
    controller.SetConfig(command_key, sub_index, value)
    print(controller.GetValue("m", 2))
    # if success:
    #     print(f"Successfully set {pdo_type} mapping at sub-index {sub_index} to {value}.")
    # else:
    #     print(f"Failed to set {pdo_type} mapping at sub-index {sub_index}.")
    #     print_test_result(f"Change {pdo_type} Mapping Tests", False,test_nr,test_passes,test_fails)
    #     return

    # Confirm the new mapping by reading it back
    confirmed_value = controller.GetConfig(command_key, sub_index)
    if confirmed_value == value:
        print(f"Confirmed new mapping for {pdo_type} at sub-index {sub_index} = {confirmed_value}.")
        [test_passes,test_fails] = print_test_result(f"Change {pdo_type} Mapping Tests", True,test_nr,test_passes,test_fails)
    else:
        print(
            f"Mapping confirmation failed for {pdo_type} at sub-index {sub_index}. Expected {value}, got {confirmed_value if confirmed_value is not None else 'None'}.")
        [test_passes,test_fails] = print_test_result(f"Change {pdo_type} Mapping Tests", False,test_nr,test_passes,test_fails)
    test_nr += 1
    return(test_nr,test_passes,test_fails)


def set_rpdo_value(controller, node_id, rpdo_index, sub_index, value, rpdo_number,test_nr):
    fail_counter = 0
    """
    Sets a value for a specific RPDO variable.

    Args:
    controller: Instance of RoboController.
    node_id: Node ID of the CANopen device.
    rpdo_index: Index of the RPDO object.
    sub_index: Sub-index of the RPDO object variable.
    value: New value to set for the RPDO variable.
    """
    # Convert integer value to byte array (2 bytes, little endian)
    data_to_write = struct.pack('<l', value)

    # Write the new value to the specified SDO index and sub-index
    success = controller.WriteObject(controller.SdoTimeout, 1, rpdo_index, sub_index, data_to_write)
    if success:
        # print(f"Successfully set RPDO{rpdo_number}, sub-index {sub_index} to {value}.")
        time.sleep(Pars.t_wait_vshort)
    else:
        print(f"Failed to set RPDO{rpdo_number}, sub-index {sub_index}.")
        # print_test_result("Set RPDO Values Tests", False,test_nr,test_passes,test_fails)  # Update criteria as needed
        test_nr += 1
        fail_counter+=1
        return (test_nr,fail_counter)

    # Optionally confirm the new value by reading it back
    confirmed_value = (controller.GetValue("Var", sub_index))
    if confirmed_value == value:
        # print(f"Confirmed new value for RPDO{rpdo_number}, var{sub_index} = {confirmed_value}.")
        time.sleep(Pars.t_wait_vshort)
    else:
        print(f"Value confirmation failed for RPDO{rpdo_number}, var{sub_index}. Expected {value}, got {confirmed_value if confirmed_value is not None else 'None'}.")
        test_nr += 1
        fail_counter+=1
        return (test_nr,fail_counter)
    test_nr += 1
    # print_test_result("Set RPDO Values Tests", False,test_nr,test_passes,test_fails)
    return (test_nr,fail_counter)


def read_tpdo_value(controller, node_id, sub_index, tpdo_number, var_number,test_nr):
    """
    Read the current value from a specific TPDO's variable.

    Args:
    controller (RoboController): The controller instance to interact with.
    node_id (int): The node ID of the CANopen device.
    tpdo_number (int): The TPDO number (1 to 8).
    var_number (int): The variable number (1 or 2) under the chosen TPDO to read.
    """
    fail_counter = 0
    # Base index for TPDO mappings
    base_index = 0x2106
    controller.SetCommand("var", var_number, random.randint(1, 999))
    # Read the current value at the specified index and sub-index
    current_value = controller.ReadObjectS32(controller.SdoTimeout, 1, base_index, sub_index)
    if current_value is not None:
        # print(f"Current value at TPDO{tpdo_number} var{var_number}: {current_value}")
        time.sleep(Pars.t_wait_vshort)
    else:
        print(f"Failed to read value at TPDO{tpdo_number} var{var_number}.")
        test_nr += 1
        fail_counter+= 1
    return (test_nr, fail_counter)
