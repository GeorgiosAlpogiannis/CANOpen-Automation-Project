# Import packages
import serial
import time
import Pars
# Define Functions
def wait(milliseconds):
    time.sleep(milliseconds / 1000)

def setcommand(ser,*args):
    cmd = "!" + " ".join(str(arg) for arg in args) + "\r"
    #print(cmd)
    ser.write(cmd.encode())

def setconfig(ser,*args):
    cmd = "^" + " ".join(str(arg) for arg in args) + "\r"
    ser.write(cmd.encode())


def setcommandmaint(ser,*args):
    cmd = "%" + " ".join(str(arg) for arg in args) + "\r"
    ser.write(cmd.encode())

def getvalue(ser,*args):
    start_time = time.time()
    # Wait for a response with a timeout
    reply_full = b""
    reply_value_mid = []
    get_config_cnt = 0
    while len(reply_value_mid) < 2:
        cmd = "?" + " ".join(str(arg) for arg in args) + "\r"
        cmd_int = args[0] + "="
        ser.write(cmd.encode())
        while (time.time() - start_time) < Pars.response_timeout:
            if ser.in_waiting > 0:
                reply_full = ser.readline()
                if reply_full != b"":
                    break
        reply_full = reply_full.replace(cmd.encode(), b'').strip()
        #print("reply_full is ",reply_full)
        reply_value_mid = reply_full.decode().split(cmd_int)
    reply_value_midd = reply_value_mid[1].split("\r",1)[0]
    #print("reply_value_mid",reply_value_mid,"reply_value_midd",reply_value_midd)
    get_config_cnt +=1
    reply_value = reply_value_midd #reply_value_mid[1]
    return reply_value

def getvaluespecial(ser,*args):
    #time.sleep(0.004)
    start_time = time.time()
    reply_full = b""
    reply_value_mid = []
    get_config_cnt = 0
    while len(reply_value_mid) < 2:
        cmd = "?" + " ".join(str(arg) for arg in args) + "\r"
        if args[0] == "CD":
            cmd_int = args[0]
        else:
            cmd_int = args[0] + "="
        ser.write(cmd.encode())
        ser.flushInput()  # needed after performing !stt (which returns data)
        # Wait for a response with a timeout
        while (time.time() - start_time) < Pars.response_timeout: #or reply_full == b"":
            if ser.in_waiting > 0:
                reply_full = ser.readline()
                if reply_full != b"":
                    break
        reply_full = reply_full.replace(cmd.encode(), b'').strip()
        #print("reply_full is", reply_full)
        reply_value_mid = reply_full.decode().split(cmd_int)
    reply_value = reply_value_mid[1]
    get_config_cnt +=1
    #print("get config reply_value is",reply_value,"get_config_cnt",get_config_cnt,"cmd_int",cmd_int)
    return reply_value

def getconfig(ser,*args):
    #time.sleep(0.004)
    start_time = time.time()
    reply_full = b""
    reply_value_mid = []
    get_config_cnt = 0
    while len(reply_value_mid) < 2:
        cmd = "~" + " ".join(str(arg) for arg in args) + "\r"
        cmd_int = args[0] + "="
        ser.write(cmd.encode())
        # Wait for a response with a timeout
        while (time.time() - start_time) < Pars.response_timeout:
            if ser.in_waiting > 0:
                reply_full = ser.readline()
                # break
                if reply_full != b"":
                    break
            #print("reply_full",reply_full,"get_config_cnt", get_config_cnt)
            get_config_cnt +=1
        reply_full = reply_full.replace(cmd.encode(), b'').strip()
        reply_value_mid = reply_full.decode().split(cmd_int)
    reply_value = reply_value_mid[1]
    get_config_cnt +=1
    print("get config reply_value is",reply_value,"get_config_cnt",get_config_cnt,"cmd_int",cmd_int)
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
def fault_flag_test(ser,test_name,FF_type,counts,fail_counter,test_setting,test_nr):
    ff_cnt_fails = 0
    for cnt in range(counts):
        init_setting = getconfig(ser,FF_type, cnt+1)  # write down default setting
        setconfig(ser,FF_type,cnt+1,test_setting)  # apply test setting
        if test_name != "FF_SED":
            time.sleep(Pars.t_wait_short)#sed takes longer to trigger
        else:
            time.sleep(Pars.t_wait_mid)#sed takes longer to trigger
        FF = getvalue(ser,"FF", 1)
        FF_dict = FF_read(FF)
        FM = getvalue(ser,"FM", Pars.cc)
        FM_dict = FM_read(FM)
        print("FF_dict",FF_dict,"FM_dict",FM_dict)
        if (FF_dict[test_name] and FM_dict["FM_FetsOff"]):
            print("Test " + str(test_nr) + "." + str(cnt) +" "+ test_name+": - Pass \n \n")
        else:
            print("Test " + str(test_nr) + "." + str(cnt) +" "+ test_name+": - Fail \n \n")
            ff_cnt_fails += 1
        DO_sum = int(getvalue(ser,"DO"))
        setconfig(ser,FF_type, cnt+1, init_setting)  # restore default setting
    if ff_cnt_fails == 0:
        print("Test " + str(test_nr) +" "+ test_name+": - Pass \n \n")
    else:
        print("Test " + str(test_nr) +" "+ test_name+": - Fail \n \n")
        fail_counter +=1
    return fail_counter,DO_sum
# perform a Fault Flag Type (no config) test
def fault_flag_test_no_config(ser,test_name,FF_type,counts,fail_counter,test_nr):
    setcommand(ser,FF_type,1)
    time.sleep(Pars.t_wait_short)
    FF = getvalue(ser,"FF", 1)
    FF_dict = FF_read(FF)
    FM = getvalue(ser,"FM", Pars.cc)
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
        fail_counter+=1
    return fail_counter

def calibration_test(ser,test_name,FF_type,counts,fail_counter,test_setting,test_nr):
    for cnt in range(counts):
        init_setting = getconfig(ser,FF_type)  # write down default setting
        # print(init_setting)
        setconfig(ser,FF_type,test_setting)  # apply test setting
        time.sleep(Pars.t_wait_long)
        setcommand(ser,"STT")
        time.sleep(Pars.t_wait_long)
        setcommand(ser,"STT")
        time.sleep(Pars.t_wait_long)
        FF = getvaluespecial(ser,"FF", 1)
        FF_dict = FF_read(FF)
        FM = getvaluespecial(ser,"FM", Pars.cc)
        FM_dict = FM_read(FM)
        #print(FF_dict)
        DO_sum = int(getvalue(ser,"DO"))
        print("DO is ",DO_sum)
        if (FF_dict[test_name] and FM_dict["FM_FetsOff"]):
            print("Test " + str(test_nr) + "." + str(cnt) +" "+ test_name+": - Pass \n \n")
            print("FAIL COUNTER IS ",fail_counter)
            fail_bool = 0
        else:
            print("Test " + str(test_nr) + "." + str(cnt) +" "+ test_name+": - Fail \n \n")
            fail_counter += 1
            fail_bool = 1
        setconfig(ser,FF_type,init_setting)  # restore default setting
        setcommand(ser,"STT")
    if fail_bool == 0:
        print("Test " + str(test_nr) +" "+ test_name+": - Pass \n \n")
        result = "Pass"
    else:
        print("Test " + str(test_nr) +" "+ test_name+": - Fail \n \n")
        fail_counter+=1
    return fail_counter
#--------------------------------------------------------------------
def var_read_write(ser,test_abrv,test_name,test_nr,fail_counter):
    var = getvalue(ser,test_abrv)
    var_length = round(len(var)/2)
    #print("var length is ",var_length)
    cnt_zero = 1
    cnt_one = 1
    sum_zero = 0
    sum_one = 0
    while cnt_zero <= var_length:
        setcommand(ser,test_abrv, cnt_zero, 0)  # set all  vars to zero
        zero = int(getvalue(ser,test_abrv,cnt_zero))
        sum_zero = sum_zero + zero
        cnt_zero += 1
    setcommand(ser,test_abrv, 0, 1)  # set all  vars to one
    while cnt_one <= var_length:
        setcommand(ser,test_abrv, cnt_one, 1)  # set all  vars to zero
        one = int(getvalue(ser,test_abrv,cnt_one))
        sum_one = sum_one + one
        cnt_one +=1
    setcommand(ser,test_abrv, 0, 0)#restore to default (logical zero)
    #print("sum_zero is:",sum_zero,"sum_one is:",sum_one)
    if sum_zero == 0 and sum_one == var_length:
        print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
        fail_counter += 1
    return fail_counter
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
def dout_actions_test(ser,test_abrv,dout_aa,DO_nr,test_setting,DO_sum_tot,fail_counter,test_nr,test_name):
    dout_cnt = 1
    # DO_sum = 0
    setconfig(ser,"RWD",0)
    setconfig(ser,"SED", 0, 0)  # disable SED
    setconfig(ser,"BLSTD", 0, 0)  # disable stall
    setcommand(ser,"G", 0, 0)  # Command zero
    while dout_cnt <= DO_nr:
        setconfig(ser,"DOA", dout_cnt, dout_aa)  # configure DOUT action
        dout_cnt+=1
    setcommand(ser,test_abrv, Pars.cc, test_setting)
    time.sleep(Pars.t_wait_long)#mid
    DO_sum = 0
    while DO_sum == 0:
        DO_sum = int(getvalue(ser,"DO"))
        time.sleep(Pars.t_wait_mid)
        print("NOT TRIGGERED YET")
    print("DO_sum is ", DO_sum,"DO_sum_tot",DO_sum_tot)
    if DO_sum == DO_sum_tot:
        print("Test " + str(test_nr) + " " + test_name + ": - Pass \n \n")
    else:
        print("Test " + str(test_nr) + " " + test_name + ": - Fail \n \n")
        fail_counter += 1
    setcommand(ser,test_abrv, Pars.cc, 0)#restore
    time.sleep(Pars.t_wait_mid)
    setconfig(ser,"SED", 0, 2)  # restore SED
    return fail_counter
# --------------------------------------------------------------------------------------------------------------------
# DINA Test function (DINA actions)
def DINA_test(ser,DI_nr,DINA_setting,cc,flag_triggered,fail_counter,MC_test,home_count,test_nr,test_name):
    DI_count = 1
    if Pars.motor_type != 3: #don't run for brushed DC
        setconfig(ser,"SED", 0, 0)
    setconfig(ser,"RWD",0)
    all_DINs_OK = True
    while DI_count <= DI_nr:
        setconfig(ser,"DINA", DI_count,DINA_setting)#select digital input action
        setconfig(ser,"DINL", DI_count, 0)#start with active level 0 --> DIN is low
        mid = getvalue(ser,"DI",DI_count)
        din_deact = int(mid)
        setcommand(ser,"G", cc, MC_test)  # restore settings
        print("din_deact",din_deact)
        time.sleep(Pars.t_wait_mid)# long, mid
        MC_mid_1 = getvalue(ser,"P", cc)
        print("MC_mid_1 is",MC_mid_1)
        MC_mid_2 = MC_mid_1.split(':')
        #MC_mid = MC_mid_2[cc-1]
        MC_mid = MC_mid_2[0]
        MC_init = int(MC_mid)
        setconfig(ser,"DINL", DI_count, 1)#trigger DIN action
        time.sleep(Pars.t_wait_mid)#mid
        sft_FM = getvalue(ser,"FM", cc)
        sft_dict = FM_read(sft_FM)
        din_act = int(getvalue(ser,"DI",DI_count))
        MC_after = int(getvalue(ser,"P",cc))
        print("MC_init is",MC_init,"MC_after is",MC_after)
        FS_script = getvalue(ser,"FS", 1)
        FS_dict_script = FS_read(FS_script)
        bs_counter = int(getvalue(ser,"CB",cc))
        enc_counter = int(getvalue(ser,"C",cc))
        ssi_counter = int(getvalue(ser,"CSS",cc))
        # print(bs_counter,enc_counter,ssi_counter)
        # restore settings
        setconfig(ser,"DINA", 0, 0)  # restore settings
        setconfig(ser,"DINL", 0, 0)  # restore settings
        setcommand(ser,"G", cc, 0)  # restore settings
        setcommand(ser,"R",0) # stop script , if running
        setcommand(ser,"CB", cc,0) # zero counters
        setcommand(ser,"C", cc,0)
        setcommand(ser,"CSS", cc,0)
        setcommand(ser,"EX", 1)  # clear sft flag
        time.sleep(Pars.t_wait_short)
        if flag_triggered == "FM_FetsOff": # used for dead man switch
             setcommand(ser,"MG", 1)  # clear sft flag
             time.sleep(Pars.t_wait_long)  # mid
        time.sleep(Pars.t_wait_mid)#mid
        sft_FM_cleared = getvalue(ser,"FM", cc)
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
            print("FS_dict_script",FS_dict_script)
        elif flag_triggered == "HOME":
            if bs_counter == enc_counter == ssi_counter == home_count:
                cond_flag = 1
            else:
                cond_flag = 0
        else:
            cond_flag = sft_dict[flag_triggered] and not sft_dict_cleared[flag_triggered]
        print("FS_dict_script",FS_dict_script,"cond_flag",cond_flag,"din_act",din_act,"din_deact",din_deact)
        if cond_flag and din_act == 1 and din_deact == 0:
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
    #setconfig(ser,"SED", 0, 2)
    return fail_counter
# ---------------------------------------------------------------------------------------------------------------------
# Raw Redirect
def convert_integers_to_string(*integers):
    # Step 1: Group the individual integers into a list
    integer_list = list(integers)
    # Step 2: Convert each integer to its ASCII character
    ascii_characters = [chr(num) for num in integer_list]
    # Step 3: Merge the ASCII characters into a single string
    result_string = ''.join(ascii_characters)
    return result_string
# ---------------------------------------------------------------------------------------------------------------------
# Compute slope (SFT , DEAD MAN etc)
def compute_slope(ser,test_abrv,cc,DI_count,DINA_setting,RWD_trigger):
    setconfig(ser,"RWD", 0)
    setconfig(ser,"BLSTD", 0,0)
    setconfig(ser,"G", cc,0)
    setcommand(ser,"MG",1)
    setconfig(ser,"SED", 0, 0)
    if RWD_trigger == False:
        setconfig(ser,"DINA", DI_count, DINA_setting)  # select digital input action
    else:
        setconfig(ser,"DINA", DI_count, 0)  # Triggered by RWD expiration instead of DINA.
    setconfig(ser,"EDEC", cc, Pars.EDEC_ramp_test)
    setconfig(ser,"DINL", DI_count, 0)  # start with active level 0 --> DIN is low
    setcommand(ser,"G", cc, Pars.MC_test)  # give test motor command
    time.sleep(Pars.t_wait_mid)#mid --> G4
    prev_val = int(getvalue(ser,test_abrv, cc))
    if RWD_trigger == False:
        setconfig(ser,"DINL", DI_count, 1)  # trigger DIN action
    else:
        setconfig(ser,"RWD", 1) #1ms
    print("prev_val",prev_val)
    prev_time = time.time()
    slope_cnt = 0
    slope_sum = 0
    while prev_val > 0:
        # Read new value and time
        new_val = int(getvalue(ser,test_abrv,cc))
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
def amps_trigger_test(ser,test_abrv,cc,ATGA_setting,fail_counter,test_nr,MC,home_count,FM_flag,test_name):
    time.sleep(Pars.t_wait_long)#mid
    # zpao_cc = 2*cc#ZPAO 2 -->cc1, ZPAO 4 --> cc2
    zpao_cc = cc#ZPAO 2 -->cc1, ZPAO 4 --> cc2 # Brushed DC
    setcommand(ser,"SED",0,0)
    setcommand(ser,"MG",1)
    setconfig(ser,"RWD",0)
    time.sleep(Pars.t_wait_mid)
    setcommand(ser,"G",cc,MC)
    time.sleep(Pars.t_wait_short) #
    P_act = int(getvalue(ser,"P",cc))
    ZPAO_test_setting = 0
    ZPAO_init = getconfig(ser,"ZPAO",zpao_cc)
    ZPAO_init_2 = getconfig(ser,"ZPAO",zpao_cc+1)
    setconfig(ser,"ATGA",cc,ATGA_setting)
    setconfig(ser,"ZPAO",zpao_cc,ZPAO_test_setting)#apply test_setting
    # print("wait 1 started")
    time.sleep(Pars.t_wait_long)#mid
    # print("wait 1 ended")
    setconfig(ser,"ZPAO",zpao_cc+1,ZPAO_test_setting)#apply test_setting # Remove this for brushed DC cc2
    # print("wait 2 started")
    time.sleep(Pars.t_wait_long)#mid
    # print("wait 2 ended")
    amps = int(getvalue(ser, "A", cc))
    ZPAO_1 = int(getconfig(ser, "ZPAO", zpao_cc))
    ZPAO_2 = int(getconfig(ser, "ZPAO", zpao_cc + 1))
    print(str(amps) + " Motor Amps  \n \n" + str(ZPAO_1) + " " + str(ZPAO_2) + "ZPAO 1,2 pre-actual \n \n")
    FM = getvalue(ser,"FM",cc)
    FS = getvalue(ser,"FS",1)
    ATGA_result = FM_read(FM)
    FS_result = FS_read(FS)
    P_deact = int(getvalue(ser,"P",cc))
    M_deact = int(getvalue(ser,"M",cc))
    bs_counter = int(getvalue(ser,"CB", cc))
    enc_counter = int(getvalue(ser,"C", cc))
    ssi_counter = int(getvalue(ser,"CSS", cc))
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
    setconfig(ser,"ATGA",cc,0)
    setcommand(ser,"SED",0,0)
    setconfig(ser,"ZPAO",zpao_cc,ZPAO_init)
    setconfig(ser,"ZPAO",zpao_cc+1,ZPAO_init_2)
    setcommand(ser,"R", 0)  # Stop script.
    setcommand(ser,"CB", cc, 0)  # zero counters
    setcommand(ser,"C", cc, 0)
    setcommand(ser,"CSS", cc, 0)
    setcommand(ser,"MG",1)
    time.sleep(Pars.t_wait_short)
    return fail_counter
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
#ser = serial.Serial(Pars.COM_port_USB,Pars.COM_baudrate,timeout = Pars.COM_timeout)
def Test_Functions_Main():
    try:
        ser = establish_serial_connection(Pars.COM_port_USB,Pars.COM_baudrate,Pars.COM_timeout)
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
    #Reboot via %reset
    print("START! \n")
    test_start_time = time.time()
    if Pars.reset_defaults_flag:
        print("Perform reset to defaults ")
        setcommandmaint(ser,"eerst", Pars.key)
        setcommandmaint(ser,"eerst", Pars.key)#needed twice
        print("Controller has been reset to defaults")
        time.sleep(Pars.t_wait_vlong)
    # Clear initial errors (SED, FETS OFF)
    FF = getvalue(ser, "FF", 1)
    FF_dict = FF_read(FF)
    if (FF_dict["FF_Estop"] or FF_dict["FF_SED"]):  # 'SED or / and Estop are active
        setconfig(ser,"SED", 0, 0)
        setcommand(ser,"MG", 1)
        print("Cleared initial SED error by disabling sensor error detection. \n \n")
    if Pars.reboot_flag:
        print("Perform reboot via %reset ")
        setcommandmaint(ser,"reset",Pars.key)
        print("Controller has been reboot via %reset")
        time.sleep(Pars.t_wait_long)
        ser.close()
        time.sleep(Pars.t_wait_long)
        try:
            ser = establish_serial_connection(Pars.COM_port_USB, Pars.COM_baudrate, Pars.COM_timeout)
            # Use serial_connection for further operations
        except serial.SerialException as e:
            print(e)
        print(ser)
        setconfig(ser,"BMOD", Pars.cc, 1) #sinusoidal mode
        setcommand(ser, "DS", 0)  # de-activate all DOUT's
    return ser