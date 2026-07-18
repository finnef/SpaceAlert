import os

_baseDir = os.path.dirname(os.path.realpath(__file__))


class Settings:
    """
    Class that contains all the variables to the mp3's and messages. Allows for easy swtchint between language's and fixing of typo's
    """

    def __init__(self):
        pass

    soundsDir = os.path.join(_baseDir, 'sounds') + os.sep

    sound = {}
    messg = {}

    # Siren
    sound['siren0'] = 'red_alert_0.mp3'
    sound['siren1'] = 'red_alert_1.mp3'
    sound['siren2'] = 'red_alert_2.mp3'
    sound['siren3'] = 'red_alert_3.mp3'

    #Alerts
    sound['alert'] = 'alert.mp3'
    messg['alert'] = 'Alert'

    # Note the %s is the number of the phase (i.e. 1 to 8)
    sound['time_t'] = 'time_t_plus_%s.mp3'
    messg['time_t'] = 'time t+%s'

    sound['threat_normal'] = 'threat.mp3'
    messg['threat_normal'] = 'incoming threat'
    sound['threat_serious'] = 'serious_threat.mp3'
    messg['threat_serious'] = 'incoming serious threat'
    sound['internal_normal'] = 'internal_threat.mp3'
    messg['internal_normal'] = 'internal threat'
    sound['internal_serious'] = 'serious_internal_threat.mp3'
    messg['internal_serious'] = 'serious internal threat'

    sound['zone_blue'] = 'zone_Blue.mp3'
    messg['zone_blue'] = 'zone blue'
    sound['zone_red'] = 'zone_Red.mp3'
    messg['zone_red'] = 'zone red'
    sound['zone_white'] = 'zone_White.mp3'
    messg['zone_white'] = 'zone white'

    sound['repeat'] = 'repeat.mp3'
    messg['repeat'] = 'I repeat:'

    # Phase Events
    sound['begin'] = 'begin_first_phase.mp3'
    messg['begin'] = 'Alert! Enemy activity detected. Please begin first phase.'

    sound['phase_1_ends_in_1min'] = 'first_phase_ends_in_1_minute.mp3'
    messg['phase_1_ends_in_1min'] = 'First phase will ends in 1 minute!'
    sound['phase_1_ends_in_20s'] = 'first_phase_ends_in_20_seconds.mp3'
    messg['phase_1_ends_in_20s'] = 'First phase will end in 20 seconds!'
    sound['phase_1_ends_in_now'] = 'first_phase_ends.mp3'
    messg['phase_1_ends_in_now'] = 'First phase will end!'
    messg['phase_1_has_ended'] = 'First phase has ended!'

    sound['phase_2_ends_in_1min'] = 'second_phase_ends_in_1_minute.mp3'
    messg['phase_2_ends_in_1min'] = 'Second phase will ends in 1 minute!'
    sound['phase_2_ends_in_20s'] = 'second_phase_ends_in_20_seconds.mp3'
    messg['phase_2_ends_in_20s'] = 'Second phase will end in 20 seconds!'
    sound['phase_2_ends_in_now'] = 'second_phase_ends.mp3'
    messg['phase_2_ends_in_now'] = 'Second phase will end!'
    messg['phase_2_has_ended'] = 'Second phase has ended!'

    sound['begin_second_phase'] = 'second_phase_begins.mp3'
    messg['begin_second_phase'] = 'Please begin second phase!'

    sound['begin_third_phase'] = 'third_phase_begins.mp3'
    messg['begin_third_phase'] = 'Please begin the third phase!'

    #Operation ends
    sound['operation_ends_in_1min'] = 'operation_ends_in_1_minute.mp3'
    messg['operation_ends_in_1min'] = 'Operation will ends in 1 minute!'
    sound['operation_ends_in_20s'] = 'operation_ends_in_20_seconds.mp3'
    messg['operation_ends_in_20s'] = 'Operation will end in 20 seconds!'
    sound['operation_ends_in_now'] = 'operation_ends.mp3'
    messg['operation_ends_in_now'] = 'Operation will End!'
    messg['operation_has_ended'] = 'Operation has ended!'

    #Unconfirmed report
    sound['UR'] = 'unconfirmed_report.mp3'
    messg['UR'] = 'Unconfirmed report!'

    #Incoming Data
    sound['incoming_data'] = 'incoming_data.mp3'
    messg['incoming_data'] = 'Incoming data!'

    #Data Transfer
    sound['data_transfer'] = 'data_transfer.mp3'
    messg['data_transfer'] = 'Data transfer!'

    sound['communication_systems_down'] = 'communications_down.mp3'
    messg['communication_systems_down'] = 'Communications down!'
    sound['noise'] = 'white_noise.mp3'

    sound['communication_systems_restored'] = 'communications_restored.mp3'
    messg['communication_systems_restored'] = 'Communications restored!'
