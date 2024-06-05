#Imports
import clr
import sys
import time
import re
import Pars
import struct
import random
import DS402_Test_Functions
from DS402_Test_Functions import *
import CANOpen_Test_Functions
from CANOpen_Test_Functions import *
import Misc_Test_Functions
from Misc_Test_Functions import *
# Import .dll and connection setup
sys.path.append(r"./Output/RoboLabViewUtils")
clr.AddReference("RoboLabViewUtils")
from Roboteq.LabView.Utils import RoboController, RoboControllerBaudRate, RoboException

# Main function to orchestrate the execution
def main():
    global controller, handle, baud_rate_enum, node_id
    [test_nr, test_passes, test_fails] = [1,0,0]
    test_nr_2 = 0
    controller = RoboController()
    node_id = Pars.Node_ID_default
    valid_handles = list(controller.FindAllAdapters())
    if not valid_handles:
        raise Exception("No valid adapters found.")
    handle = valid_handles[0]
    baud_rate_enum = RoboControllerBaudRate.Baud_250K
    controller.Connect(handle, baud_rate_enum, 1)
    ###################################################################################################################################################
    #######################################################  DS402 Tests  #############################################################################
    [test_nr,test_passes,test_fails] = DS402_State_Machine_Transitions(controller,test_nr,test_passes,test_fails)
    [test_nr, test_passes, test_fails] = enable_ds402_and_test_modes(controller,test_nr,test_passes,test_fails)
    [test_nr, test_passes, test_fails] = supported_drive_modes(controller,test_nr,test_passes,test_fails)
    [test_nr, test_passes, test_fails] = DS402_version_nr(controller,test_nr,test_passes,test_fails)
    [test_nr, test_passes, test_fails] = No_mode_change_check(controller,test_nr,test_passes,test_fails)
    [test_nr, test_passes, test_fails] = DS402_CW_SW_Operations(controller,test_nr,test_passes,test_fails)
    control_word = 6
    result = check_bit_high(control_word, 1) and check_bit_high(control_word, 2)
    print(" CW is ", control_word," and result is ",result)

    ##################################################################################################################################################
    ######################################################  CANOpen Tests  ###########################################################################
   # change pdo , read tpdo, send rpdo functions
   #  [test_nr,test_passes,test_fails] = change_pdo_mapping(controller, "RPDO", 10,  536871428,test_nr,test_passes,test_fails)
    print_separator("Set RPDO Values Tests")
    for i in range(1, 9):
        for j in range(9 + (i - 1) * 2, 9 + (i - 1) * 2 + 2):
            [test_nr_2,rpdo_fails] = set_rpdo_value(controller, 1, 0x2005, j, random.randint(1, 999), i,test_nr)
    test_nr+=1
    if rpdo_fails !=0:
        [test_passes,test_fails] = print_test_result("Set RPDO Values Tests", False,test_nr,test_passes,test_fails)  # Update criteria as needed
    else:
        [test_passes,test_fails] = print_test_result("Set RPDO Values Tests", True,test_nr,test_passes,test_fails)  # Update criteria as needed
    print_separator("Read TPDO Values Tests")
    for i in range(1, 5):
        for j in range(2 * (i - 1) + 1, 2 * i + 1):
            [test_nr,tpdo_fails_1]= read_tpdo_value(controller, 1, j, i, j,test_nr)
   #
    for i in range(5, 9):
        for j in range(25 + (i - 5) * 2, min(33, 25 + (i - 5) * 2 + 2)):
            [test_nr_2,tpdo_fails_2] = read_tpdo_value(controller, 1, j, i, j,test_nr)
    test_nr+=1
    if tpdo_fails_1 !=0 or tpdo_fails_2 !=0:
        [test_passes,test_fails] = print_test_result("Read TPDO Values Tests", False,test_nr,test_passes,test_fails)  # Update criteria as needed
    else:
        [test_passes,test_fails] = print_test_result("Read TPDO Values Tests", True,test_nr,test_passes,test_fails)  # Update criteria as needed
    # Remove ESTOP to run the motor
    controller.SetCommand("MG", 0, 0)
    fw = controller.GetValueString("FID", 0)
    print(fw)
    version = extract_version(fw)  # version variable is used later for selecting the correct command
    reset_to_defaults_and_reconnect(controller,handle)
    # [test_nr,test_passes,test_fails] = apply_config_and_restart(controller,test_nr,Pars.t_wait_long,test_passes,test_fails,handle)
    # [test_nr,test_passes,test_fails] = calibration_retention(controller,test_nr,Pars.t_wait_long,test_passes,test_fails,handle)
   # # #
    [test_nr,test_passes,test_fails] = manage_heartbeat(controller,Pars.Heartbeat_test,test_nr,test_passes,test_fails)
    [test_nr,test_passes,test_fails] = try_baud_rates(controller,test_nr,Pars.Node_ID_default,test_passes,test_fails,handle)
    [test_nr,test_passes,test_fails] = change_node_id(controller, Pars.Node_ID_test,test_nr,test_passes,test_fails,handle)
    [test_nr,test_passes,test_fails] = change_node_id(controller,Pars.Node_ID_default,test_nr,test_passes,test_fails,handle)
    time.sleep(0.3)  # Wait a bit after the restart command
    reset_to_defaults_and_reconnect(controller,handle)
    ###################################################################################################################################################
    #######################################################  Misc Tests  ##############################################################################
    [test_nr,test_passes,test_fails] = lock_get_unlock(controller,test_nr,test_passes,test_fails)
   # controller_reboot(controller,handle)
    [test_nr,test_passes,test_fails] = test_overvoltage_protection(controller,test_nr,test_passes,test_fails)
    [test_nr,test_passes,test_fails] = test_undervoltage_protection(controller,test_nr,test_passes,test_fails)
    [test_nr,test_passes,test_fails] = test_overtemp_protection(controller,test_nr,test_passes,test_fails)
    [test_nr,test_passes,test_fails] = test_estop_protection(controller,test_nr,test_passes,test_fails)
   #  # # run_motor_and_switch_mode(controller,test_passes,test_fails)
   #  controller.SetMaintenanceString("swrit", 0, "hello")
   #  print("SREAD CHECK ",controller.GetMaintenanceString("SREAD", 1).replace("\r", "\n"))
    ###################################################################################################################################################
    #######################################################  Final Report  ############################################################################
    print("\n" + "=" * 30)
    print("FINAL REPORT")
    print("=" * 30)
    print(f"Total Passes: {test_passes}")
    print(f"Total Fails: {test_fails}")

    print("Total Tests Performed: ",test_nr-1)

if __name__ == "__main__":
    main()