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
# # Part 3 start: Standalone controller tests.
# # ----------------------------------------------------------------------------------------------------------------------
test_nr = 0
fail_counter = 0
# # ###----------------------------------------------------------------------------------------------------------------------'
# # # ## Test 50: %CLMOD 6 (ZSRM calibration).
test_nr = test_nr + 1
test_name = "Test 50: %CLMOD 6 (ZSRM calibration)."
test_abrv = "ZSRM"
ZSRM_orig = int(getconfig(ser,test_abrv))
setconfig(ser,test_abrv,-1)
setcommandmaint(ser,"clsav",Pars.key)
time.sleep(Pars.t_wait_long)
setcommandmaint(ser,"reset",Pars.key)
print("Controller has been reboot via %reset")
ser.close()
time.sleep(Pars.t_wait_long)
##------------------------------------------------------------------------------------------
try:
    ser = establish_serial_connection(Pars.COM_port_USB,Pars.COM_baudrate,Pars.COM_timeout)
    # Use serial_connection for further operations
except serial.SerialException as e:
    print(e)
setconfig(ser, "SED", 0, 0)
setcommand(ser, "MG", 1)
setcommandmaint(ser,"clmod",6)
time.sleep(Pars.t_wait_vlong)
ZSRM_final = int(getconfig(ser,test_abrv))
print("ZSRM_orig",ZSRM_orig,"ZSRM_final",ZSRM_final)
if ZSRM_final > Pars.ZSRM_min_threshold and ZSRM_final < Pars.ZSRM_max_threshold:
    print("Test " + str(test_nr) + " " + test_name + "." + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + "." + ": - Fail \n \n")
    #print("Raw_Redirect_Read_OK_1",Raw_Redirect_Read_OK_1,"Raw_Redirect_Read_OK_2",Raw_Redirect_Read_OK_2)
    fail_counter += 1
# # # # # ----------------------------------------------------------------------------------------------------------------------'
# # # # # ----------------------------------------------------------------------------------------------------------------------'
# # Finale
# # ------------------------------------------------------------------------------------------------------------------------'
test_end_time = time.time()
test_duration = test_end_time-test_start_time
print("Number of tests completed" ,test_nr,"Number of failed tests:",fail_counter, ". Test_duration was: ",test_duration," secs.")
ser.close()
time.sleep(Pars.t_wait_long)
