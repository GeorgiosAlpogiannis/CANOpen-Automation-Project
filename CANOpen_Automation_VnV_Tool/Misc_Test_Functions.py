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
import CANOpen_Test_Functions
from CANOpen_Test_Functions import *


# Import .dll and connection setup
sys.path.append(r"./Output/RoboLabViewUtils")
clr.AddReference("RoboLabViewUtils")
from Roboteq.LabView.Utils import RoboController, RoboControllerBaudRate, RoboException


# Function to print test separator
def print_separator(test_name):
    print("\n" + "-" * 50)
    print(f"Starting Test: {test_name}")
    print("-" * 50)

# Function to print test result
def print_test_result(test_name, passed,test_nr,test_passes,test_fails):
    if passed:
        print(f"Test Nr {test_nr} : {test_name}: PASSED")
        test_passes += 1
    else:
        print(f"Test Nr {test_nr} : {test_name}: FAILED")
        test_fails += 1
        print("test_fails")

    print("-" * 50 + "\n")
    return(test_passes,test_fails)

# Fifth test, Lock - Unlock
def lock_get_unlock(controller,test_nr,test_passes,test_fails):
    test_name = "Lock, Get Config, and Unlock"
    print_separator(test_name)

    # Lock the configuration
    controller.SetMaintenance("LK", 0, 123456789)
    print("Configuration locked.")

    # Attempt to get the configuration value
    try:
        current_value = controller.GetConfig("OVL", 0)
        print(f"Current 'OVL' configuration value: {current_value}")
    except RoboException as e:
        print(f"Configuration can not be read because it is locked.")

    # Unlock the configuration
    controller.SetMaintenance("UK", 0, 123456789)
    print("Configuration unlocked.")

    # Retry getting the configuration value
    try:
        current_value = controller.GetConfig("OVL", 0)
        print(f"'OVL' configuration value after unlocking: {current_value}")
    except RoboException as e:
        print(f"Unexpected exception when retrying to get 'OVL': {e}")
        [test_passes,test_fails] = print_test_result(test_name, False,test_nr,test_passes,test_fails)
        test_nr += 1
        return (test_nr, test_passes, test_fails)

    [test_passes,test_fails] = print_test_result(test_name, True,test_nr,test_passes,test_fails)
    test_nr +=1
    return(test_nr,test_passes,test_fails)


# Sixth test overvoltage protection fault flags
def test_overvoltage_protection(controller,test_nr,test_passes,test_fails):
    #
    test_name = "Over-voltage protection Fault Flag"
    print_separator(test_name)
    controller.SetConfig('SED', 1, 0)
    controller.SetConfig('SED', 2, 0)

    # Step 1: Set OVL lower than current voltage to trigger overvoltage fault
    controller.SetConfig("OVL", 0, 150)
    print("Set OVL to 15.0V to trigger overvoltage fault.")
    controller.SetCommand("EESAV", 0, 0)
    time.sleep(0.5)
    # Remove Emergency stop
    controller.SetCommand("MG", 0, 0)
    # Step 2: Check overvoltage fault flag
    overvoltage_fault = controller.GetValue("FF", 0)
    print(f"Fault Flag: {overvoltage_fault}")

    if overvoltage_fault == 2 or overvoltage_fault == 18:
        print("Over-voltage Fault Flag successfully triggered!")
    else:
        [test_passes,test_fails] = print_test_result("Over-voltage Protection Test", False,test_nr,test_passes,test_fails)
        test_nr += 1
        return(test_nr,test_passes,test_fails)

    # Step 3: Reset OVL to a normal range
    controller.SetConfig("OVL", 0, 600)
    print("Reset OVL to 60.0V.")
    controller.SetCommand("EESAV", 0, 0)
    time.sleep(0.5)
    # Step 4: Verify overvoltage fault is cleared
    fault_reset = controller.GetValue("FF", 0)
    print(f"Fault Flag after resetting OVL: {fault_reset}")

    # Decide on pass/fail criteria based on fault flags
    [test_passes,test_fails] = print_test_result("Over-voltage Protection Test", True,test_nr,test_passes,test_fails)  # Update criteria as needed
    test_nr +=1
    return(test_nr,test_passes,test_fails)

# Seventh test undervoltage protection
def test_undervoltage_protection(controller,test_nr,test_passes,test_fails):
    #
    test_name = "Under-voltage protection Fault Flag"
    print_separator(test_name)
    controller.SetConfig('SED', 1, 0)
    controller.SetConfig('SED', 2, 0)

    # Step 1: Set UVL higher than current voltage to trigger overvoltage fault
    # Adjust the controller's voltage from your supply as needed
    controller.SetConfig("UVL", 0, 500)
    print("Set UVL to 50.0V to trigger Under-voltage fault.")
    controller.SetCommand("EESAV", 0, 0)
    time.sleep(0.5)
    # Remove Emergency stop
    controller.SetCommand("MG", 0, 0)
    # Step 2: Check Undervoltage fault flag
    undervoltage_fault = controller.GetValue("FF", 0)
    print(f"Fault Flag: {undervoltage_fault}")

    if undervoltage_fault == 4 or undervoltage_fault == 20:
        print("Under-voltage Fault Flag successfully triggered!")
    else:
        [test_passes,test_fails] = print_test_result("Under-voltage Protection Test", False,test_nr,test_passes,test_fails)
        test_nr += 1
        return(test_nr,test_passes,test_fails)

    # Step 3: Reset UVL to a normal range
    controller.SetConfig("UVL", 0, 100)
    print("Reset OVL to 10.0V.")
    controller.SetCommand("EESAV", 0, 0)
    time.sleep(0.5)
    # Step 4: Verify undervoltage fault is cleared
    fault_reset = controller.GetValue("FF", 0)
    print(f"Fault Flag after resetting UVL: {fault_reset}")

    # Decide on pass/fail criteria based on fault flags
    [test_passes,test_fails] = print_test_result("Under-voltage Protection Test", True,test_nr,test_passes,test_fails)  # Update criteria as needed
    test_nr +=1
    return(test_nr,test_passes,test_fails)

# Eighth test Over-temp protection
def test_overtemp_protection(controller,test_nr,test_passes,test_fails):
    #
    test_name = "Over-heat protection Fault Flag"
    print_separator(test_name)
    controller.SetConfig('SED', 1, 0)
    controller.SetConfig('SED', 2, 0)

    # Step 1: Set OTL higher than current voltage to trigger overtemp fault
    controller.SetConfig("OTL", 1, 5)
    print("Set OTL to 5 Celsius degrees to trigger Over-Temperature fault.")
    controller.SetCommand("EESAV", 0, 0)
    time.sleep(1)
    # Remove Emergency stop
    controller.SetCommand("MG", 0, 0)
    # Step 2: Check Overtemp fault flag
    overtemp_fault = controller.GetValue("FF", 0)
    print(f"Fault Flag: {overtemp_fault}")

    if overtemp_fault == 1 or overtemp_fault == 17:
        print("Over-heat Fault Flag successfully triggered!")
    else:
        [test_passes,test_fails] = print_test_result("Over-heat Protection Test", False,test_nr,test_passes,test_fails)
        test_nr +=1
        return(test_nr,test_passes,test_fails)

    # Step 3: Reset OTL to a normal range
    controller.SetConfig("OTL", 1, 85)
    print("Reset OTL to 85 Celsius degrees.")
    controller.SetCommand("EESAV", 0, 0)
    time.sleep(0.5)
    # Step 4: Verify overvoltage fault is cleared
    fault_reset = controller.GetValue("FF", 0)
    print(f"Fault Flag after resetting UVL: {fault_reset}")

    # Decide on pass/fail criteria based on fault flags
    [test_passes,test_fails] = print_test_result("Over-heat Protection Test", True,test_nr,test_passes,test_fails)  # Update criteria as needed
    test_nr +=1
    return(test_nr,test_passes,test_fails)

# Ninth test Estop protection
def test_estop_protection(controller,test_nr,test_passes,test_fails):
    #
    test_name = "Emergency-stop protection Flag"
    print_separator(test_name)
    controller.SetConfig('SED', 1, 0)
    controller.SetConfig('SED', 2, 0)

    # Step 1: Activate emergency stop
    controller.SetCommand("EX", 0, 0)
    time.sleep(1)
    # Step 2: Check Estop fault flag
    estop_fault = controller.GetValue("FF", 0)
    print(f"Fault Flag: {estop_fault}")
    if estop_fault == 16:
        print("Estop Flag successfully triggered!")
    else:
        [test_passes,test_fails] = print_test_result("Estop Protection Test", False,test_nr,test_passes,test_fails)
        return(test_nr,test_passes,test_fails)
    # # Step 3: Remove Emergency stop
    controller.SetCommand("MG", 0, 0)
    print("Emergency stop has been deactivated")
    time.sleep(1)
    # Step 4: Verify overvoltage fault is cleared
    fault_reset = controller.GetValue("FF", 0)
    print(f"Fault Flag after disengaging estop: {fault_reset}")

    # Decide on pass/fail criteria based on fault flags
    [test_passes,test_fails] = print_test_result("Estop Protection Test", True,test_nr,test_passes,test_fails)  # Update criteria as needed
    test_nr +=1
    return(test_nr,test_passes,test_fails)

# Function to reboot the controller
def controller_reboot(controller,handle):
    try:
        # controller.SetCommand("RST", 0, 0)
        controller.SetMaintenance("reset", 0, 321654987)

    except RoboException as e:
        # Handle the exception
        time.sleep(1)
    baud_rate_v = RoboControllerBaudRate.Baud_250K
    # Try to reconnect with the new baud rate
    try:
        # Ensure disconnected before attempting to reconnect
        controller.Disconnect()
        time.sleep(0.2)
        # Attempt to connect with the new settings
        controller.Connect(handle, baud_rate_v, 1)
        print(f"Successfully set and connected with {baud_rate_v}")
        time.sleep(0.2)
    except Exception as e:
        print(f"Failed to set and connect using {baud_rate_v}: {e}")
        time.sleep(0.2)


# Function to reset the controller to defaults
def reset_to_defaults_and_reconnect(controller,handle):
    # Attempt to reset the controller using the "eerst" command
    try:
        controller.SetMaintenance("eerst", 0, 321654987)
    except RoboException as e:
        print("Reset to Defaults deployed successfully. Waiting before reconnecting.")
        time.sleep(0.1)  # Wait a bit after the reset command

    # Attempt to reconnect to the controller with the default settings
    try:
        controller.Disconnect()  # Ensure disconnected before attempting to reconnect
        # Use default baud rate for reconnection
        baud_rate_name = RoboControllerBaudRate.Baud_250K
        controller.Connect(handle, baud_rate_name, 1)
        print("Successfully reconnected to the controller after reset to defaults.")
    except Exception as e:
        print(f"Failed to reconnect after reset to defaults: {e}")

# Function to read controller's FW version
def extract_version(s):
    match = re.search(r'v(\d+\.\d+)', s)
    if match:
        return match.group(1)
    else:
        return None
# Fourth test, EESAV, RESET, EERST V3.1


# Tenth test Run motor in OL - CL
def run_motor_and_switch_mode(controller,test_nr):
    print_separator("Motor Run and Mode Switch Test")
    # Set WatchDog protection to 0
    controller.SetConfig("RWD", 0, 0)
    # Remove ESTOP to run the motor
    controller.SetCommand("MG", 0, 0)
    # Run the motor with open loop
    print("Running motor in open loop mode...")
    controller.SetConfig("MMOD", 1, 0)  # Set mode to closed-loop speed for channel 1
    controller.SetCommand("CG", 1, 300)  # Assuming channel 1, adjust if necessary
    time.sleep(10)  # Run for a short period; adjust as needed
    controller.SetCommand("CG", 1, 0)    # Stop the motor
    print("Motor stopped.")

    # Change operation mode to closed-loop speed
    print("Switching to closed-loop speed mode...")
    controller.SetConfig("MMOD", 1, 1)  # Set mode to closed-loop speed for channel 1
    controller.SetCommand("EESAV", 0, 0)  # Save the setting
    print("Mode switched and saved. Restarting the motor in closed-loop speed mode...")
    time.sleep(10)
    # Remove ESTOP to run the motor
    controller.SetCommand("MG", 0, 0)
    # Restart the motor in closed-loop speed mode
    controller.SetCommand("CG", 1, 800)  # Run motor in closed-loop speed mode
    time.sleep(15)  # Run for a period; adjust as needed
    controller.SetCommand("CG", 1, 0)    # Stop the motor
    print("Motor stopped in closed-loop speed mode.")

    # Decide on pass/fail criteria based on fault flags
    print_test_result("Motor Run and Mode Switch Test", True,test_nr,test_passes,test_fails)  # Update criteria as needed
    test_nr +=1
    return(test_nr)
# Eleventh test Enable DS402 and Change Modes of operation

def check_bit_high(status, position):
    """
    Check if the bit at the given position is high.

    Args:
    status (int): The status word (16-bit integer).
    position (int): The position of the bit to check (0-indexed).

    Returns:
    bool: True if the bit is high, False if the bit is low.
    """
    # Shift the bit in the 'position' to the least significant bit and mask with 1
    time.sleep(Pars.t_wait_mid_short)
    return (status & (1 << position)) != 0
