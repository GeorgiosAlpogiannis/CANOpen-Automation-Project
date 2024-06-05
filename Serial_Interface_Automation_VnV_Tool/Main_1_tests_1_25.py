# Import packages
import serial
import time
import Pars
import Test_Functions
from Test_Functions import *
ser = Test_Functions.Test_Functions_Main()
# ----------------------------------------------------------------------------------------------------------------------
# Tests start
# ----------------------------------------------------------------------------------------------------------------------
test_start_time = time.time()
# Perform reset to defaults & Clear fault flags to begin

# Write Parameters defined in Pars
setconfig(ser,"RS", Pars.cc, Pars.Rs)# apply setting
setconfig(ser,"LD", Pars.cc, Pars.Ld)# apply setting
setconfig(ser,"LQ", Pars.cc, Pars.Lq)# apply setting
print(Pars.Rs,Pars.Ld,Pars.Lq)
print("ser is ",ser)
# # ----------------------------------------------------------------------------------------------------------------------
# # Part 1 start: Standalone controller tests.
# # ----------------------------------------------------------------------------------------------------------------------
test_nr = 0
fail_counter = 0
# ##----------------------------------------------------------------------------------------------------------------------
print("FAIL COUNTERRRR IS ",fail_counter)
# # # #  Test 1 Overheat: Verify Overheat and Fets OFF flags trigger when OTL limit is violated.
# test_nr = test_nr + 1
# test_name = "FF_Overheat"
# test_abrv = "OTL"
# counts = 3#3 different temp limits
# fail_counter = fault_flag_test(ser,test_name,test_abrv,counts,fail_counter, Pars.overheat_lim_test,test_nr)[0]
# print("FAIL COUNTER IS ",fail_counter)
# # # ----------------------------------------------------------------------------------------------------------------------
# # # # #  Test 2 Overvolt: Verify Overvolt and Fets OFF flags trigger when OVL limit is violated.
# test_nr = test_nr + 1
# test_name = "FF_Overvolt"
# test_abrv = "OVL"
# counts = 1#only 1 OVL limit
# fail_counter = fault_flag_test(ser,test_name,test_abrv,counts,fail_counter, Pars.overvolt_lim_test,test_nr)[0]
# # # # # ----------------------------------------------------------------------------------------------------------------------
# # # #  Test 3 Undervolt: Verify Undervolt and Fets OFF flags trigger when UVL limit is violated.
# test_nr = test_nr + 1
# test_name = "FF_Undervolt"
# test_abrv = "UVL"
# counts = 1#only 1 UVL limit
# fail_counter = fault_flag_test(ser,test_name,test_abrv,counts,fail_counter,Pars.undervolt_lim_test,test_nr)[0]
# # # # ----------------------------------------------------------------------------------------------------------------------
# # # # #  Test 4 Estop: Verify Estop & Fets OFF flags trigger when Estop is requested.
# test_nr = test_nr + 1
# test_name = "FF_Estop"
# test_abrv = "EX"
# counts = 1 #only 1 Estop limit
# fail_counter = fault_flag_test_no_config(ser,test_name,test_abrv,counts,fail_counter,test_nr)
# setcommand(ser,"MG",1)#clear Estop
# time.sleep(Pars.t_wait_long)
# # # # # ----------------------------------------------------------------------------------------------------------------------
# if Pars.motor_type != 3: ## N/A for Brushed DC
#     # # #  Test 5 SED error: Verify SED & Fets OFF flags trigger when SED conditions are violated(no sensor connected).
#     test_nr = test_nr + 1
#     test_name = "FF_SED"
#     test_abrv = "SED"
#     counts = 1 #2
#     fail_counter = fault_flag_test(ser,test_name,test_abrv,counts,fail_counter,Pars.sed_value_test,test_nr)[0]
# # # # ----------------------------------------------------------------------------------------------------------------------
# #  # Test 6 Mosfail error: Verify Mosfail flags trigger when Mosfail conditions are violated(using ZSRM).
# test_nr = test_nr + 1
# test_name = "FF_Mosfail"
# test_abrv = "ZSRM"
# counts = 1 #2
# fail_counter = calibration_test(ser,test_name,test_abrv,counts,fail_counter,Pars.ZSRM_value_test,test_nr)
# # # # ----------------------------------------------------------------------------------------------------------------------
# # # # ----------------------------------------------------------------------------------------------------------------------
# # # Test 7 Script run functionality: Test that script can be (re)started and stopped using !R ).
# test_nr = test_nr + 1
# test_name = "Script Start / Stop / Restart"
# # print("Perform reboot via %reset ")
# setconfig(ser,"SCRO",2)
# setcommandmaint(ser,"sld",Pars.key,":10000000240568656C6C6F0310272300FFFFFFFF5A:00000001FF")#
# time.sleep(Pars.t_wait_mid)
# setcommandmaint(ser,"sld",Pars.key,":10000000240568656C6C6F0310272300FFFFFFFF5A:00000001FF")# needed twice
# setcommand(ser,"R",1)# Start script.
# time.sleep(Pars.t_wait_long2)
# FS_active = getvalue(ser,"FS", 1)
# FS_dict_active = FS_read(FS_active)
# setcommand(ser,"R", 0)  # Stop script.
# time.sleep(Pars.t_wait_mid)
# FS_deact = getvalue(ser,"FS", 1)
# FS_dict_deact = FS_read(FS_deact)
# setcommand(ser,"R", 2)  # Restart script.
# time.sleep(Pars.t_wait_mid)
# FS_react = getvalue(ser,"FS", 1)
# FS_dict_react = FS_read(FS_react)
# if FS_dict_active["FS_RunScript"] and not FS_dict_deact["FS_RunScript"] and FS_dict_react["FS_RunScript"]:
#     print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
# else:
#     print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
#     print(FS_dict_active,FS_dict_deact,FS_dict_react)
#     print(FS_dict_active["FS_RunScript"],FS_dict_deact["FS_RunScript"],FS_dict_react["FS_RunScript"])
#     fail_counter += 1
# setcommand(ser,"R", 0)  # Stop script.
# # # # # # # # ----------------------------------------------------------------------------------------------------------------------
# # # Test 8 Script auto-start functionality: Reboot controller and verify script starts running automatically ).
# test_nr = test_nr + 1
# test_name = "Script Auto-Start"
# setcommand(ser,"R", 0)  # Stop script.
# time.sleep(Pars.t_wait_mid)
# FS_bef_reset = getvalue(ser,"FS", 1)
# FS_dict_bef_reset = FS_read(FS_bef_reset)
# setconfig(ser,"BRUN", 2)  # Enable immediate script-auto start.
# setcommandmaint(ser,"eesav") # save to controller
# print("Perform reboot via %reset ")
# setcommandmaint(ser,"reset",Pars.key)
# setcommandmaint(ser,"reset",Pars.key)
# print("Controller has been reboot via %reset")
# time.sleep(Pars.t_wait_mid)#long
# ser.close()
# time.sleep(Pars.t_wait_mid)#long
# try:
#     ser = establish_serial_connection(Pars.COM_port_USB,Pars.COM_baudrate,Pars.COM_timeout)
#     # Use serial_connection for further operations
# except serial.SerialException as e:
#     print(e)
# print(ser)
# # ser = Test_Functions.Test_Functions_Main()
# # print(ser.is_open)
# # Perform reset to defaults & Clear fault flags to begin
# if Pars.reset_defaults_flag == True:
#     print("Perform reset to defaults ")
#     setcommandmaint(ser,"eerst",Pars.key)
#     print("Controller has been reset to defaults")
#     time.sleep(Pars.t_wait_vlong)
# FS_aft_reset = getvalue(ser,"FS", 1)
# FS_dict_aft_reset = FS_read(FS_aft_reset)
# print(FS_dict_bef_reset)
# print(FS_dict_aft_reset)
# if not FS_dict_bef_reset["FS_RunScript"] and FS_dict_aft_reset["FS_RunScript"]:
#     print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
# else:
#     print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
#     fail_counter += 1
# setcommand(ser,"R", 0)  # Stop script.
# setconfig(ser,"BRUN", 0)  # Disable script-auto start.
# # # # # # # # ----------------------------------------------------------------------------------------------------------------------
# # # Test 9: Read / Write all boolean variables.
# test_nr = test_nr + 1
# test_name = "Boolean_Vars_Read_Write"
# test_abrv = "B"
# fail_counter = var_read_write(ser,test_abrv,test_name,test_nr,fail_counter)
# # # # ----------------------------------------------------------------------------------------------------------------------
# # # Test 10: Write all user variables .
# test_nr = test_nr + 1
# test_name = "User_Vars_Read_Write"
# test_abrv = "VAR"
# fail_counter = var_read_write(ser,test_abrv,test_name,test_nr,fail_counter)
# # # ----------------------------------------------------------------------------------------------------------------------
# # # DOUT tests
# # # ----------------------------------------------------------------------------------------------------------------------
Dout = getconfig(ser,"DOA")
DO_nr_calc = round(len(Dout) / 2)
DO_nr = Pars.DO_nr
DO_sum_tot = power_sum(DO_nr)
print("DO_nr",DO_nr,"DO_nr_calc",DO_nr_calc)
# ----------------------------------------------------------------------------------------------------------------------
## Test 11: Digital outputs - Set using !DS
test_nr = test_nr + 1
test_name = "Digital outputs control via !DS"
setcommand(ser,"DS",DO_sum_tot)# activate all DOUT's
time.sleep(Pars.t_wait_mid)#short
DO_act_check = int(getvalue(ser,"DO"))#
setcommand(ser,"DS",0)# de-activate all DOUT's
time.sleep(Pars.t_wait_mid)
DO_deact_check = int(getvalue(ser,"DO"))
print(DO_act_check)
print(DO_deact_check)
print(DO_sum_tot)
if DO_act_check == DO_sum_tot and DO_deact_check == 0:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter +=1
# # # # # # ----------------------------------------------------------------------------------------------------------------------
# # Test 12: Digital output actions- Motor is ON
test_nr = test_nr + 1
test_name = "Digital output actions Motor is ON"
test_abrv = "G"
test_setting = Pars.MC_test
dout_aa = 16*Pars.kk+1 # aa according to DOA syntax in user manual
fail_counter = dout_actions_test(ser,test_abrv,dout_aa,DO_nr,test_setting,DO_sum_tot,fail_counter,test_nr,test_name)
# ----------------------------------------------------------------------------------------------------------------------
# Test 13: Digital output actions- Motor is Reverse
test_nr = test_nr + 1
test_name = "Digital output actions Motor is Reverse"
test_abrv = "G"
test_setting = -Pars.MC_test
dout_aa = 16*Pars.kk+2 # aa according to DOA syntax in user manual
fail_counter = dout_actions_test(ser,test_abrv,dout_aa,DO_nr,test_setting,DO_sum_tot,fail_counter,test_nr,test_name)
# # ----------------------------------------------------------------------------------------------------------------------
# Test 14: Digital output actions - Overvoltage
test_nr = test_nr + 1
test_name = "Digital output actions - Overvoltage"
test_name_aux = "FF_Overvolt"
test_abrv = "OVL"
counts = 1#only 1 OVL limit
test_setting = Pars.overvolt_lim_test
dout_aa = 16*Pars.cc+3 # aa according to DOA syntax in user manual
setconfig(ser,"DOA", 0, dout_aa)  # configure DOUT action as OVL for DOUT's
DOA_OVL_result = fault_flag_test(ser,test_name_aux, test_abrv, counts, fail_counter, test_setting,test_nr)[1]
print(DOA_OVL_result)
if DOA_OVL_result == DO_sum_tot:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter += 1
print("fail_counter",fail_counter,"fail_counter type",type(fail_counter))
# # # ----------------------------------------------------------------------------------------------------------------------
# Test 15: Digital output actions - Overtemperature
test_nr = test_nr + 1
test_name = "Digital output actions - Overtemperature"
test_name_aux = "FF_Overheat"
test_abrv = "OTL"
counts = 1#only 1 OTL limit
test_setting = Pars.overheat_lim_test
dout_aa = 16*Pars.cc+4 # aa according to DOA syntax in user manual
setconfig(ser,"DOA", 0, dout_aa)  # configure DOUT action as OVL for DOUT's
DOA_OTL_result = fault_flag_test(ser,test_name_aux, test_abrv, counts, fail_counter, test_setting,test_nr)[1]
print(DOA_OTL_result)
if DOA_OTL_result == DO_sum_tot:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter += 1
# # # ----------------------------------------------------------------------------------------------------------------------
# Test 16: Digital output actions - Mirror Status LED
test_nr = test_nr + 1
test_name = "Digital output actions - Mirror Status LED"
dout_aa = 16*Pars.cc+5 # aa according to DOA syntax in user manual
setconfig(ser,"DOA", 0, dout_aa)  # configure DOUT action as OVL for DOUT's
time.sleep(Pars.t_wait_short)
LED_OFF_threshold = round(DO_sum_tot*Pars.LED_iters/3)
LED_ON_threshold = round((2*DO_sum_tot*Pars.LED_iters)/3)
LED_cnt = 0
LED_OFF_sum = 0
LED_ON_sum = 0
default_set = getconfig(ser,"OVL")
while LED_cnt < Pars.LED_iters:
    do_mirror_check_1 = int(getvalue(ser,"DO"))# DOUT LED should be mostly OFF
    LED_OFF_sum = LED_OFF_sum + do_mirror_check_1
    setconfig(ser,"OVL",Pars.overvolt_lim_test)# this will cause DOUT LED to be mostly ON
    time.sleep(Pars.t_wait_mid)
    do_mirror_check_2 = int(getvalue(ser,"DO"))
    LED_ON_sum = LED_ON_sum + do_mirror_check_2
    setconfig(ser,"OVL", default_set)  # restore setting to default
    time.sleep(Pars.t_wait_mid)
    LED_cnt += 1
print("LED_OFF_sum (OFF),",LED_OFF_sum,"LED_OFF_threshold (OFF)",LED_OFF_threshold,"LED_ON_sum (ON),",LED_ON_sum,"LED_ON_threshold (ON)",LED_ON_threshold,"DO_sum_tot",DO_sum_tot)
if LED_OFF_sum < LED_OFF_threshold and LED_ON_sum > LED_ON_threshold:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter += 1
print("fail_counter",fail_counter,"fail_counter type",type(fail_counter))
# ----------------------------------------------------------------------------------------------------------------------
# Test 17: Digital output actions - No Mosfail
test_nr = test_nr + 1
test_name = "Digital output actions - No Mosfail"
test_name_aux = "FF_Mosfail"
test_abrv = "ZSRM"
counts = 1#only 1 OTL limit
test_setting = Pars.ZSRM_value_test
dout_aa = 16*Pars.cc+6 # aa according to DOA syntax in user manual
setconfig(ser,"DOA", 0, dout_aa)  # configure DOUT action as OVL for DOUT's
time.sleep(Pars.t_wait_short)
No_mosfail_check_1 = int(getvalue(ser,"DO"))
No_mosfail_check_2 = calibration_test(ser,test_name_aux,test_abrv,counts,fail_counter,Pars.ZSRM_value_test,test_nr)
time.sleep(Pars.t_wait_short)
#print(No_mosfail_check_1,No_mosfail_check_2,DO_sum_tot)
if No_mosfail_check_1 == DO_sum_tot and No_mosfail_check_2 == 0:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter += 1
setconfig(ser,"DOA", 0, 0)  # restore DOUT's to No Action
time.sleep(Pars.t_wait_long)#neeeded
# # # # # # ----------------------------------------------------------------------------------------------------------------------
# # # # # # # DINA action tests
# # # # # ## ----------------------------------------------------------------------------------------------------------------------
# # # # # # Read Digital input number
Din_1 = getvalue(ser,"DI")
print("DIN 1 DONE")
Din_orig = len(Din_1)
Din_orig_2 = Din_orig/2
DI_nr_alt = round(len(Din_1) / 2) #check again
print("DI_nr_alt",DI_nr_alt,"Din_orig",Din_orig,"Din_1",len(Din_1))
DI_nr = Pars.DI_nr
# # # ## ----------------------------------------------------------------------------------------------------------------------
# # # Test 18: Digital input actions - Safety Stop
test_nr = test_nr + 1
test_name = "Digital input actions - Safety Stop"
DINA_setting = 1 + 16 * Pars.kk
flag_triggered = "FM_Safestop"
fail_counter = DINA_test(ser,DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count,test_nr,test_name)
## ----------------------------------------------------------------------------------------------------------------------
# # Test 19: Digital input actions - EM Stop
test_nr = test_nr + 1
test_name = "Digital input actions - EM Stop"
setcommand(ser,"MG", 1)
time.sleep(Pars.t_wait_mid)#neeeded
DINA_setting = 2 + 16 * Pars.kk
flag_triggered = "FM_FetsOff"
fail_counter = DINA_test(ser,DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count,test_nr,test_name)
# ## ----------------------------------------------------------------------------------------------------------------------
# #Test 20: Digital input actions - Dead Man Switch
test_nr = test_nr + 1
test_name = "Digital input actions - Dead Man Switch"
DINA_setting = 3 + 16 * Pars.kk
flag_triggered = "DEAD"
fail_counter = DINA_test(ser,DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count,test_nr,test_name)
# ## ----------------------------------------------------------------------------------------------------------------------
# #Test 21: Digital input actions - FWD limit Switch
test_nr = test_nr + 1
test_name = "Digital input actions - FWD limit Switch"
DINA_setting = 4 + 16 * Pars.kk
flag_triggered = "FM_FwdLim"
fail_counter = DINA_test(ser,DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count,test_nr,test_name)
# # ----------------------------------------------------------------------------------------------------------------------
# #Test 22: Digital input actions - REV limit Switch
test_nr = test_nr + 1
test_name = "Digital input actions - REV limit Switch"
DINA_setting = 5 + 16 * Pars.kk
flag_triggered = "FM_RevLim"
fail_counter = DINA_test(ser,DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count,test_nr,test_name)
# # ----------------------------------------------------------------------------------------------------------------------'
# # #Test 23: Digital input actions - Inverse direction
test_nr = test_nr + 1
test_name = "Digital input actions - Inverse direction"
DINA_setting = 6 + 16 * Pars.kk
flag_triggered = "INV"
fail_counter = DINA_test(ser,DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count,test_nr,test_name)
# ----------------------------------------------------------------------------------------------------------------------
# #Test 24: Digital input actions - Run Microbasic script
time.sleep(Pars.t_wait_long)## DEBUG
setcommandmaint(ser,"sld",Pars.key,":10000000240568656C6C6F0310272300FFFFFFFF5A:00000001FF")#
time.sleep(Pars.t_wait_mid)
setcommandmaint(ser,"sld",Pars.key,":10000000240568656C6C6F0310272300FFFFFFFF5A:00000001FF")# needed twice
test_nr = test_nr + 1
test_name = "Digital input actions - Run Microbasic script"
DINA_setting = 7 + 16 * Pars.kk
flag_triggered = "FS_RunScript"
fail_counter = DINA_test(ser,DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count,test_nr,test_name)
# # # ----------------------------------------------------------------------------------------------------------------------
#Test 25: Digital input actions - Load  Counter with Home Value
test_nr = test_nr + 1
test_name = "Digital input actions - Load  Counter with Home Value"
DINA_setting = 8 + 16 * Pars.kk
flag_triggered = "HOME"
setconfig(ser,"BHOME",Pars.cc,Pars.home_count)
setconfig(ser,"SHOME",Pars.cc,Pars.home_count)
setconfig(ser,"EHOME",Pars.cc,Pars.home_count)
fail_counter = DINA_test(ser,DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count,test_nr,test_name)
# # # # # ----------------------------------------------------------------------------------------------------------------------'
# # Finale
# # ------------------------------------------------------------------------------------------------------------------------'
test_end_time = time.time()
test_duration = test_end_time-test_start_time
print("Number of tests completed" ,test_nr,"Number of failed tests:",fail_counter, ". Test_duration was: ",test_duration," secs.")
ser.close()
time.sleep(Pars.t_wait_long)
