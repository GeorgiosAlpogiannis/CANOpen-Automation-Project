# Import packages
import serial
import time
import Pars
import io
# Define Functions
def wait(milliseconds):
    time.sleep(milliseconds / 1000)

def setcommand(*args):
    cmd = "!" + " ".join(str(arg) for arg in args) + "\r"
    #print(cmd)
    ser.write(cmd.encode())

def setconfig(*args):
    cmd = "^" + " ".join(str(arg) for arg in args) + "\r"
    ser.write(cmd.encode())


def setcommandmaint(*args):
    cmd = "%" + " ".join(str(arg) for arg in args) + "\r"
    ser.write(cmd.encode())

def getvalue(*args):
    start_time = time.time()
    cmd = "?" + " ".join(str(arg) for arg in args) + "\r"
    # ser.write(cmd.encode())
    # # print(cmd)
    # time.sleep(0.002)#0.002
    # elapsed_time = time.time() - start_time
    # # print(f"Time elapsed getvalue 3a is : {elapsed_time:.2f} seconds.")s
    # reply_full = ser.readline().replace(cmd.encode(), b'').strip()
    # elapsed_time = time.time() - start_time
    # # print(f"Time elapsed getvalue 3b is : {elapsed_time:.2f} seconds.")
    ser.write(cmd.encode())
    start_time = time.time()
    reply_full = b""
    # Wait for a response with a timeout
    timeout = 10  # Maximum time to wait in seconds
    while (time.time() - start_time) < timeout:
        if ser.in_waiting > 0:
            reply_full = ser.readline()
            break
    reply_full = reply_full.replace(cmd.encode(), b'').strip()
    print("reply_full is ",reply_full)
    reply_value_mid = reply_full.decode().split("=")
    print("reply_value_mid",reply_value_mid)
    reply_value = reply_value_mid[1]
    #print(reply_value)
    return reply_value

def getvaluespecial(*args):
    cmd = "?" + " ".join(str(arg) for arg in args) + "\r"
    ser.write(cmd.encode())
    #print(cmd)
    ser.flushInput()#needed after performing !stt (which returns data)
    time.sleep(0.004)
    reply_full = ser.readline().replace(cmd.encode(), b'').strip()
    #print(reply_full)
    reply_value_mid = reply_full.decode().split("=")
    #print(reply_value_mid)
    reply_value = reply_value_mid[1]
    #print(reply_value)
    return reply_value

def getconfig(*args):
    cmd = "~" + " ".join(str(arg) for arg in args) + "\r"
    ser.write(cmd.encode())
    # print(cmd)
    time.sleep(0.004)
    reply_full = ser.readline().replace(cmd.encode(), b'').strip()
    #print("get config reply_full is",reply_full)
    reply_value_mid = reply_full.decode().split("=")
    reply_value = reply_value_mid[1]
    #print("get config reply_value is",reply_value)
    return reply_value
# -------------------------------------------------------------------------------------------------------------------------------
# Fault flags
def FF_read(FF):
    #print("FF start is ",FF)
    FF_init = int(FF)
    # print("FF init is ",FF_init)
    FF_list_init = [FF_init & 0b01, FF_init & 0b10, FF_init & 0b100, FF_init & 0b1000, FF_init & 0b10000,
                    FF_init & 0b100000, FF_init & 0b1000000, FF_init & 0b10000000, FF_init & 0b100000000]
    FF_list = [bool(item) for item in FF_list_init]

    FF_dict = {
        'FF_Overheat': FF_list[0],
        'FF_Overvolt': FF_list[1],
        'FF_Undervolt': FF_list[2],
        'FF_Short': FF_list[3],
        'FF_Estop': FF_list[4],
        'FF_SED': FF_list[5],
        'FF_Mosfail': FF_list[6],
        'FF_DefConf': FF_list[7],
        'FF_STO_fault': FF_list[8]
    }
    #print("FF end is ",FF)
    return FF_dict
# FM flags
def FM_read(FM):

    FM_init = int(FM)
    FM_list_init = [FM_init & 0b01, FM_init & 0b10, FM_init & 0b100, FM_init & 0b1000, FM_init & 0b10000,
                    FM_init & 0b100000, FM_init & 0b1000000, FM_init & 0b10000000]
    FM_list = [bool(item) for item in FM_list_init]

    FM_dict = {
        'FM_AmpLim': FM_list[0],
        'FM_Stall': FM_list[1],
        'FM_LoopErr': FM_list[2],
        'FM_Safestop': FM_list[3],
        'FM_FwdLim': FM_list[4],
        'FM_RevLim': FM_list[5],
        'FM_AmpTrig': FM_list[6],
        'FM_FetsOff': FM_list[7]
    }
    return FM_dict
# FM flags
def FS_read(FS):
    FS_init = int(FS)
    FS_list_init = [FS_init & 0b01, FS_init & 0b10, FS_init & 0b100, FS_init & 0b1000, FS_init & 0b10000,
                    FS_init & 0b100000, FS_init & 0b1000000, FS_init & 0b10000000,FS_init & 0b100000000]
    FS_list = [bool(item) for item in FS_list_init]

    FS_dict = {
        'FS_Serial': FS_list[0],
        'FS_Pulse': FS_list[1],
        'FS_Analog': FS_list[2],
        'FS_Fetsoff': FS_list[3],
        'FS_Stall': FS_list[4],
        'FS_AtLimit': FS_list[5],
        'FS_STO': FS_list[6],
        'FS_RunScript': FS_list[7],
        'FS_Setup': FS_list[8]
    }
    return FS_dict
# perform a Fault Flag Type test
def fault_flag_test(test_name,FF_type,counts,fail_counter,test_setting):
    for cnt in range(counts):
        init_setting = getconfig(FF_type, cnt+1)  # write down default setting
        setconfig(FF_type,cnt+1,test_setting)  # apply test setting
        if test_name != "FF_SED":
            time.sleep(Pars.t_wait_short)#sed takes longer to trigger
        else:
            time.sleep(Pars.t_wait_mid)#sed takes longer to trigger
        FF = getvalue("FF", 1)
        FF_dict = FF_read(FF)
        FM = getvalue("FM", Pars.cc)
        FM_dict = FM_read(FM)
        print("FF_dict",FF_dict,"FM_dict",FM_dict)
        if (FF_dict[test_name] and FM_dict["FM_FetsOff"]):
            print("Test " + str(test_nr) + "." + str(cnt) +" "+ test_name+": - Pass \n \n")
        else:
            print("Test " + str(test_nr) + "." + str(cnt) +" "+ test_name+": - Fail \n \n")
            fail_counter += 1
        DO_sum = int(getvalue("DO"))
        setconfig(FF_type, cnt+1, init_setting)  # restore default setting
    if fail_counter == 0:
        print("Test " + str(test_nr) +" "+ test_name+": - Pass \n \n")
        result = "Pass"
    else:
        print("Test " + str(test_nr) +" "+ test_name+": - Fail \n \n")
        result = "Fail"
    return DO_sum
# perform a Fault Flag Type (no config) test
def fault_flag_test_no_config(test_name,FF_type,counts,fail_counter):
    setcommand(FF_type,1)
    time.sleep(Pars.t_wait_short)
    FF = getvalue("FF", 1)
    FF_dict = FF_read(FF)
    FM = getvalue("FM", Pars.cc)
    FM_dict = FM_read(FM)
    if (FF_dict[test_name] and FM_dict["FM_FetsOff"]):
        print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
        fail_counter += 1
    if fail_counter == 0:
        print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
        result = "Pass"
        result = "Pass"
    else:
        print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
        result = "Fail"
    return result

def calibration_test(test_name,FF_type,counts,fail_counter,test_setting):
    for cnt in range(counts):
        init_setting = getconfig(FF_type)  # write down default setting
        # print(init_setting)
        setconfig(FF_type,test_setting)  # apply test setting
        time.sleep(Pars.t_wait_long)
        setcommand("STT")
        time.sleep(Pars.t_wait_long)
        FF = getvaluespecial("FF", 1)
        FF_dict = FF_read(FF)
        FM = getvaluespecial("FM", Pars.cc)
        FM_dict = FM_read(FM)
        #print(FF_dict)
        DO_sum = int(getvalue("DO"))
        #print("DO is ",DO_sum)
        if (FF_dict[test_name] and FM_dict["FM_FetsOff"]):
            print("Test " + str(test_nr) + "." + str(cnt) +" "+ test_name+": - Pass \n \n")
            print("FAIL COUNTER IS ",fail_counter)
            fail_bool = 0
        else:
            print("Test " + str(test_nr) + "." + str(cnt) +" "+ test_name+": - Fail \n \n")
            fail_counter += 1
            fail_bool = 1
        setconfig(FF_type,init_setting)  # restore default setting
        setcommand("STT")

    if fail_bool == 0:
        print("Test " + str(test_nr) +" "+ test_name+": - Pass \n \n")
        result = "Pass"
    else:
        print("Test " + str(test_nr) +" "+ test_name+": - Fail \n \n")
        result = "Fail"
    return DO_sum
#--------------------------------------------------------------------
# var read / write function (used for !B, !Var etc)
def var_read_write_old(test_abrv,test_name,test_nr,fail_counter):
    setcommand(test_abrv, 0, 0)#set all boolean vars to zero
    var = getvalue(test_abrv)
    var_length = round(len(var)/2)
    print(var_length)
    cnt = 1
    sum_zero = 0
    sum_one = 0
    while cnt <= var_length:
        setcommand(test_abrv, cnt, 0)#apply logical zero
        zero = int(getvalue(test_abrv,cnt))
        setcommand(test_abrv, cnt, 1)#apply logical one
        one = int(getvalue(test_abrv,cnt))
        sum_one = sum_one + one
        sum_zero = sum_zero + zero
        setcommand(test_abrv, cnt, 0)#restore to default (logical zero)
        cnt += 1
        print(cnt)
    print(sum_zero)
    print(sum_one)
    if sum_zero == 0  and sum_one == var_length:
        print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
        fail_counter += 1
def var_read_write(test_abrv,test_name,test_nr,fail_counter):
    var = getvalue(test_abrv)
    var_length = round(len(var)/2)
    #print("var length is ",var_length)
    cnt_zero = 1
    cnt_one = 1
    sum_zero = 0
    sum_one = 0
    while cnt_zero <= var_length:
        setcommand(test_abrv, cnt_zero, 0)  # set all  vars to zero
        zero = int(getvalue(test_abrv,cnt_zero))
        sum_zero = sum_zero + zero
        cnt_zero += 1
    setcommand(test_abrv, 0, 1)  # set all  vars to one
    while cnt_one <= var_length:
        setcommand(test_abrv, cnt_one, 1)  # set all  vars to zero
        one = int(getvalue(test_abrv,cnt_one))
        sum_one = sum_one + one
        cnt_one +=1


    setcommand(test_abrv, 0, 0)#restore to default (logical zero)
    #print("sum_zero is:",sum_zero)
    #print("sum_one is:",sum_one)
    if sum_zero == 0 and sum_one == var_length:
        print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
        fail_counter += 1
# --------------------------------------------------------------------------------------------------------------
# Calculate sum of 2^x powers, where x is e.g. the number Douts.
def power_sum(DO_nr):

    DO_Sum_Tot =1 #2^0
    k = 1
    while k < DO_nr:
        answer = 2
        increment = 2
        i = 1
        while i < k:
            j = 1
            while j < 2: #2 for binary
                answer = answer + increment
                j += 1
            increment = answer
            i+=1
        DO_Sum_Tot = DO_Sum_Tot + answer
        k +=1
    return DO_Sum_Tot
#----------------------------------------------------------------------------------------------------------------------
# dout actions
def dout_actions_test(test_abrv,dout_aa,DO_nr,test_setting,DO_sum_tot,fail_counter,test_nr):
    dout_cnt = 1
    DO_sum = 0
    setconfig("RWD",0)
    setconfig("SED", 0, 0)  # disable SED
    while dout_cnt <= DO_nr:
        setconfig("DOA", dout_cnt, dout_aa)  # configure DOUT action
        dout_cnt+=1
    setcommand(test_abrv, Pars.cc, test_setting)
    time.sleep(Pars.t_wait_mid)
    DO_sum = int(getvalue("DO"))
    print("DO_sum is ", DO_sum,"DO_sum_tot",DO_sum_tot)
    if DO_sum == DO_sum_tot:
        print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
        fail_counter += 1
    setcommand(test_abrv, Pars.cc, 0)#restore
    time.sleep(Pars.t_wait_mid)
    setconfig("SED", 0, 2)  # restore SED
    return fail_counter
# --------------------------------------------------------------------------------------------------------------------
# DINA Test function (DINA actions)
def DINA_test(DI_nr,DINA_setting,cc,flag_triggered,fail_counter,MC_test,home_count):
    DI_count = 1
    setconfig("SED", 0, 0)
    setconfig("RWD",0)
    all_DINs_OK = True
    while DI_count <= DI_nr:
        setconfig("DINA", DI_count,DINA_setting)#select digital input action
        setconfig("DINL", DI_count, 0)#start with active level 0 --> DIN is low
        mid = getvalue("DI",DI_count)
        din_deact = int(mid)
        setcommand("G", cc, MC_test)  # restore settings
        print("din_deact",din_deact)
        time.sleep(Pars.t_wait_mid)# long, mid
        MC_mid_1 = getvalue("P", cc)
        MC_mid_2 = MC_mid_1.split(':')
        MC_mid = MC_mid_2[cc-1]
        MC_init = int(MC_mid)
        setconfig("DINL", DI_count, 1)#trigger DIN action
        time.sleep(Pars.t_wait_mid)#mid
        sft_FM = getvalue("FM", cc)
        sft_dict = FM_read(sft_FM)
        din_act = int(getvalue("DI",DI_count))
        MC_after = int(getvalue("P",cc))
        print("MC_init is",MC_init,"MC_after is",MC_after)
        FS_script = getvalue("FS", 1)
        FS_dict_script = FS_read(FS_script)
        bs_counter = int(getvalue("CB",cc))
        enc_counter = int(getvalue("C",cc))
        ssi_counter = int(getvalue("CSS",cc))
        # print(bs_counter,enc_counter,ssi_counter)
        # restore settings
        setconfig("DINA", 0, 0)  # restore settings
        setconfig("DINL", 0, 0)  # restore settings
        setcommand("G", cc, 0)  # restore settings
        setcommand("R",0) # stop script , if running
        setcommand("CB", cc,0) # zero counters
        setcommand("C", cc,0)
        setcommand("CSS", cc,0)
        setcommand("EX", 1)  # clear sft flag
        time.sleep(Pars.t_wait_short)
        if flag_triggered == "FM_FetsOff": # used for dead man switch
             setcommand("MG", 1)  # clear sft flag
             time.sleep(Pars.t_wait_long)  # mid
        time.sleep(Pars.t_wait_mid)#mid
        sft_FM_cleared = getvalue("FM", cc)
        sft_dict_cleared = FM_read(sft_FM_cleared)
        print("din_act",din_act)
        if flag_triggered == "DEAD": # used for dead man switch
            cond_flag = 1
        elif flag_triggered == "INV":
            if MC_init == -MC_after:
                cond_flag = 1
            else:
                cond_flag = 0
        elif flag_triggered == "FS_RunScript":
            cond_flag = FS_dict_script[flag_triggered]
        elif flag_triggered == "HOME":
            if bs_counter == enc_counter == ssi_counter == home_count:
                cond_flag = 1
            else:
                cond_flag = 0
        else:
            cond_flag = sft_dict[flag_triggered] and not sft_dict_cleared[flag_triggered]

        #print("sft_FM_cleared",sft_FM_cleared)
        #print("sft_dict_cleared",sft_dict_cleared)
        if cond_flag and din_act == 1 and din_deact == 0 :
            print("Test " + str(test_nr) + " " + test_name + ". DIN nr " + str(DI_count) + ": - Pass \n \n")
        else:
            print("Test " + str(test_nr) + " " + test_name + ". DIN nr " + str(DI_count) + ": - Fail \n \n")
            all_DINs_OK = False
        DI_count +=1
    if all_DINs_OK:
        print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
        fail_counter +=1
    #setconfig("SED", 0, 2)
# ---------------------------------------------------------------------------------------------------------------------
# Compute slope : Requires small slopes.
def compute_slope(test_abrv,cc,DI_count,DINA_setting):
    setconfig("RWD", 0)
    setcommand("MG",1)
    setconfig("SED", 0, 0)
    setconfig("DINA", DI_count, DINA_setting)  # select digital input action
    setconfig("EDEC", cc, Pars.EDEC_ramp_test)
    setconfig("DINL", DI_count, 0)  # start with active level 0 --> DIN is low
    setcommand("G", cc, Pars.MC_test)  # give test motor command
    time.sleep(Pars.t_wait_mid)
    prev_val = int(getvalue(test_abrv, cc))
    setconfig("DINL", DI_count, 1)  # trigger DIN action
    print("prev_val",prev_val)
    prev_time = time.time()
    slope_cnt = 0
    slope_sum = 0
    while prev_val > 0:
        # Read new value and time
        new_val = int(getvalue(test_abrv,cc))
        new_time = time.time()
        # Compute slope
        slope = (new_val - prev_val) / (new_time - prev_time)
        slope_sum = slope_sum + slope
        # Print slope and update previous values
        prev_val = new_val
        prev_time = new_time
        slope_cnt +=1
    slope_avg = abs(slope_sum / slope_cnt)
    print("slope_avg is",slope_avg)
    return slope_avg
# ---------------------------------------------------------------------------------------------------------------------
## Amps Trigger Tests
def amps_trigger_test(test_abrv,cc,ATGA_setting,fail_counter,test_nr,MC,home_count,FM_flag):
    setcommand("SED",0,0)
    setcommand("MG",1)
    setconfig("RWD",0)
    time.sleep(Pars.t_wait_mid)
    setcommand("G",cc,MC)
    time.sleep(Pars.t_wait_short) #
    P_act = int(getvalue("P",cc))
    ZPAO_test_setting = 0
    ZPAO_init = getconfig("ZPAO",2)
    setconfig("ATGA",cc,ATGA_setting)
    setconfig("ZPAO",2,ZPAO_test_setting)#apply test_setting
    time.sleep(Pars.t_wait_mid)#mid
    FM = getvalue("FM",cc)
    FS = getvalue("FS",cc)
    ATGA_result = FM_read(FM)
    FS_result = FS_read(FS)
    P_deact = int(getvalue("P",cc))
    M_deact = int(getvalue("M",cc))
    bs_counter = int(getvalue("CB", cc))
    enc_counter = int(getvalue("C", cc))
    ssi_counter = int(getvalue("CSS", cc))
    print(test_abrv,P_act,P_deact)
    if test_abrv == "Dead" and P_act > 0 and P_deact == 0:
        ATGA_cond = True
    elif test_abrv == "Inv" and P_act > 0 and M_deact < 0:
        ATGA_cond = True
    elif test_abrv == "Script" :
        ATGA_cond = FS_result["FS_RunScript"]
    elif test_abrv == "Home" and bs_counter == enc_counter == ssi_counter == home_count:
        ATGA_cond = True
    else:
        ATGA_cond = ATGA_result[FM_flag]
    print("ATGA_result[FM_flag]",ATGA_result[FM_flag],"ATGA_result",ATGA_result)
    if ATGA_cond and ATGA_result["FM_AmpTrig"]:
        print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
        fail_counter += 1
    setconfig("ATGA",cc,0)
    setcommand("SED",0,0)
    setconfig("ZPAO",2,ZPAO_init)
    setcommand("R", 0)  # Stop script.
    setcommand("CB", cc, 0)  # zero counters
    setcommand("C", cc, 0)
    setcommand("CSS", cc, 0)
    setcommand("MG",1)
    time.sleep(Pars.t_wait_short)
    return ATGA_result
# ---------------------------------------------------------------------------------------------------------------------
## Establish serial Connection
def establish_serial_connection(COM_port,COM_baudrate,COM_timeout):
    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        try:
            ser = serial.Serial(COM_port, COM_baudrate, timeout=COM_timeout)
            print("Serial connection established on", COM_port)
            return ser
        except serial.SerialException as e:
            print(f"Failed to connect on {COM_port}: {e}")
            attempt += 1
            time.sleep(1)  # Wait for 1 second before retrying

    raise serial.SerialException(f"Could not open port {COM_port} after {max_attempts} attempts")
# Use the function to establish the connection
# ----------------------------------------------------------------------------------------------------------------------
# Create a Serial object by specifying the serial port and baud rate:
# start_time = time.time()
#ser = serial.Serial(Pars.COM_port,Pars.COM_baudrate,timeout = Pars.COM_timeout)
try:
    ser = establish_serial_connection(Pars.COM_port,Pars.COM_baudrate,Pars.COM_timeout)
    # Use serial_connection for further operations
except serial.SerialException as e:
    print(e)
print(ser)
# print(ser.is_open)
if ser.is_open == True:
    print("Controller found on specified Serial Port!")
else:
    print("Controller could not be found on specified Serial Port!")
# ----------------------------------------------------------------------------------------------------------------------
# Tests start
# ----------------------------------------------------------------------------------------------------------------------
#Reboot via %reset

print("START! \n")
test_start_time = time.time()
if Pars.reboot_flag == True:
    print("Perform reboot via %reset ")
    setcommandmaint("reset",Pars.key)
    print("Controller has been reboot via %reset")
    time.sleep(Pars.t_wait_long)
    ser.close()
    time.sleep(Pars.t_wait_long)
    #ser = serial.Serial(Pars.COM_port, Pars.COM_baudrate, timeout=Pars.COM_timeout)
    try:
        ser = establish_serial_connection(Pars.COM_port, Pars.COM_baudrate, Pars.COM_timeout)
        # Use serial_connection for further operations
    except serial.SerialException as e:
        print(e)
    print(ser)
    # print(ser.is_open)
    if ser.is_open == True:
        print("Controller found on specified Serial Port!")
    else:
        print("Controller could not be found on specified Serial Port!")
#-----------------------------------------------------------------------------------------------------------------------
# Perform reset to defaults & Clear fault flags to begin
if Pars.reset_defaults_flag == True:
    print("Perform reset to defaults ")
    setcommandmaint("eerst",Pars.key)
    print("Controller has been reset to defaults")
    time.sleep(Pars.t_wait_vlong)
# Clear initial errors (SED, FETS OFF)
FF = getvalue("FF",1)
FF_dict = FF_read(FF)
if (FF_dict["FF_Estop"] or FF_dict["FF_SED"]): #'SED or / and Estop are active
	setconfig("SED", 0, 0)
	setcommand("MG", 1)
	print("Cleared initial SED error by disabling sensor error detection. \n \n")
# Write Parameters defined in Pars
setconfig("RS", Pars.cc, Pars.Rs)# apply setting
setconfig("LD", Pars.cc, Pars.Ld)# apply setting
setconfig("LQ", Pars.cc, Pars.Lq)# apply setting
print(Pars.Rs,Pars.Ld,Pars.Lq)
# ----------------------------------------------------------------------------------------------------------------------
# Part 1 start: Standalone controller tests.
# ----------------------------------------------------------------------------------------------------------------------
test_nr = 0
fail_counter = 0
##----------------------------------------------------------------------------------------------------------------------
# # #  Test 1 Overheat: Verify Overheat and Fets OFF flags trigger when OTL limit is violated.
# Calculate and print the elapsed time
# elapsed_time = time.time() - start_time
# print(f"Time elapsed until test 1 start is : {elapsed_time:.2f} seconds.")
test_nr = test_nr + 1
test_name = "FF_Overheat"
test_abrv = "OTL"
counts = 3#3 different temp limits
test_result = fault_flag_test(test_name,test_abrv,counts,fail_counter, Pars.overheat_lim_test)
# elapsed_time = time.time() - start_time
# print(f"Time elapsed until test 1 end is : {elapsed_time:.2f} seconds.")
# # # ----------------------------------------------------------------------------------------------------------------------
# # # #  Test 2 Overvolt: Verify Overvolt and Fets OFF flags trigger when OVL limit is violated.
test_nr = test_nr + 1
test_name = "FF_Overvolt"
test_abrv = "OVL"
counts = 1#only 1 OVL limit
test_result = fault_flag_test(test_name,test_abrv,counts,fail_counter, Pars.overvolt_lim_test)
# # # ----------------------------------------------------------------------------------------------------------------------
# # #  Test 3 Undervolt: Verify Undervolt and Fets OFF flags trigger when UVL limit is violated.
test_nr = test_nr + 1
test_name = "FF_Undervolt"
test_abrv = "UVL"
counts = 1#only 1 OVL limit
test_result = fault_flag_test(test_name,test_abrv,counts,fail_counter,Pars.undervolt_lim_test)
# # ----------------------------------------------------------------------------------------------------------------------
# # #  Test 4 Estop: Verify Estop & Fets OFF flags trigger when Estop is requested.
test_nr = test_nr + 1
test_name = "FF_Estop"
test_abrv = "EX"
counts = 1 #only 1 Estop limit
test_result = fault_flag_test_no_config(test_name,test_abrv,counts,fail_counter)
setcommand("MG",1)#clear Estop
time.sleep(Pars.t_wait_long)
# # # ----------------------------------------------------------------------------------------------------------------------
# # #  Test 5 SED error: Verify SED & Fets OFF flags trigger when SED conditions are violated(no sensor connected).
test_nr = test_nr + 1
test_name = "FF_SED"
test_abrv = "SED"
counts = 1 #2
test_result = fault_flag_test(test_name,test_abrv,counts,fail_counter,Pars.sed_value_test)
# # # ----------------------------------------------------------------------------------------------------------------------
#  # Test 6 Mosfail error: Verify Mosfail flags trigger when Mosfail conditions are violated(using ZSRM).
test_nr = test_nr + 1
test_name = "FF_Mosfail"
test_abrv = "ZSRM"
counts = 1 #2
test_result = calibration_test(test_name,test_abrv,counts,fail_counter,Pars.ZSRM_value_test)
# ----------------------------------------------------------------------------------------------------------------------
# Test 7 Script run functionality: Test that script can be (re)started and stopped using !R ).
test_nr = test_nr + 1
test_name = "Script Start / Stop / Restart"
# print("Perform reboot via %reset ")
setconfig("SCRO",2)
setcommandmaint("sld",Pars.key,":1000000002010315001F0206020102012903E80391:10001000230300002000FFFFFFFFFFFFFFFFFFFFA4:00000001FF")#
time.sleep(Pars.t_wait_mid)
setcommandmaint("sld",Pars.key,":1000000002010315001F0206020102012903E80391:10001000230300002000FFFFFFFFFFFFFFFFFFFFA4:00000001FF")# needed twice
setcommand("R",1)# Start script.
time.sleep(Pars.t_wait_vlong)
var = getvaluespecial("Var",1)
FS_active = getvalue("FS", 1)
FS_dict_active = FS_read(FS_active)
setcommand("R", 0)  # Stop script.
time.sleep(Pars.t_wait_mid)
FS_deact = getvalue("FS", 1)
FS_dict_deact = FS_read(FS_deact)
setcommand("R", 2)  # Restart script.
time.sleep(Pars.t_wait_mid)
FS_react = getvalue("FS", 1)
FS_dict_react = FS_read(FS_react)
if FS_dict_active["FS_RunScript"] and not FS_dict_deact["FS_RunScript"] and FS_dict_react["FS_RunScript"]:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter += 1
setcommand("R", 0)  # Stop script.
# # # # # # ----------------------------------------------------------------------------------------------------------------------
# # Test 8 Script auto-start functionality: Reboot controller and verify script starts running automatically ).
test_nr = test_nr + 1
test_name = "Script Auto-Start"
setcommand("R", 0)  # Stop script.
time.sleep(Pars.t_wait_mid)
FS_bef_reset = getvalue("FS", 1)
FS_dict_bef_reset = FS_read(FS_bef_reset)
setconfig("BRUN", 2)  # Enable immediate script-auto start.
setcommandmaint("eesav") # save to controller
print("Perform reboot via %reset ")
setcommandmaint("reset",Pars.key)
setcommandmaint("reset",Pars.key)
print("Controller has been reboot via %reset")
time.sleep(Pars.t_wait_long)
ser.close()
time.sleep(Pars.t_wait_long)
# ser = serial.Serial(Pars.COM_port, Pars.COM_baudrate, timeout=Pars.COM_timeout)
try:
    ser = establish_serial_connection(Pars.COM_port,Pars.COM_baudrate,Pars.COM_timeout)
    # Use serial_connection for further operations
except serial.SerialException as e:
    print(e)
print(ser)
# print(ser.is_open)
if ser.is_open == True:
    print("Controller found on specified Serial Port!")
else:
    print("Controller could not be found on specified Serial Port!")
# Perform reset to defaults & Clear fault flags to begin
if Pars.reset_defaults_flag == True:
    print("Perform reset to defaults ")
    setcommandmaint("eerst",Pars.key)
    print("Controller has been reset to defaults")
    time.sleep(Pars.t_wait_vlong)
FS_aft_reset = getvalue("FS", 1)
FS_dict_aft_reset = FS_read(FS_aft_reset)
print(FS_dict_bef_reset)
print(FS_dict_aft_reset)
if not FS_dict_bef_reset["FS_RunScript"] and FS_dict_aft_reset["FS_RunScript"]:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter += 1
setcommand("R", 0)  # Stop script.
setconfig("BRUN", 0)  # Disable script-auto start.
# # # # # # ----------------------------------------------------------------------------------------------------------------------
# # Test 9: Read / Write all boolean variables.
test_nr = test_nr + 1
test_name = "Boolean_Vars_Read_Write"
test_abrv = "B"
var_read_write(test_abrv,test_name,test_nr,fail_counter)
# # # ----------------------------------------------------------------------------------------------------------------------
# # Test 10: Write all user variables .
test_nr = test_nr + 1
test_name = "User_Vars_Read_Write"
test_abrv = "VAR"
var_read_write(test_abrv,test_name,test_nr,fail_counter)
# # # ----------------------------------------------------------------------------------------------------------------------
# # # DOUT tests
# # # ----------------------------------------------------------------------------------------------------------------------
# Dout = getconfig("DOA")
# DO_nr = round(len(Dout) / 2)
DO_nr = Pars.DO_nr
DO_sum_tot = power_sum(DO_nr)
#print("DO_nr",DO_nr,"len DOUT",len(Dout))
# # ----------------------------------------------------------------------------------------------------------------------
## Test 11: Digital outputs - Set using !DS
test_nr = test_nr + 1
test_name = "Digital outputs control via !DS"
setcommand("DS",DO_sum_tot)# activate all DOUT's
time.sleep(Pars.t_wait_short)
DO_act_check = int(getvalue("DO"))# de-activate all DOUT's
setcommand("DS",0)
time.sleep(Pars.t_wait_short)
DO_deact_check = int(getvalue("DO"))# de-activate all DOUT's
print(DO_act_check)
print(DO_deact_check)
print(DO_sum_tot)
if DO_act_check == DO_sum_tot and DO_deact_check == 0:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
# # # # ----------------------------------------------------------------------------------------------------------------------
# Test 12: Digital output actions- Motor is ON
test_nr = test_nr + 1
test_name = "Digital output actions Motor is ON"
test_abrv = "G"
test_setting = Pars.MC_test
dout_aa = 16*Pars.cc+1 # aa according to DOA syntax in user manual
dout_result = dout_actions_test(test_abrv,dout_aa,DO_nr,test_setting,DO_sum_tot,fail_counter,test_nr)
# ----------------------------------------------------------------------------------------------------------------------
# Test 13: Digital output actions- Motor is Reverse
test_nr = test_nr + 1
test_name = "Digital output actions Motor is Reverse"
test_abrv = "G"
test_setting = -Pars.MC_test
dout_aa = 16*Pars.cc+2 # aa according to DOA syntax in user manual
dout_result = dout_actions_test(test_abrv,dout_aa,DO_nr,test_setting,DO_sum_tot,fail_counter,test_nr)
# # ----------------------------------------------------------------------------------------------------------------------
# Test 14: Digital output actions - Overvoltage
test_nr = test_nr + 1
test_name = "Digital output actions - Overvoltage"
test_name_aux = "FF_Overvolt"
test_abrv = "OVL"
counts = 1#only 1 OVL limit
test_setting = Pars.overvolt_lim_test
dout_aa = 16*Pars.cc+3 # aa according to DOA syntax in user manual
setconfig("DOA", 0, dout_aa)  # configure DOUT action as OVL for DOUT's
DOA_OVL_result = fault_flag_test(test_name_aux, test_abrv, counts, fail_counter, test_setting)
print(DOA_OVL_result)
if DOA_OVL_result == DO_sum_tot:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter += 1
# # # # ----------------------------------------------------------------------------------------------------------------------
# Test 15: Digital output actions - Overtemperature
test_nr = test_nr + 1
test_name = "Digital output actions - Overtemperature"
test_name_aux = "FF_Overheat"
test_abrv = "OTL"
counts = 1#only 1 OTL limit
test_setting = Pars.overheat_lim_test
dout_aa = 16*Pars.cc+4 # aa according to DOA syntax in user manual
setconfig("DOA", 0, dout_aa)  # configure DOUT action as OVL for DOUT's
DOA_OTL_result = fault_flag_test(test_name_aux, test_abrv, counts, fail_counter, test_setting)
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
setconfig("DOA", 0, dout_aa)  # configure DOUT action as OVL for DOUT's
time.sleep(Pars.t_wait_short)
LED_OFF_threshold = round(DO_sum_tot*Pars.LED_iters/3)
LED_ON_threshold = round((2*DO_sum_tot*Pars.LED_iters)/3)
LED_cnt = 0
LED_OFF_sum = 0
LED_ON_sum = 0
default_set = getconfig("OVL")
while LED_cnt < Pars.LED_iters:
    do_mirror_check_1 = int(getvalue("DO"))# DOUT LED should be mostly OFF
    LED_OFF_sum = LED_OFF_sum + do_mirror_check_1
    setconfig("OVL",Pars.overvolt_lim_test)# this will cause DOUT LED to be mostly ON
    time.sleep(Pars.t_wait_mid)
    do_mirror_check_2 = int(getvalue("DO"))
    LED_ON_sum = LED_ON_sum + do_mirror_check_2
    setconfig("OVL", default_set)  # restore setting to default
    time.sleep(Pars.t_wait_mid)
    LED_cnt += 1
print("LED_OFF_sum (OFF),",LED_OFF_sum,"LED_OFF_threshold (OFF)",LED_OFF_threshold,"LED_ON_sum (ON),",LED_ON_sum,"LED_ON_threshold (ON)",LED_ON_threshold,"DO_sum_tot",DO_sum_tot)
if LED_OFF_sum < LED_OFF_threshold and LED_ON_sum > LED_ON_threshold:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter += 1
# # # ----------------------------------------------------------------------------------------------------------------------
# Test 17: Digital output actions - No Mosfail
test_nr = test_nr + 1
test_name = "Digital output actions - No Mosfail"
test_name_aux = "FF_Mosfail"
test_abrv = "ZSRM"
counts = 1#only 1 OTL limit
test_setting = Pars.ZSRM_value_test
dout_aa = 16*Pars.cc+6 # aa according to DOA syntax in user manual
setconfig("DOA", 0, dout_aa)  # configure DOUT action as OVL for DOUT's
time.sleep(Pars.t_wait_short)
No_mosfail_check_1 = int(getvalue("DO"))
No_mosfail_check_2 = calibration_test(test_name_aux,test_abrv,counts,fail_counter,Pars.ZSRM_value_test)
time.sleep(Pars.t_wait_short)
#print(No_mosfail_check_1,No_mosfail_check_2,DO_sum_tot)
if No_mosfail_check_1 == DO_sum_tot and No_mosfail_check_2 == 0:
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
    fail_counter += 1
setconfig("DOA", 0, 0)  # restore DOUT's to No Action
time.sleep(Pars.t_wait_long)#neeeded
# # # # ----------------------------------------------------------------------------------------------------------------------
# # # # DINA action tests
# # ## ----------------------------------------------------------------------------------------------------------------------
# # # Read Digital input number
Din_1 = getvalue("DI")
print("DIN 1 DONE")
Din_orig = len(Din_1)
Din_orig_2 = Din_orig/2
DI_nr_alt = round(len(Din_1) / 2) #check again
print("DI_nr_alt",DI_nr_alt,"Din_orig",Din_orig,"Din_1",len(Din_1))
DI_nr = Pars.DI_nr
# ## ----------------------------------------------------------------------------------------------------------------------
# Test 18: Digital input actions - Safety Stop
test_nr = test_nr + 1
test_name = "Digital input actions - Safety Stop"
DINA_setting = 1 + 16 * Pars.kk
flag_triggered = "FM_Safestop"
dina_result = DINA_test(DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count)
## ----------------------------------------------------------------------------------------------------------------------
# # Test 19: Digital input actions - EM Stop
test_nr = test_nr + 1
test_name = "Digital input actions - EM Stop"
setcommand("MG", 1)
time.sleep(Pars.t_wait_mid)#neeeded
DINA_setting = 2 + 16 * Pars.kk
flag_triggered = "FM_FetsOff"
dina_result = DINA_test(DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count)
# ## ----------------------------------------------------------------------------------------------------------------------
# #Test 20: Digital input actions - Dead Man Switch
test_nr = test_nr + 1
test_name = "Digital input actions - Dead Man Switch"
DINA_setting = 3 + 16 * Pars.kk
flag_triggered = "DEAD"
dina_result = DINA_test(DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count)
## ----------------------------------------------------------------------------------------------------------------------
# #Test 21: Digital input actions - FWD limit Switch
test_nr = test_nr + 1
test_name = "Digital input actions - FWD limit Switch"
DINA_setting = 4 + 16 * Pars.kk
flag_triggered = "FM_FwdLim"
dina_result = DINA_test(DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count)
# # ----------------------------------------------------------------------------------------------------------------------
# #Test 22: Digital input actions - REV limit Switch
test_nr = test_nr + 1
test_name = "Digital input actions - REV limit Switch"
DINA_setting = 5 + 16 * Pars.kk
flag_triggered = "FM_RevLim"
dina_result = DINA_test(DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count)
# # ----------------------------------------------------------------------------------------------------------------------'
# # #Test 23: Digital input actions - Inverse direction
test_nr = test_nr + 1
test_name = "Digital input actions - Inverse direction"
DINA_setting = 6 + 16 * Pars.kk
flag_triggered = "INV"
dina_result = DINA_test(DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count)
# ----------------------------------------------------------------------------------------------------------------------
# #Test 24: Digital input actions - Run Microbasic script
test_nr = test_nr + 1
test_name = "Digital input actions - Run Microbasic script"
DINA_setting = 7 + 16 * Pars.kk
flag_triggered = "FS_RunScript"
dina_result = DINA_test(DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count)
# # ----------------------------------------------------------------------------------------------------------------------
#Test 25: Digital input actions - Load  Counter with Home Value
test_nr = test_nr + 1
test_name = "Digital input actions - Load  Counter with Home Value"
DINA_setting = 8 + 16 * Pars.kk
flag_triggered = "HOME"
setconfig("BHOME",Pars.cc,Pars.home_count)
setconfig("SHOME",Pars.cc,Pars.home_count)
setconfig("EHOME",Pars.cc,Pars.home_count)
dina_result = DINA_test(DI_nr,DINA_setting,Pars.cc,flag_triggered,fail_counter,Pars.MC_test,Pars.home_count)
# # ----------------------------------------------------------------------------------------------------------------------'
## Test 26: Safety Stop - !SFT and EDEC ramp check"
test_nr = test_nr + 1
test_name = "Safety Stop via !sft - EDEC ramp check"
test_abrv = "RMP"#compute ramp based on Power drop
DI_count = 1
DINA_setting = 1 + 16 * Pars.kk
#time.sleep(Pars.t_wait_long)
sft_slope = compute_slope(test_abrv,Pars.cc,DI_count,DINA_setting)
print(sft_slope)
sft_FM_trig = getvalue("FM", Pars.cc)
sft_dict_trig = FM_read(sft_FM_trig)
if sft_dict_trig["FM_Safestop"] and sft_slope > Pars.EDEC_ramp_min and sft_slope < Pars.EDEC_ramp_max:
    print("Test " + str(test_nr) + " " + test_name +"."+ str(DI_count)+": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name +"."+ str(DI_count)+ ": - Fail \n \n")
    fail_counter += 1
setconfig("DINA", DI_count,0)#restore digital input action
setconfig("DINL", DI_count, 0)#restore  active level 0 --> DIN is low
setcommand("G", Pars.cc, 0)#restore test motor command
# ##----------------------------------------------------------------------------------------------------------------------'
# Test 27: Safety Stop - Dead Man Switch and EDEC ramp check"
test_nr = test_nr + 1
test_name = "Safety Stop via !sft - EDEC ramp check"
test_abrv = "RMP"#compute ramp based on Power drop
DI_count = 1
DINA_setting = 3 + 16 * Pars.kk #dead man switch
sft_slope = compute_slope(test_abrv,Pars.cc,DI_count,DINA_setting)
print(sft_slope)
sft_FM_trig = getvalue("FM", Pars.cc)
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
ATGA_result = amps_trigger_test(test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag)
# #----------------------------------------------------------------------------------------------------------------------'
# # Test 29 "Amps Trigger Actions - EM Stop"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - EM Stop"
test_abrv = "EMstop"#
FM_flag = "FM_FetsOff"
ATGA_setting = 2 + 16 * Pars.kk
ATGA_result = amps_trigger_test(test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag)
# #----------------------------------------------------------------------------------------------------------------------'
# # Test 30 "Amps Trigger Actions - Dead Man Stop"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Dead Man Stop"
test_abrv = "Dead"#
FM_flag = "FM_AmpTrig"
ATGA_setting = 3 + 16 * Pars.kk
ATGA_result = amps_trigger_test(test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag)
# #----------------------------------------------------------------------------------------------------------------------'
# # Test 31 "Amps Trigger Actions - FWD limit switch"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - FWD limit switch"
test_abrv = "FWD"#use this to trigger AmpsTrig
FM_flag = "FM_FwdLim"
ATGA_setting = 4 + 16 * Pars.kk
ATGA_result = amps_trigger_test(test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag)
# ##----------------------------------------------------------------------------------------------------------------------'
# # # Test 32 "Amps Trigger Actions - Rev limit switch"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Rev limit switch"
test_abrv = "REV"#use this to trigger AmpsTrig
FM_flag = "FM_RevLim"
ATGA_setting = 5 + 16 * Pars.kk
ATGA_result = amps_trigger_test(test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag)
# # ##----------------------------------------------------------------------------------------------------------------------'
# Test 33 "Amps Trigger Actions - Invert Direction"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Invert Direction"
test_abrv = "Inv"
FM_flag = "FM_AmpTrig"#not used here
ATGA_setting = 6 + 16 * Pars.kk
ATGA_result = amps_trigger_test(test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag)
# ##----------------------------------------------------------------------------------------------------------------------'
# Test 34 "Amps Trigger Actions - Run Script"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Run Script"
setcommandmaint("sld",Pars.key,":100000000201030E001F03E803230300002000FF8A:00000001FF")# script: wait forever
time.sleep(Pars.t_wait_mid)
setcommandmaint("sld",Pars.key,":100000000201030E001F03E803230300002000FF8A:00000001FF")# needed twice
time.sleep(Pars.t_wait_long)
test_abrv = "Script"
FM_flag = "FM_RevLim"#not used here
ATGA_setting = 7 + 16 * Pars.kk
ATGA_result = amps_trigger_test(test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag)
# # #----------------------------------------------------------------------------------------------------------------------'
# # Test 35 "Amps Trigger Actions - Load  Counter with Home Value"
test_nr = test_nr + 1
test_name = "Amps Trigger Actions - Load  Counter with Home Value"
test_abrv = "Home"
FM_flag = "FM_AmpTrig"
ATGA_setting = 8 + 16 * Pars.kk
setconfig("BHOME",Pars.cc,Pars.home_count)
setconfig("SHOME",Pars.cc,Pars.home_count)
setconfig("EHOME",Pars.cc,Pars.home_count)
ATGA_result = amps_trigger_test(test_abrv,Pars.cc,ATGA_setting,fail_counter,test_nr,Pars.MC_test,Pars.home_count,FM_flag)
# # # #----------------------------------------------------------------------------------------------------------------------'
## Test 36 "Telemetry"
# test_nr = test_nr + 1
test_name = "Telemetry"
test_abrv = "TELS"
test_vars = "\"?A:?V:?T:# 200\""
setconfig("SCRO",1)#1 = serial
setconfig(test_abrv,test_vars)
setcommandmaint("eesav")
time.sleep(Pars.t_wait_long)
setcommandmaint("reset",Pars.key)
print("Controller has been reboot via %reset")
ser.close()
time.sleep(Pars.t_wait_long)
ser.close()
time.sleep(Pars.t_wait_vlong)
#ser = serial.Serial(Pars.COM_port_2, Pars.COM_baudrate, timeout=Pars.COM_timeout)
#------------------------------------------------------------------------------------------
try:
    ser = establish_serial_connection(Pars.COM_port_2,Pars.COM_baudrate,Pars.COM_timeout)
    # Use serial_connection for further operations
except serial.SerialException as e:
    print(e)
print(ser)
# print(ser.is_open)
if ser.is_open == True:
    print("Controller found on specified Serial Port!")
else:
    print("Controller could not be found on specified Serial Port!")
if Pars.reset_defaults_flag == True:
    print("Perform reset to defaults ")
    setcommandmaint("eerst",Pars.key)
    print("Controller has been reset to defaults")
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
print("FINALE")
if tels_result == "Pass":
    print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
else:
    print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")

# time.sleep(Pars.t_wait_long)
# # # ----------------------------------------------------------------------------------------------------------------------'
# # # ----------------------------------------------------------------------------------------------------------------------'
# # Finale
# # ------------------------------------------------------------------------------------------------------------------------'
test_end_time = time.time()
test_duration = test_end_time-test_start_time
print("Number of tests completed" ,test_nr,"Number of failed tests:",fail_counter, ". Test_duration was: ",test_duration," secs.")
ser.close()
time.sleep(Pars.t_wait_long)
