#Import packages
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
# # ----------------------------------------------------------------------------------------------------------------------
# # Part 2 start: Standalone controller tests.
# # ----------------------------------------------------------------------------------------------------------------------
test_nr = 0
fail_counter = 0
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
# # # ----------------------------------------------------------------------------------------------------------------------'
# ## Test 26: Safety Stop - !SFT and EDEC ramp check"
if Pars.FW_type != 2 :#"#works only for F3 !
    test_nr = test_nr + 1
    test_name = "Safety Stop via !sft - EDEC ramp check"
    test_abrv = "RMP"#compute ramp based on Power drop
    RWD_trigger = False
    DI_count = 3
    DINA_setting = 1 + 16 * Pars.kk
    #time.sleep(Pars.t_wait_long)
    sft_slope = compute_slope(ser,test_abrv,Pars.cc,DI_count,DINA_setting,RWD_trigger)
    print(sft_slope)
    sft_FM_trig = getvalue(ser,"FM", Pars.cc)
    sft_dict_trig = FM_read(sft_FM_trig)
    if sft_dict_trig["FM_Safestop"] and sft_slope > Pars.EDEC_ramp_min and sft_slope < Pars.EDEC_ramp_max:
        print("Test " + str(test_nr) + " " + test_name +"."+ str(DI_count)+": - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name +"."+ str(DI_count)+ ": - Fail \n \n")
        fail_counter += 1
    setconfig(ser,"DINA", DI_count,0)#restore digital input action
    setconfig(ser,"DINL", DI_count, 0)#restore  active level 0 --> DIN is low
    setcommand(ser,"G", Pars.cc, 0)#restore test motor command
# # ##----------------------------------------------------------------------------------------------------------------------'
# Test 27: Safety Stop - Dead Man Switch and EDEC ramp check"
if Pars.FW_type != 2 :#"#works only for F3 !
    test_nr = test_nr + 1
    test_name = "Safety Stop via Dead Man Switch - EDEC ramp check"
    test_abrv = "RMP"#compute ramp based on Power drop
    RWD_trigger = False
    DI_count = 3
    DINA_setting = 3 + 16 * Pars.kk #dead man switch
    sft_slope = compute_slope(ser,test_abrv,Pars.cc,DI_count,DINA_setting,RWD_trigger)
    print(sft_slope)
    sft_FM_trig = getvalue(ser,"FM", Pars.cc)
    sft_dict_trig = FM_read(sft_FM_trig)
    if sft_slope > Pars.EDEC_ramp_min and sft_slope < Pars.EDEC_ramp_max:
        print("Test " + str(test_nr) + " " + test_name +"."+ str(DI_count)+": - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name +"."+ str(DI_count)+ ": - Fail \n \n")
        fail_counter += 1
# ---------------------------------------------------------------------------------------------------------------------'
# Test 28 "Amps Trigger Actions - Safety Stop"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Safety Stop"
test_abrv = "SFT"#
FM_flag = "FM_Safestop"
ATGA_setting = 1 + 16 * Pars.kk
fail_counter = amps_trigger_test(ser,test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag,test_name)
# #----------------------------------------------------------------------------------------------------------------------'
# # Test 29 "Amps Trigger Actions - EM Stop"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - EM Stop"
test_abrv = "EMstop"#
FM_flag = "FM_FetsOff"
ATGA_setting = 2 + 16 * Pars.kk
fail_counter = amps_trigger_test(ser,test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag,test_name)
# #----------------------------------------------------------------------------------------------------------------------'
# # Test 30 "Amps Trigger Actions - Dead Man Stop"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Dead Man Stop"
test_abrv = "Dead"#
FM_flag = "FM_AmpTrig"
ATGA_setting = 3 + 16 * Pars.kk
fail_counter = amps_trigger_test(ser,test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag,test_name)
# #----------------------------------------------------------------------------------------------------------------------'
# # Test 31 "Amps Trigger Actions - FWD limit switch"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - FWD limit switch"
test_abrv = "FWD"#use this to trigger AmpsTrig
FM_flag = "FM_FwdLim"
ATGA_setting = 4 + 16 * Pars.kk
fail_counter = amps_trigger_test(ser,test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag,test_name)
# ##----------------------------------------------------------------------------------------------------------------------'
# # # Test 32 "Amps Trigger Actions - Rev limit switch"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Rev limit switch"
test_abrv = "REV"#use this to trigger AmpsTrig
FM_flag = "FM_RevLim"
ATGA_setting = 5 + 16 * Pars.kk
fail_counter = amps_trigger_test(ser,test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag,test_name)
# # ##----------------------------------------------------------------------------------------------------------------------'
# Test 33 "Amps Trigger Actions - Invert Direction"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Invert Direction"
test_abrv = "Inv"
FM_flag = "FM_AmpTrig"#not used here
ATGA_setting = 6 + 16 * Pars.kk
fail_counter = amps_trigger_test(ser,test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag,test_name)
# ##----------------------------------------------------------------------------------------------------------------------'
# Test 34 "Amps Trigger Actions - Run Script"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Run Script"
setcommandmaint(ser,"sld",Pars.key,":100000000201030E001F03E803230300002000FF8A:00000001FF")# script: wait forever
time.sleep(Pars.t_wait_mid)
setcommandmaint(ser,"sld",Pars.key,":100000000201030E001F03E803230300002000FF8A:00000001FF")# needed twice
time.sleep(Pars.t_wait_long)
test_abrv = "Script"
FM_flag = "FM_RevLim"#not used here
ATGA_setting = 7 + 16 * Pars.kk
fail_counter = amps_trigger_test(ser,test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag,test_name)
# # #----------------------------------------------------------------------------------------------------------------------'
# # Test 35 "Amps Trigger Actions - Load  Counter with Home Value"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Load  Counter with Home Value"
test_abrv = "Home"
FM_flag = "FM_AmpTrig"
ATGA_setting = 8 + 16 * Pars.kk
setconfig(ser,"BHOME",Pars.cc,Pars.home_count)
setconfig(ser,"SHOME",Pars.cc,Pars.home_count)
setconfig(ser,"EHOME",Pars.cc,Pars.home_count)
fail_counter = amps_trigger_test(ser,test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag,test_name)
# # # #----------------------------------------------------------------------------------------------------------------------'
## Test 36 "Telemetry" (combined with config retention)
test_nr = test_nr + 1
test_name = "Telemetry"
test_abrv = "TELS"
test_vars = "\"?A:?V:?T:# 200\""
setconfig(ser,"SCRO",1)#1 = serial
setconfig(ser,test_abrv,test_vars)
setcommandmaint(ser,"eesav")
time.sleep(Pars.t_wait_long)
setcommandmaint(ser,"reset",Pars.key)
print("Controller has been reboot via %reset")
ser.close()
time.sleep(Pars.t_wait_long)
ser.close()
time.sleep(Pars.t_wait_vlong)
#------------------------------------------------------------------------------------------
try:
    ser = establish_serial_connection(Pars.COM_port_serial,Pars.COM_baudrate,Pars.COM_timeout)
    # Use serial_connection for further operations
except serial.SerialException as e:
    print(e)
print(ser)
time.sleep(Pars.t_wait_vlong)
tels_counter = 1
tels_counts = 2
while tels_counter < tels_counts:
    RS_Stream = ser.readline()
    RS_String = RS_Stream.decode()
    tels_result = "Pass" if all(expr in RS_String for expr in ["A=", "T=", "V="]) else "Fail"
    print("ser is ",)
    print("test result is ",tels_result)
    tels_counter +=1
if tels_result == "Pass":
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter +=1
# setconfig(ser,"SCRO",1)#1 = serial
# setconfig(ser,test_abrv,0)#
# # # # # ----------------------------------------------------------------------------------------------------------------------'
# # Finale
# # ------------------------------------------------------------------------------------------------------------------------'
test_end_time = time.time()
test_duration = test_end_time-test_start_time
print("Number of tests completed" ,test_nr,"Number of failed tests:",fail_counter, ". Test_duration was: ",test_duration," secs.")
ser.close()
time.sleep(Pars.t_wait_long)
