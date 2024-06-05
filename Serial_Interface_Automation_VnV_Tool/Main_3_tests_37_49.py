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
# # #----------------------------------------------------------------------------------------------------------------------'
# ## Tests 37,38,39,40 "Retention of Configuration (EESAV) , Calibration  (CLSAV), BackUp Registers(BEE) & Time (TM) after %Reset"
test_nr = test_nr + 1
test_name = "Retention of Configuration (EESAV) , Calibration  (CLSAV) "
Config_check_default = getconfig(ser,Pars.Config_Retention_Object)#get initial setting.
Calib_check_default = getconfig(ser,Pars.Calib_Retention_Object, 1)
Backup_Reg_check_default = getconfig(ser,Pars.Backup_Register_Object, 1)
Backup_Time_check_default = getvalue(ser,Pars.Backup_Time_Object)
setconfig(ser,Pars.Config_Retention_Object,Pars.Config_retention_check)
setconfig(ser,Pars.Calib_Retention_Object,1,Pars.Calib_retention_check)
setconfig(ser,Pars.Backup_Register_Object,1,Pars.Backup_Register_check)
setcommandmaint(ser,"STIME",3,16)#set time
setcommandmaint(ser,"STIME",4,7)
setcommandmaint(ser,"STIME",5,2023)
time.sleep(Pars.t_wait_mid)
Config_check_before_reset = getconfig(ser,Pars.Config_Retention_Object)#get initial setting.
Calib_check_before_reset = getconfig(ser,Pars.Calib_Retention_Object,1)#get initial setting.
Backup_Reg_check_before_reset = getconfig(ser,Pars.Backup_Register_Object, 1)
Backup_Reg_time_before_reset = getvalue(ser,Pars.Backup_Time_Object)
setcommandmaint(ser,"EESAV")
setcommandmaint(ser,"CLSAV",Pars.key)
time.sleep(Pars.t_wait_long)
setcommandmaint(ser,"reset",Pars.key)
print("Controller has been reboot via %reset")
ser.close()
time.sleep(Pars.t_wait_long)
#------------------------------------------------------------------------------------------
try:
    ser = establish_serial_connection(Pars.COM_port_USB,Pars.COM_baudrate,Pars.COM_timeout)
    # Use serial_connection for further operations
except serial.SerialException as e:
    print(e)
print(ser)
# print(ser.is_open)
Config_check_after_reset = getconfig(ser,Pars.Config_Retention_Object)#get final setting.
Calib_check_after_reset = getconfig(ser,Pars.Calib_Retention_Object, 1)
Backup_Reg_check_after_reset = getconfig(ser,Pars.Backup_Register_Object, 1)
Backup_Reg_time_after_reset = getvalue(ser,Pars.Backup_Time_Object)
print("Config_check_after_reset",Config_check_after_reset,"Config_check_before_reset",Config_check_before_reset)
print("Calib_check_after_reset",Calib_check_after_reset,"Calib_check_before_reset",Calib_check_before_reset)
print("Backup_Reg_check_after_reset",Backup_Reg_check_after_reset,"Backup_Reg_check_before_reset",Backup_Reg_check_before_reset)
print("Backup_Reg_time_after_reset",Backup_Reg_time_after_reset,"Backup_Reg_time_before_reset",Backup_Reg_time_before_reset)
if (Config_check_after_reset == Config_check_before_reset) and (Calib_check_after_reset == Calib_check_before_reset):
    print("Tests " + str(test_nr) + ","+ str(test_nr+1) + " " + test_name + ": - Pass \n \n")
elif (Config_check_after_reset == Config_check_before_reset):
    print("Test " + str(test_nr+1) + " " + test_name + ": %CLSAV - Fail \n \n")
    fail_counter +=1
else:
    print("Test " + str(test_nr) + " " + test_name + ": %EESAV - Fail \n \n")
    fail_counter += 1
if Pars.Battery_included:
    test_name = "Retention of BackUp Registers(BEE) and Time (TM) after %Reset"
    if (Backup_Reg_check_after_reset==Backup_Reg_check_before_reset):
        test_nr += 2
        print("Test " + str(test_nr) + " " + test_name + ": ~BEE - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name + ": ~BEE - Fail \n \n")
        fail_counter+=1
    test_nr += 1
    if (Backup_Reg_time_after_reset==Backup_Reg_time_before_reset) and (Backup_Reg_time_after_reset != Backup_Time_check_default):
        print("Test " + str(test_nr) + " " + test_name + ": ?TM - Pass \n \n")
    elif (Backup_Reg_time_after_reset==Backup_Reg_time_before_reset):
        print("Test " + str(test_nr) + " " + test_name + ": %STIME - Fail \n \n")
        fail_counter+=1
    else:
        print("Test " + str(test_nr ) + " " + test_name + ": ?TM - Fail \n \n")
        fail_counter+=1
setconfig(ser,Pars.Config_Retention_Object,Config_check_default)# restore default setting.
setconfig(ser,Pars.Calib_Retention_Object,1,Calib_check_default)# restore default setting.
ser.flushInput() # clear data
time.sleep(Pars.t_wait_short)
# # #----------------------------------------------------------------------------------------------------------------------'
## Test 41 Query ?UID & Verify Response: MCU type and Device ID according to Script Settings. Unique ID has correct length and is Non-Zero"
test_nr = test_nr + 1
test_name = "Query ?UID & Verify Response"
UID_MCU_type = int(getvalue(ser,"UID",1))
UID_MCU_device_ID = int(getvalue(ser,"UID",2))
UID_MCU_unique_ID_pt1 = getvalue(ser,"UID",3)
UID_MCU_unique_ID_pt2 = getvalue(ser,"UID",4)
UID_MCU_unique_ID_pt3 = getvalue(ser,"UID",5)
UID_unique_ID_is_valid= False
if len(UID_MCU_unique_ID_pt1) == Pars.UID_Unique_ID_pt1 and len(UID_MCU_unique_ID_pt2) == Pars.UID_Unique_ID_pt2 and len(UID_MCU_unique_ID_pt3) == Pars.UID_Unique_ID_pt3:
    if int(UID_MCU_unique_ID_pt1) != 0 and int(UID_MCU_unique_ID_pt2) != 0 and int(UID_MCU_unique_ID_pt3) != 0:
        UID_unique_ID_is_valid = True
if (UID_MCU_device_ID == Pars.UID_MCU_device_ID) and (UID_MCU_type == Pars.UID_MCU_type) and UID_unique_ID_is_valid:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter+=1
# # #----------------------------------------------------------------------------------------------------------------------'
## Test 42 Query ?TRN & Verify Response: Controller type, Controller Model are matching, and according to Script Settings"
test_nr = test_nr + 1
test_name = "Query ?TRN & Verify Response"
TRN_init = getvalue(ser,"TRN")
TRN_check = TRN_init.split(":")
TRN_pt1 = (TRN_check[0])[:Pars.Controller_Characters]
TRN_pt2 = (TRN_check[1])[:Pars.Controller_Characters]
print("TRN_pt1",TRN_pt1,"TRN_pt2",TRN_pt2)
print("TRN_init",TRN_init,"TRN_check",TRN_check)
if TRN_check[0] == Pars.Controller_Type and TRN_pt1 == TRN_pt2:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter+=1
# # # #----------------------------------------------------------------------------------------------------------------------'
## Test 43 Query ?FID / ?FIN & Verify Response: Verify Controller Type, FW version and FW date are matching & according to Script Settings"
test_nr = test_nr + 1
test_name = "Query ?FID / ?FIN & Verify Response"
FID_init = getvalue(ser,"FID")
FIN_init_pt1 = getvalue(ser,"FIN",2)
FIN_init_pt2 = getvalue(ser,"FIN",3)
FIN_init_pt3 = getvalue(ser,"FIN",4)
Date_valid = False
if FIN_init_pt1 in FID_init and FIN_init_pt2 in FID_init and FIN_init_pt3 in FID_init and Pars.FID_date in FID_init:
    Date_valid = True
print("FID_init",FID_init,"FIN_init ",FIN_init_pt1,FIN_init_pt2,FIN_init_pt3),
if Pars.Controller_Type in FID_init and Pars.FID_fw_version in FID_init and Date_valid:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter+=1
# # #----------------------------------------------------------------------------------------------------------------------'
## Test 44 Serial Watchdog - Verify MC drops with specified EDEC Ramp, and Serial Bit drops, after Watchdog expires.
test_nr = test_nr + 1
test_name = "Serial Watchdog - Verify MC drops with specified EDEC Ramp, and Serial Bit drops, after Watchdog expires."
test_abrv = "RMP"#compute ramp based on Power drop
RWD_trigger = True
DI_count = 3
DINA_setting = 16 * Pars.kk # Not used.
sft_slope = compute_slope(ser,test_abrv,Pars.cc,DI_count,DINA_setting,RWD_trigger)
print("RWD slope", sft_slope)
sft_FS_trig = getvalue(ser,"FS", 1)
sft_dict_trig = FS_read(sft_FS_trig)
if Pars.FW_type != 2: #only F3 applicable.
    Ramp_Ok = sft_slope > Pars.EDEC_ramp_min and sft_slope < Pars.EDEC_ramp_max
else: #G4
    Ramp_Ok = True
if sft_dict_trig["FS_Serial"] == False and Ramp_Ok:
    print("Test " + str(test_nr) + " " + test_name +"."+": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name +"."+ ": - Fail \n \n")
    fail_counter += 1
##----------------------------------------------------------------------------------------------------------------------'
## Test 45 Serial Echo - Verify ECHO is enabled / disabled successfully.
test_nr = test_nr + 1
test_name = "Serial Echo - Verify ECHO is enabled / disabled successfully"
test_abrv = "RMP"#compute ramp based on Power drop
start_time = time.time()
echo_count = 0
echo_reply_full = [0,0]
while echo_count < 2:
    setconfig(ser,"ECHOF",echo_count)# 0 --> echo enabled, 1 --> echo disabled
    ser.write(Pars.echo_cmd.encode())
    start_time = time.time()
    reply_full = b""
    # Wait for a response with a timeout
    while (time.time() - start_time) < Pars.response_timeout:
        if ser.in_waiting > 0:
            reply_full = ser.readline()
            break
    echo_reply_full[echo_count] = reply_full
    echo_count +=1
print("echo_reply_full[0]",echo_reply_full[0],"echo_reply_full[1]",echo_reply_full[1])
if Pars.echo_cmd in echo_reply_full[0].decode() and Pars.echo_cmd not in echo_reply_full[1].decode():
    print("Test " + str(test_nr) + " " + test_name +"."+": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name +"."+ ": - Fail \n \n")
    fail_counter += 1
##----------------------------------------------------------------------------------------------------------------------'
## Test 46 Internal Serial Command- Query ?CIS & Verify response.
test_nr = test_nr + 1
test_name = "Internal Serial Command- Query ?CIS & Verify response"
setconfig(ser,"RWD",0)
setcommand(ser,"G",Pars.cc,Pars.MC_test)
CIS_act = getvalue(ser,"CIS",Pars.cc)
MC_act = getvalue(ser,"M",Pars.cc)
if CIS_act == MC_act:
    print("Test " + str(test_nr) + " " + test_name +"."+": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name +"."+ ": - Fail \n \n")
    fail_counter += 1
setcommand(ser,"G",Pars.cc,0)
##----------------------------------------------------------------------------------------------------------------------'
# ## Test 47 Script Output - Verify that Script output is printed via the SCRO-defined channel
test_nr = test_nr + 1
test_name = "Script Output - Verify that Script output is printed via the SCRO-defined channel (USB, RS232)"
USB_SCRO_OK = Serial_SCRO_OK = False
setcommandmaint(ser,"sld", Pars.key,":10000000240568656C6C6F00FFFFFFFFFFFFFFFFBB:00000001FF")  #
time.sleep(Pars.t_wait_mid)
setcommandmaint(ser,"sld", Pars.key,":10000000240568656C6C6F00FFFFFFFFFFFFFFFFBB:00000001FF")  # needed twice
if ser.port != Pars.COM_port_USB: # switch to USB (if not already connected via USB)
    try:
        ser = establish_serial_connection(Pars.COM_port_USB, Pars.COM_baudrate, Pars.COM_timeout)
    except serial.SerialException as e:
        print(e)
    print(ser)
setconfig(ser,"SCRO", 2)#USB
setcommand(ser,"R", 2)  # ReStart script.
start_time = time.time()
reply_full = b""
while (time.time() - start_time) < Pars.response_timeout:
    if ser.in_waiting > 0:
        reply_full = ser.readline()
        break
reply_midd = str(reply_full).strip()
if Pars.SCRO_test_print in reply_midd:
    USB_SCRO_OK = True
setconfig(ser,"SCRO", 1)  # Switch to Serial
try:
    ser = establish_serial_connection(Pars.COM_port_serial, Pars.COM_baudrate, Pars.COM_timeout)
except serial.SerialException as e:
    print(e)
print(ser)
# print(ser.is_open)
setcommand(ser,"R", 2)  # ReStart script.
start_time = time.time()
reply_full = b""
while (time.time() - start_time) < Pars.response_timeout:
    if ser.in_waiting > 0:
        reply_full = ser.readline()
        break
reply_midd = str(reply_full).strip()
if Pars.SCRO_test_print in reply_midd:
    Serial_SCRO_OK = True
if Serial_SCRO_OK and USB_SCRO_OK:
    print("Test " + str(test_nr) + " " + test_name + "." + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + "." + ": - Fail \n \n")
    print("USB_SCRO_OK",USB_SCRO_OK,"Serial_SCRO_OK",Serial_SCRO_OK)
    fail_counter += 1
##----------------------------------------------------------------------------------------------------------------------'
## Test 48 Serial Baud Rate - Verify RSBR is adjusted successfully.
test_nr = test_nr + 1
test_name = "Serial Baud Rate - Verify RSBR is adjusted successfully"
rsbr_init = getconfig(ser,"RSBR")
setconfig(ser,"RSBR",Pars.baud_rate_test)
setcommandmaint(ser,"eesav")
time.sleep(Pars.t_wait_long)
setcommandmaint(ser,"reset",Pars.key)
print("Controller has been reboot via %reset")
ser.close()
time.sleep(Pars.t_wait_long)
#------------------------------------------------------------------------------------------
try:
    ser = establish_serial_connection(Pars.COM_port_serial,Pars.baud_rate_test_Mbs,Pars.COM_timeout)
    # Use serial_connection for further operations
except serial.SerialException as e:
    print(e)
rsbr_fin = int(getconfig(ser,"RSBR"))
print("new baudrate is",ser.baudrate,"rsbr_fin",type(rsbr_fin))
if ser.baudrate == Pars.baud_rate_test_Mbs and rsbr_fin == Pars.baud_rate_test:
    print("Test " + str(test_nr) + " " + test_name + "." + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + "." + ": - Fail \n \n")
    fail_counter += 1
setconfig(ser,"RSBR",rsbr_init) #Revert to original baud rate & reconnect
setcommandmaint(ser,"eesav")
setcommandmaint(ser,"reset",Pars.key)
print("Controller has been reboot via %reset")
ser.close()
time.sleep(Pars.t_wait_long)
try:
    ser = establish_serial_connection(Pars.COM_port_USB,Pars.COM_baudrate,Pars.COM_timeout)
    # Use serial_connection for further operations
except serial.SerialException as e:
    print(e)
# # ###----------------------------------------------------------------------------------------------------------------------'
# # # ## Test 49 Serial Raw Redirect - Configure ISM, DMOD accordingly & Verify ?CD, ?SDT, ?DDT responses.
test_nr = test_nr + 1
test_name = "Serial Raw Redirect - Configure ISM, DMOD accordingly & Verify ?CD, ?SDT responses."
Raw_Redirect_Write_OK = Raw_Redirect_Read_OK_1 = Raw_Redirect_Read_OK_2 = False #Raw_Redirect_Write_OK --> Check USB write / RS232 read, Raw_Redirect_Read_OK --> Check USB read / RS232 write.
setconfig(ser,"ISM",2)#RS232 (Documentation is Wrong?)
setconfig(ser,"DMOD",5)#Modbus Mode = RS232 RTU, Requires %RESET to take effect
setcommandmaint(ser,"eesav")
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
try:
    ser_parallel = establish_serial_connection(Pars.COM_port_serial,Pars.COM_baudrate,Pars.COM_timeout)
    # Use serial_connection for further operations
except serial.SerialException as e:
    print(e)
ser_parallel.write(Pars.Raw_Redirect_Read_Test.encode())# send ?FID
time.sleep(Pars.t_wait_short)
CD_query = getvaluespecial(ser,"CD", 1)
time.sleep(Pars.t_wait_short)
SDT_query = getvaluespecial(ser,"SDT", 1)
time.sleep(Pars.t_wait_short)
DDT_query_list = []
DDT_query_pt1 = getvalue(ser,"DDT", 1)
ddt_count = 2#1st element is the length
time.sleep(Pars.t_wait_mid)
while ddt_count < (len(Pars.ASCII_conversion_read)+2):
    element = getvalue(ser,"DDT",ddt_count)
    DDT_query_list.append(element)
    time.sleep(Pars.t_wait_mid)
    ddt_count +=1
setcommand(ser,"CU",1,0)
for CU_cnt in range(len(Pars.ASCII_conversion_write)):
    element = Pars.ASCII_conversion_write[CU_cnt]
    print("element ",element)
    setcommand(ser,"CU",CU_cnt+3,element)
setcommand(ser,"CU",2,len(Pars.ASCII_conversion_write))
start_time = time.time()
reply_full = b""
while (time.time() - start_time) < Pars.response_timeout:
    if ser_parallel.in_waiting > 0:
        reply_full = ser_parallel.readline()
        break
reply_midd = str(reply_full).strip()
if Pars.Raw_Redirect_Write_Test in reply_midd:
    Raw_Redirect_Write_OK = True
print("Raw_Redirect_Write_OK is ",Raw_Redirect_Write_OK)
setconfig(ser,"ISM",0)#restore settings
setconfig(ser,"DMOD",0)
setcommandmaint(ser,"eesav")
setcommandmaint(ser,"clsav",Pars.key)
time.sleep(Pars.t_wait_long)
setcommandmaint(ser,"reset",Pars.key)
print("Controller has been reboot via %reset")
ser.close()
time.sleep(Pars.t_wait_long)
raw_cnt = 0
while raw_cnt < len(Pars.ASCII_conversion_read):
    if str(Pars.ASCII_conversion_read[raw_cnt]) == DDT_query_list[raw_cnt]:
        Raw_Redirect_Read_OK_1 = True
    else:
        print(str(Pars.ASCII_conversion_read[raw_cnt]),"Pars.ASCII_conversion_read[raw_cnt] result",str(DDT_query_list[raw_cnt]),"DDT_query_list[raw_cnt] result ")
    raw_cnt += 1
print("str(len(Pars.ASCII_conversion_read))", str(len(Pars.ASCII_conversion_read)),"DDT_query_list length",len(DDT_query_list))
if str(len(Pars.ASCII_conversion_read)) == DDT_query_pt1:
    Raw_Redirect_Read_OK_2 = True
else:
    print(str(len(Pars.ASCII_conversion_read)),"str(len(Pars.ASCII_conversion_read))",DDT_query_pt1,"DDT_query_pt1")
if Raw_Redirect_Read_OK_1 and Raw_Redirect_Read_OK_2 and Raw_Redirect_Write_OK:
    print("Test " + str(test_nr) + " " + test_name + "." + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + "." + ": - Fail \n \n")
    print("Raw_Redirect_Read_OK_1",Raw_Redirect_Read_OK_1,"Raw_Redirect_Read_OK_2",Raw_Redirect_Read_OK_2,"Raw_Redirect_Write_OK",Raw_Redirect_Write_OK)
    fail_counter += 1
# # # # ----------------------------------------------------------------------------------------------------------------------'
# # # # # ----------------------------------------------------------------------------------------------------------------------'
# # Finale
# # ------------------------------------------------------------------------------------------------------------------------'
test_end_time = time.time()
test_duration = test_end_time-test_start_time
print("Number of tests completed" ,test_nr,"Number of failed tests:",fail_counter, ". Test_duration was: ",test_duration," secs.")
ser.close()
time.sleep(Pars.t_wait_long)
