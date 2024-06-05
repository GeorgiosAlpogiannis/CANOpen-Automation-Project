#-----------------------------------------------------------------------------------------------------------------------
#General Declarations
#I/O#s
FW_type = 2 #(1 = F3 (2.1a), 2 = G4 (3.0), 3 = F3 (2.2))
motor_type = 3 # (1 = BLDC, 2 = Induction, 3 = Brushed DC, 4 = Sensorless)
soft_STO = 0 # set to 1 in case controller has soft STO.
DO_nr = 4## of digital outputs
pow_a = 4# binary
AI_nr = 8## of analog inputs
PI_nr = 8
DI_nr = 10## of digital inputs
#wait times
t_wait_vlong = 9#s
t_wait_long = 3#s
t_wait_long2 = 5#s
t_wait_mid_low = 0.1
t_wait_mid = 1#s
t_wait_short = 0.02#s
t_wait_vshort = 0.005#s
t_wait_vvshort= 0.003#s
t_wait_mid_bef = 0.75*t_wait_mid
t_wait_mid_aft = 0.5*t_wait_mid# so that we are with +/-25%
bool_vars_nr = 65## of boolean vars
ff_nr = 6# # of fault flags tested
DINA_nr = 7 ## of DIN actions tested
DOA_nr = 7# # of DO actions tested
MC_test = 500 # test Motor Command value
EDEC_ramp_test = MC_test# so that ramp down completes after 1sec
EDEC_ramp_tolerance = 0.05*EDEC_ramp_test
EDEC_ramp_min = (EDEC_ramp_test-EDEC_ramp_tolerance)/10 # /10 convert to RPM/s
EDEC_ramp_max = (EDEC_ramp_test+EDEC_ramp_tolerance)/10
fail_count = 0# # of failed tests
acc_low = 1000#set acceleration to 100 RPM/s
acc_mid = 10000#set acceleration to 1000 RPM/s
acc_high = 50000#set acceleration to 5000 RPM/s
user_vars = 5
MC_max = 1000#max motor command
MC_test_mid = 200#motor command
freq_bound_high = 1050#Hz, use for PMOD 2
freq_bound_low = 995#Hz, use for PMOD 2
cc = 1 # channel
if cc == 3:
	kk = 4 # used when cc =3
else:
	kk = cc # used when cc =3
cc_gain_1 = 0+cc # used for PID gain channel selection
cc_gain_2 = 2+cc
gain_check = 50000#test value for PID gains
ratio_lim_low = 95# tolerance in %, when comparing values
ratio_lim_high = 105# tolerance in %, when comparing values
#----------------------------------------------------------------------------------------------------------
#Motor/Sensor Data
Max_RPM = 1000
#Equivalent circuit parameters
Rs = 117# phase resistance [mOhm]
Ld = 250# d-axis inductance [uH]
Lq = 250# q-axis inductance [uH]
#Pole Pair Settings
pp_hall_enc = 5#pole pairs
pp_sincos = 5
pp_resolver = 3#resolver motor under test has 3 pole pairs.all others have 5.
pp_SSI = 5
#PPR/CPR Settings
enc_ppr = 4096#encoder ppr
SSI_ppr = 4096
sin_cos_cpr = 512
int_sens_count_max = 500#max counts, internal sensor
int_sens_count_min = -int_sens_count_max
enc_count_max = 15000
enc_count_min = -enc_count_max
#VPM counts hall
hall_vpm_counts_1rev = pp_hall_enc*6#hall sensor counts for 1 mech rev
hall_vpm_count_tolerance = 2#counts
hall_vpm_counts_max = hall_vpm_counts_1rev + hall_vpm_count_tolerance
hall_vpm_counts_min = hall_vpm_counts_1rev - hall_vpm_count_tolerance
#VPM counts encoder
enc_vpm_counts_1rev = 4*enc_ppr
enc_vpm_count_tolerance = 4#counts
enc_vpm_counts_max = enc_vpm_counts_1rev + enc_vpm_count_tolerance
enc_vpm_counts_min = enc_vpm_counts_1rev - enc_vpm_count_tolerance
#VPM counts encoder
sincos_vpm_counts_1rev = sin_cos_cpr
sincos_vpm_count_tolerance = 4#counts
sincos_vpm_counts_max = sincos_vpm_counts_1rev + sincos_vpm_count_tolerance
sincos_vpm_counts_min = sincos_vpm_counts_1rev - sincos_vpm_count_tolerance
#VPM counts resolver
Resolver_vpm_counts_1rev = sin_cos_cpr
Resolver_vpm_count_tolerance = 4#counts
Resolver_vpm_counts_max = Resolver_vpm_counts_1rev + Resolver_vpm_count_tolerance
Resolver_vpm_counts_min = Resolver_vpm_counts_1rev - Resolver_vpm_count_tolerance
#VPM counts SSI
SSI_vpm_counts_1rev = SSI_ppr
SSI_vpm_count_tolerance = 100#counts
SSI_vpm_counts_max = SSI_vpm_counts_1rev + SSI_vpm_count_tolerance
SSI_vpm_counts_min = SSI_vpm_counts_1rev - SSI_vpm_count_tolerance
#ASI counts tolerance
ASI_vpm_count_tolerance = SSI_vpm_count_tolerance#counts
ASI_vpm_counts_max = SSI_vpm_counts_1rev + ASI_vpm_count_tolerance
ASI_vpm_counts_min = SSI_vpm_counts_1rev - ASI_vpm_count_tolerance
#---------------------------------------------------------------------------------------------------------
#Motor thermistor settings
r25 = 60000
b25 = -750
motor_temp_expected = 105#deg C
motor_temp_tolerance = 15#deg C
motor_temp_max = motor_temp_expected + motor_temp_tolerance
motor_temp_min = motor_temp_expected - motor_temp_tolerance
# ---------------------------------------------------------------------------------------------------------
overheat_lim_test = -5 #deg C
overvolt_lim_test = 0 #V*10
undervolt_lim_test = 500 #V*10
sed_value_test = 2# tolerant / strict
ZSRM_value_test = 500#to trigger mosfail
ZSRM_typical = 60000#mV
ZSRM_tolerance = 0.05#*100%
ZSRM_min_threshold = (1-ZSRM_tolerance)*ZSRM_typical
ZSRM_max_threshold = (1+ZSRM_tolerance)*ZSRM_typical
key = 321654987
home_count = 50#
reboot_flag = True
reset_defaults_flag = True
LED_iters = 10
#---------------------------------------------------------------------------------------------------------
#Memory Retention tests
Config_Retention_Object = "OVL"
Calib_Retention_Object = "ZPAC"
Backup_Register_Object = "BEE"
Backup_Time_Object = "TM"
Config_retention_check = 590#volts*10
Calib_retention_check = 666#ZPAC
Backup_Register_check = 7#dummy
Battery_included = True
#---------------------------------------------------------------------------------------------------------
#Serial Communication Tests
COM_port_USB = 'COM3'
COM_port_serial = 'COM15'# RS232 port, used e.g. for telemetry
COM_timeout = 0.05#s
COM_baudrate = 115200#115200
response_timeout = 10# sec, used in Getvalue, GetConfig
echo_cmd = "?Var" + "\r"
SCRO_test_print = "hello"
baud_rate_test = 4#corresponding to 9600
baud_rate_test_Mbs = 9600
Raw_Redirect_Write_Test = "123"
Raw_Redirect_Read_Test = "?FID" + "\r"
ASCII_conversion_read = [ord(char) for char in Raw_Redirect_Read_Test]
ASCII_conversion_write = [ord(char) for char in Raw_Redirect_Write_Test]
print("ASCII_conversion_read",ASCII_conversion_read,"ASCII_conversion_write",ASCII_conversion_write[0],ASCII_conversion_write[1],ASCII_conversion_write[2],type(ASCII_conversion_write[0]))
#-----------------------------------------------------------------------------------------------------------------------
#ID related
if FW_type == 2:
	UID_MCU_device_ID = 1129 #FBLG2xx, SBLMG2xx
	UID_MCU_type = 400
	FID_fw_version = "Roboteq v3."
else:
	UID_MCU_device_ID = 1058 #FBL2xx
	UID_MCU_type = 301
	FID_fw_version = "Roboteq v2."
Controller_Type = "FIMG2XXX"#"" SBLMG2XXX
Controller_Characters = 5 # nr of characters used in controller's name. Use for ?TRN check
UID_Unique_ID_pt1 = 7
UID_Unique_ID_pt2 = 10
UID_Unique_ID_pt3 = 9
FID_date = "05/17/2024" #MM:DD:YY