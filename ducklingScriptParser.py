import sys
import event


class ScriptError(Exception):
    """
    Exception raised for errors in the duckling script.
    """
    pass


class ducklingScriptParser():
    #Split the timeString (mmss) from the EventString (xxx)
    """

    """

    def __init__(self):
        pass

    @staticmethod
    def splitEvent(strEvent):
        """

        @param strEvent:
        @return:
        """
        i = 0
        while strEvent[i].isdigit():
            i += 1
        return strEvent[0:i], strEvent[i:]


    #Returns the time
    @staticmethod
    def convertTime(timeStr):

        """

        @param timeStr:
        @return:
        """
        if len(timeStr) == 3:
            return int(timeStr[0]) * 60 + int(timeStr[1:3])
        elif len(timeStr) == 4:
            return int(timeStr[0:2]) * 60 + int(timeStr[2:4])

        raise ScriptError(f"Error in time of timeStr: {timeStr}")

    @staticmethod
    def strThreatToEventThreat(strThreat):
        """

        @param strThreat:
        @return:
        """
        if strThreat == 'T':
            return 'threat_normal'
        elif strThreat == 'ST':
            return 'threat_serious'
        elif strThreat == 'IT':
            return 'internal_normal'
        elif strThreat == 'SIT':
            return 'internal_serious'
        else:
            raise ScriptError(f"Unknown threat code: {strThreat}")

    @staticmethod
    def strZonetoEventZone(strZone):
        """

        @param strZone:
        @return:
        """
        if strZone == 'R':
            return 'zone_red'
        elif strZone == 'W':
            return 'zone_white'
        elif strZone == 'B':
            return 'zone_blue'
        else:
            raise ScriptError(f"Unknown zone code: {strZone}")

    def parseEventStr(self, eventStr):
        """

        @param eventStr:
        @return:
        """
        eventList = []
        (timeStr, eventStr) = self.splitEvent(eventStr)
        time = self.convertTime(timeStr)
        strType  = eventStr[0:2]
        strParams = eventStr[2:]

        if strType == "PE":
            eventList.append((time - 60, event.phaseEnds(int(strParams), '1min')))
            eventList.append((time - 20, event.phaseEnds(int(strParams), '20s')))
            eventList.append((time - 7, event.phaseEnds(int(strParams), 'now')))
        elif strType == "AL" or strType == "UR":
            unconfirmed = (strType == "UR")
            turn = int(strParams[0])
            
            # If it ends with a known zone code, separate it.
            # Known zones are R, W, B.
            if strParams.endswith(('R', 'W', 'B')):
                threat_code = strParams[1:-1]
                zone_code = strParams[-1]
                threat = self.strThreatToEventThreat(threat_code)
                zone = self.strZonetoEventZone(zone_code)
            else:
                threat_code = strParams[1:]
                threat = self.strThreatToEventThreat(threat_code)
                zone = None
            
            eventList.append((time, event.alert(turn, threat, zone, unconfirmed)))
        elif strType == "ID":
            eventList.append((time, event.incomingData()))
        elif strType == "DT":
            eventList.append((time, event.dataTransfer()))
        elif strType == "CS":
            eventList.append((time, event.communicationSystemsDown(int(strParams))))
        else:
            raise ScriptError(f"Unknown event type in script: {strType}")

        #return the events
        return eventList

    def convertScript(self, script):
        """

        @param script:
        @return:
        """
        lijst = script.split(',')

        eventList = [(0, event.start())]
        for eventStr in lijst:
            events = self.parseEventStr(eventStr)
            eventList.extend(events)

        #Replace the last phase ends with mission ends
        lastEvent = eventList[-1][1]
        if isinstance(lastEvent,event.phaseEnds):
            lastPhaseNumber = lastEvent.getPhaseNumber()
            for time, eventItem in eventList:
                if isinstance(eventItem, event.phaseEnds):
                    if eventItem.getPhaseNumber() == lastPhaseNumber:
                        eventItem.convertToEndMission()

        else:
            raise ScriptError("The last event is not a phase end!")


        return eventList
