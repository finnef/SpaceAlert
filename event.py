from settings import Settings
#
#
## event masterClass
class event(object):
    """

    """
    settingsTag = None

    def __init__(self):
        pass

    def setQs(self, audioQ, displayQ):
        """

        @param audioQ:
        @param displayQ:
        """
        self.audioQ = audioQ
        self.displayQ = displayQ

    # The standard implementation is to queue the sound and message in the
    # settings.
    def execute(self):
        """


        @raise NotImplementedError:
        """
        if self.settingsTag is None:
            raise NotImplementedError("Settings tag is not implemented")
        else:
            self.audioQ.append( (Settings.sound[self.settingsTag], -1, None) )
            self.displayQ.append ( (Settings.messg[self.settingsTag], None) )

class start(event):
    settingsTag = 'begin'

class phaseEnds(event):
    """

    @param phaseNumber:
    @param warning:
    """

    def __init__(self, phaseNumber, warning):
        super(phaseEnds, self).__init__()
        self.warning = warning
        self.phaseNumber = phaseNumber
        self.settingsTag = 'phase_' + str(phaseNumber) + '_ends_in_' + warning
        self.missionEnds = False

    def getPhaseNumber(self):
        """


        @return:
        """
        return self.phaseNumber

    def convertToEndMission(self):
        """


        """
        import re
        self.settingsTag = re.sub(r'phase_[0-9]_', "operation_", self.settingsTag)
        self.missionEnds = True

    def execute(self):
        """


        """
        if self.warning == 'now':
           self.audioQ.append( (Settings.sound[self.settingsTag], -1, self.executeHasEnded) )
           self.displayQ.append ( (Settings.messg[self.settingsTag], None) )
        else:
            self.audioQ.append( (Settings.sound[self.settingsTag], -1, None) )
            self.displayQ.append ( (Settings.messg[self.settingsTag], None) )

    def executeHasEnded(self):
        """


        """
        import re
        self.settingsTag = re.sub(r'ends_in_now', "has_ended", self.settingsTag)
        self.displayQ.append ( (Settings.messg[self.settingsTag], None) )

        #If it wasn't the mission that was ending, start the next phase:
        if self.missionEnds != True:
            if self.phaseNumber  == 1:
                tag = 'begin_second_phase'
            else:
                tag = 'begin_third_phase'

            self.audioQ.append( (Settings.sound[tag], -1, None) )
            self.displayQ.append ( (Settings.messg[tag], None) )

class alert(event):

    # use: threat = 'threat_normal', 'threat_serious', 'internal_normal', 'internal_serious'
    # zone = 'zone_blue', 'zone_red', 'zone_white'
    """

    @param turn:
    @param threat:
    @param zone:
    @param unconfirmed:
    """

    def __init__(self, turn, threat, zone, unconfirmed=False):
        super(alert, self).__init__()
        self.turn = turn
        self.threat = threat
        self.zone = zone
        self.unconfirmed = unconfirmed

    def createMessg(self):
        """

        @return:
        """
        if self.unconfirmed:
            messg = Settings.messg['UR']
        else:
            messg = Settings.messg['alert']

        messg += ' - '
        messg = messg + Settings.messg['time_t'] % self.turn
        messg += ' - '
        messg = messg + Settings.messg[self.threat]
        if self.zone:
            messg += ' - '
            messg = messg + Settings.messg[self.zone]
        return messg

    def execute(self):
        """


        """
        self.displayQ.append( (self.createMessg(), None))
        
        if self.unconfirmed:
            alert_sound = Settings.sound['UR']
        else:
            alert_sound = Settings.sound['alert']

        audio_list = [
            (alert_sound, -1, None),
            (Settings.sound['time_t'] % self.turn, -1, None),
            (Settings.sound[self.threat], -1, None)
        ]
        
        if self.zone:
            audio_list.append((Settings.sound[self.zone], -1, self.executeRepeat))
        else:
            # If no zone, attach the repeat callback to the threat sound
            last_sound = audio_list.pop()
            audio_list.append((last_sound[0], last_sound[1], self.executeRepeat))
            
        self.audioQ.extend(audio_list)

    def executeRepeat(self):
        """


        """
        # Do not print repeat alerts, only play the audio
        
        audio_list = [
            (Settings.sound['repeat'], -1, None),
            (Settings.sound['time_t'] % self.turn, -1, None),
            (Settings.sound[self.threat], -1, None)
        ]
        
        if self.zone:
            audio_list.append((Settings.sound[self.zone], -1, None))
            
        self.audioQ.extend(audio_list)


class incomingData(event):
    settingsTag = 'incoming_data'

class dataTransfer(event):
    settingsTag = 'data_transfer'

class communicationSystemsDown(event):
    """

    @param noiseDuration:
    """

    def __init__(self, noiseDuration):
        super(communicationSystemsDown, self).__init__()
        self.noiseDuration = noiseDuration

    def execute(self):
        """


        """
        self.audioQ.append((Settings.sound['communication_systems_down'], -1, self.execute2))
        self.displayQ.append((Settings.messg['communication_systems_down'], None))

    def execute2(self):
        """


        """
        self.audioQ.append((Settings.sound['noise'], self.noiseDuration, self.execute3))

    def execute3(self):
        """


        """
        self.audioQ.append((Settings.sound['communication_systems_restored'], -1, None))
        self.displayQ.append((Settings.messg['communication_systems_restored'], None))
