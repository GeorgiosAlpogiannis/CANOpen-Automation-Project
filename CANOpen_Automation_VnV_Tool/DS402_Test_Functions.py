import Pars
import Main
from Main import *
def DS402_State_Machine_Transitions(controller,test_nr,test_passes,test_fails):
    fail_counter = 0
    print_separator("DS402 State Machine Transitions")
    print("\nEnabling DS402 with FSA and testing modes of operation...")
    # Test Fault State Transition and Clearance. (SW bit 3)
    controller.SetConfig("SED", Pars.cc, 2)#Trigger Fault State transition
    controller.SetCommand("MG", 0, 0)
    controller.SetConfig("FSA", 0, 1) # enable DS402
    time.sleep(Pars.t_wait_mid)
    status_word = controller.GetValue("SW", Pars.cc)
    fault_active_before = check_bit_high(status_word, 3)#fault bit should be active
    controller.SetConfig("SED", Pars.cc, 0)
    controller.SetConfig("SED", Pars.cc+1, 0)
    controller.SetCommand("MG", 0, 0)
    controller.SetCommand("CW", Pars.cc,0)
    controller.SetCommand("CW", Pars.cc, 128)
    status_word = controller.GetValue("SW", Pars.cc)
    fault_active_after = check_bit_high(status_word, 3)#fault bit should be cleared
    if fault_active_before and not fault_active_after:
        print("Fault Clearance applied successfully .")
    else:
        print("Fault Clearance Not applied successfully .")
        fail_counter+=1
    # Test State Transition from "Switch ON Disabled" to "Ready To Switch ON" and back. (Transitions 2,7,10)
    controller.SetCommand("CW", Pars.cc,0)
    status_word = controller.GetValue("SW", Pars.cc)
    Swich_ON_disabled_Status = check_bit_high(status_word, 4) and check_bit_high(status_word, 6) and not (check_bit_high(status_word, 0) or check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    controller.SetCommand("CW", Pars.cc,6)# Transition to "Ready To Switch ON
    status_word = controller.GetValue("SW", Pars.cc)
    Ready_To_Switch_ON_Status = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and not (check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    controller.SetCommand("CW", Pars.cc, 0)  # Transition back to "Switch ON Disabled"
    status_word = controller.GetValue("SW", Pars.cc)
    Swich_ON_disabled_Status_fin = check_bit_high(status_word, 4) and check_bit_high(status_word, 6) and not (check_bit_high(status_word, 0) or check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    if Swich_ON_disabled_Status and Ready_To_Switch_ON_Status and Swich_ON_disabled_Status_fin:
        print("Transition from 'Switch ON Disabled' to 'Ready To Switch ON' [transitions 2,7,10] completed successfully.")
    else:
        print("Transition from 'Switch ON Disabled' to 'Ready To Switch ON' [transitions 2,7,10] NOT completed successfully.")
        fail_counter+=1
    # Test State Transition from "Ready To Switch ON" to "Switched ON" and back. (Transitions 3,6,10)
    controller.SetCommand("CW", Pars.cc,6)
    status_word = controller.GetValue("SW", Pars.cc)
    Ready_To_Switch_ON_Status = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and not (check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    controller.SetCommand("CW", Pars.cc,7)# Transition to "Switched ON
    status_word = controller.GetValue("SW", Pars.cc)
    Switched_ON_Status = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and (check_bit_high(status_word, 1) and not check_bit_high(status_word, 2))
    controller.SetCommand("CW", Pars.cc, 0)  # Transition back to "Switch ON Disabled"
    status_word = controller.GetValue("SW", Pars.cc)
    Swich_ON_disabled_Status_fin = check_bit_high(status_word, 4) and check_bit_high(status_word, 6) and not (check_bit_high(status_word, 0) or check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    controller.SetCommand("CW", Pars.cc,6)# Transition to "Ready To Switch ON"
    controller.SetCommand("CW", Pars.cc,7)# Transition to "Switched ON
    status_word = controller.GetValue("SW", Pars.cc)
    Switched_ON_Status_fin = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and (check_bit_high(status_word, 1) and not check_bit_high(status_word, 2))
    controller.SetCommand("CW", Pars.cc,6)# Transition back to "Ready To Switch ON"
    status_word = controller.GetValue("SW", Pars.cc)
    Ready_To_Switch_ON_Status_fin = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and not (check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    if Switched_ON_Status and Ready_To_Switch_ON_Status and Ready_To_Switch_ON_Status_fin and Swich_ON_disabled_Status_fin and Switched_ON_Status_fin:
        print("Transition from 'Ready To Switch ON' to 'Switched ON' [transitions 3,6,10] completed successfully.")
    else:
        print("Transition from 'Ready To Switch ON' to 'Switched ON' [transitions 3,6,10]  NOT completed successfully.")
        fail_counter+=1
    # Test State Transition from "Switched ON" to "Operation Enabled" and back . (Transitions 4,5,8,9)
    controller.SetCommand("CW", Pars.cc,6)
    controller.SetCommand("CW", Pars.cc,7)
    controller.SetCommand("CW", Pars.cc,15)
    status_word = controller.GetValue("SW", Pars.cc)# transition 4
    Operation_ON_Status = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and (check_bit_high(status_word, 1) and check_bit_high(status_word, 2))
    controller.SetCommand("CW", Pars.cc,7)# transition 5
    status_word = controller.GetValue("SW", Pars.cc)
    Switched_ON_Status = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and (check_bit_high(status_word, 1) and not check_bit_high(status_word, 2))
    controller.SetCommand("CW", Pars.cc,15)
    controller.SetCommand("CW", Pars.cc,6)#transition 8
    status_word = controller.GetValue("SW", Pars.cc)
    Ready_To_Switch_ON_Status = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and not (check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    controller.SetCommand("CW", Pars.cc,15)
    controller.SetCommand("CW", Pars.cc,0)#transition 9
    status_word = controller.GetValue("SW", Pars.cc)
    Swich_ON_disabled_Status = check_bit_high(status_word, 4) and check_bit_high(status_word, 6) and not (check_bit_high(status_word, 0) or check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    if Operation_ON_Status and Switched_ON_Status and Ready_To_Switch_ON_Status and Swich_ON_disabled_Status:
        print("Transition from 'Switched ON' to 'Operation Enabled' [transitions 4,5,8,9] completed successfully.")
    else:
        print("Transition from 'Switched ON' to 'Operation Enabled' [transitions 4,5,8,9] NOT completed successfully.")
        fail_counter+=1
    # Test State Transition from "Operation Enabled" to Quick Stop and back . Transitions (11, 12). Transition 16 is N/A for Roboteq.
    controller.SetCommand("CW", Pars.cc,6)
    controller.SetCommand("CW", Pars.cc,7)
    controller.SetCommand("CW", Pars.cc,15)
    status_word = controller.GetValue("SW", Pars.cc)
    Operation_ON_Status = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and (check_bit_high(status_word, 1) and check_bit_high(status_word, 2))
    controller.SetCommand("CW", Pars.cc,2)
    status_word = controller.GetValue("SW", Pars.cc)# transition 11
    Quick_Stop_Status = check_bit_high(status_word, 0) and check_bit_high(status_word, 1) and check_bit_high(status_word, 2) and check_bit_high(status_word, 4) and not check_bit_high(status_word, 5)
    controller.SetCommand("CW", Pars.cc,0)
    status_word = controller.GetValue("SW", Pars.cc)# transition 12
    Swich_ON_disabled_Status = check_bit_high(status_word, 4) and check_bit_high(status_word, 6) and not (check_bit_high(status_word, 0) or check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    if Operation_ON_Status and Quick_Stop_Status and Swich_ON_disabled_Status:
        print("Transition from 'Operation Enabled' to 'Quick Stop' [transitions 11,12] completed successfully.")
    else:
        print("Transition from 'Operation Enabled' to 'Quick Stop' [transitions 11,12] NOT completed successfully.")
        print("Operation_ON_Status",Operation_ON_Status,"Quick_Stop_Status",Quick_Stop_Status,"Swich_ON_disabled_Status",Swich_ON_disabled_Status)
        fail_counter+=1
    if fail_counter >0:
        [test_passes,test_fails] = print_test_result("DS402 State Transition Tests", False,test_nr,test_passes,test_fails)
        print("test_passes",test_passes,"test_fails",test_fails)
    else:
        [test_passes,test_fails]  = print_test_result("DS402 State Transition Tests", True,test_nr,test_passes,test_fails)
        print("test_passes",test_passes,"test_fails",test_fails)
    # Check if the bit at the specified position is high
    test_nr += 1
    controller.SetConfig("FSA", 0, 0) # enable DS402
    return(test_nr,test_passes,test_fails)

def enable_ds402_and_test_modes(controller,test_nr,test_passes,test_fails):
    print_separator("DS402 Modes Of Operations Test")
    print("\nEnabling DS402 with FSA and testing modes of operation...")

    # Enable DS402
    controller.SetConfig("FSA", 0, 1)
    fsa_status = controller.GetConfig("FSA", 0)
    if fsa_status == 1:
        print("DS402 successfully enabled.")
    else:
        print("Failed to enable DS402.")
        print_test_result("DS402 Modes Of Operations", False,test_nr,test_passes,test_fails)
        return

    mode_explanations = {
        0: "No Mode - Open Loop Mode",
        1: "Profile Position Mode - Closed Loop Count Position Mode",
        2: "Velocity Mode - Closed Loop Speed Mode",
        3: "Profile Velocity Mode - Closed Loop Speed Mode",
        4: "Torque Profile Mode - Closed Loop Torque Mode",
        6: "Homing Mode - Closed Loop Speed Mode",
        8: "Cyclic Synchronous Position Mode - Closed Loop Count Position Mode",
        9: "Cyclic Synchronous Velocity Mode - Closed Loop Speed Mode",
        10: "Cyclic Synchronous Torque Mode - Closed Loop Torque Mode"
    }
    modes_of_operation = [x for x in range(11) if x not in (5, 7)]
    # print("mode_explanations[1]",mode_explanations[1])
    for mode in modes_of_operation:
        # Set the mode of operation
        controller.SetCommand("ROM", 1, mode)
        # Read the mode of operation for validation
        actual_mode = controller.GetValue("AOM", 1)
        if actual_mode == mode:
            print(f"Mode {mode}: {mode_explanations[mode]} successfully set and validated.")
        else:
            print(f"Failed to set Mode {mode}: {mode_explanations[mode]}.")
            [test_passes,test_fails] = print_test_result("DS402 Modes Of Operations", False,test_nr,test_passes,test_fails)  # Update criteria as needed
            return

    [test_passes,test_fails] = print_test_result("DS402 Modes Of Operations", True,test_nr,test_passes,test_fails)  # Update criteria as needed
    test_nr +=1
    return(test_nr,test_passes,test_fails)

def supported_drive_modes(controller,test_nr,test_passes,test_fails):
    print_separator("DS402 Supported Drive Modes Test")
    print("\nEnabling DS402 with FSA and testing modes of operation...")

    # Enable DS402
    controller.SetConfig("FSA", 0, 1)
    SDM = controller.GetValue("SDM", 0)
    if SDM == Pars.DS402_SDM:
        [test_passes, test_fails] = print_test_result("DS402 supported_drive_modes ", True, test_nr, test_passes,test_fails)  # Update criteria as needed
    else:
        [test_passes, test_fails] = print_test_result("DS402 supported_drive_modes ", False, test_nr, test_passes,test_fails)  # Update criteria as needed'
        print("SDM actual is",SDM," SDM expected is",Pars.DS402_SDM)
    test_nr +=1
    return(test_nr,test_passes,test_fails)

def DS402_version_nr(controller,test_nr,test_passes,test_fails):
    print_separator("DS402 Version Nr Test")
    print("\nEnabling DS402 with FSA and testing modes of operation...")

    # Enable DS402
    controller.SetConfig("FSA", 0, 1)
    VNM = controller.GetValue("VNM", 0)
    if VNM == Pars.DS402_VNM:
        [test_passes, test_fails] = print_test_result("DS402 DS402 version nr", True, test_nr, test_passes,test_fails)  # Update criteria as needed
    else:
        [test_passes, test_fails] = print_test_result("DS402 DS402 version nr", False, test_nr, test_passes,test_fails)  # Update criteria as needed'
        print("VNM actual is",VNM," VNM expected is",Pars.DS402_VNM)
    test_nr +=1
    return(test_nr,test_passes,test_fails)

def No_mode_change_check(controller,test_nr,test_passes,test_fails):
    print_separator("DS402 No Mode change test (ROM = 0)")
    print("\nEnabling DS402 with FSA and testing modes of operation...")
    # Enable DS402
    controller.SetConfig("FSA", 0, 1)
    controller.SetCommand("ROM", 1, Pars.ROM_mode_test)# go to Profile Velocity mode
    # Read the mode of operation for validation
    actual_mode = controller.GetValue("AOM", 1)
    controller.SetCommand("ROM", 1, 0)# No mode change, should remain in Profile Velocity mode
    actual_mode_fin = controller.GetValue("AOM", 1)
    if actual_mode == Pars.ROM_mode_test == actual_mode_fin:
        [test_passes, test_fails] = print_test_result("DS402 No Mode change test (ROM = 0)", True, test_nr, test_passes,test_fails)  # Update criteria as needed
    else:
        [test_passes, test_fails] = print_test_result("DS402 No Mode change test (ROM = 0)", False, test_nr, test_passes,test_fails)  # Update criteria as needed'
        print("AOM is",actual_mode," AOM expected is",Pars.ROM_mode_test)
    test_nr +=1
    return(test_nr,test_passes,test_fails)

def DS402_CW_SW_Operations(controller,test_nr,test_passes,test_fails):
    fail_counter = 0
    test_name = "DS402 Control / Status Word Operations Test"
    print_separator(test_name)
    print("\nEnabling DS402 with FSA and testing modes of operation...")
    # Clear faults
    controller.SetConfig("SED", Pars.cc, 0)
    controller.SetConfig("SED", Pars.cc+1, 0)
    controller.SetCommand("MG", 0, 0)
    controller.SetCommand("CW", Pars.cc,0)
    controller.SetCommand("CW", Pars.cc, 128)
    controller.SetCommand("CW", Pars.cc,0)
    # CW_0_5_&_8_13_&_16_SW = check_bit_high(status_word, 6) and not (check_bit_high(status_word, 0) or check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    # CW_6_&_14_SW = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and not (check_bit_high(status_word, 6) or check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
    # CW_7_SW = check_bit_high(status_word, 1) and check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and not (check_bit_high(status_word, 6) or check_bit_high(status_word, 2))
    # CW_15_SW = check_bit_high(status_word, 1) and check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and not (check_bit_high(status_word, 6) or check_bit_high(status_word, 2))
    CW_value = 0
    while CW_value <= Pars.CW_max_value:
        controller.SetCommand("CW", Pars.cc,CW_value)
        time.sleep(Pars.t_wait_short)
        control_word= controller.GetValue("CW", Pars.cc)
        CW_Ready_to_switch_ON = check_bit_high(control_word, 1) and check_bit_high(control_word, 2) and not(check_bit_high(control_word,0) or check_bit_high(control_word,4))
        CW_switch_ON_disabled = not check_bit_high(control_word, 1) or not check_bit_high(control_word, 2)
        CW_switched_ON = check_bit_high(control_word,0)  and check_bit_high(control_word, 1) and check_bit_high(control_word, 2) and not(check_bit_high(control_word,3))
        CW_operation_ON = check_bit_high(control_word,0)  and check_bit_high(control_word, 1) and check_bit_high(control_word, 2) and check_bit_high(control_word,3)

        if CW_Ready_to_switch_ON:
            status_word = controller.GetValue("SW", Pars.cc)
            SW_Ready_to_switch_ON = check_bit_high(status_word, 0) and check_bit_high(status_word,4) and check_bit_high(status_word,5) and not (check_bit_high(status_word, 6) or check_bit_high(status_word, 1) or check_bit_high(status_word,                                                                                           2))
            print("Ready to Switch ON State:control_word",control_word,"status_word",status_word)
            if SW_Ready_to_switch_ON:
                 time.sleep(Pars.t_wait_vshort)
            else:
                print("Fail CW_Ready_to_switch_ON",CW_Ready_to_switch_ON,"SW_Ready_to_switch_ON",SW_Ready_to_switch_ON," while both of them should be TRUE, status word is ",status_word," and CW is ",control_word)
                fail_counter+=1
        if CW_switch_ON_disabled:
            status_word = controller.GetValue("SW", Pars.cc)
            SW_switch_ON_disabled = check_bit_high(status_word, 4) and check_bit_high(status_word, 6) and not (check_bit_high(status_word, 0) or check_bit_high(status_word, 1) or check_bit_high(status_word, 2))
            print("Switch ON disabled State: control_word",control_word,"status_word",status_word)
            if SW_switch_ON_disabled:
                 time.sleep(Pars.t_wait_vshort)
            else:
                print("Fail CW_switch_ON_disabled",CW_switch_ON_disabled,"SW_switch_ON_disabled",SW_switch_ON_disabled," while both of them should be TRUE, status word is ",status_word," and CW is ",control_word)
                fail_counter+=1
        if CW_switched_ON:
            status_word = controller.GetValue("SW", Pars.cc)
            SW_switched_ON = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and (check_bit_high(status_word, 1) and not(check_bit_high(status_word, 6) or check_bit_high(status_word, 2)))
            print("Switched ON State: control_word",control_word,"status_word",status_word)
            if SW_switched_ON:
                 time.sleep(Pars.t_wait_vshort)
            else:
                print("Fail CW_switched_ON",CW_switched_ON,"SW_switched_ON",SW_switched_ON," while both of them should be TRUE, status word is ",status_word," and CW is ",control_word)
                fail_counter+=1
        if CW_operation_ON:
            status_word = controller.GetValue("SW", Pars.cc)
            SW_operation_ON = check_bit_high(status_word, 0) and check_bit_high(status_word, 4) and check_bit_high(status_word, 5) and (check_bit_high(status_word, 1) and check_bit_high(status_word, 2))
            print("Operation ON State: control_word",control_word,"status_word",status_word)
            if SW_operation_ON:
                 time.sleep(Pars.t_wait_vshort)
            else:
                print("Fail CW_operation_ON",CW_operation_ON,"SW_operation_ON",SW_operation_ON," while both of them should be TRUE, status word is ",status_word," and CW is ",control_word)
                fail_counter+=1
        # print("CW values is",CW_value," and fail counter is ",fail_counter)
        CW_value+=1
    if fail_counter ==0:
        [test_passes, test_fails] = print_test_result(test_name, True, test_nr, test_passes, test_fails)
    else:
        [test_passes, test_fails] = print_test_result(test_name, False, test_nr, test_passes, test_fails)
    test_nr += 1
    return (test_nr, test_passes, test_fails)
