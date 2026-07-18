try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser


class missionList():

    """

    """

    def __init__(self):
        self.chapter = {}
        #TODO
        #Scan for all cfg files in the mission dir
        #TMP solution, should be replaced with all .cfg files from 'mission' dir.
        missionConfigs = ['duckling.cfg', 'LittleDuckling.cfg']

        for configFile in missionConfigs:
            self.parseConfigFile('missions/'+configFile)

        #TODO: CHECK IF ALL MISSIONS ARE PLAYBLE.

    def parseConfigFile(self, configFile):
        """

        @param configFile:
        """
        chapter = {}
        config = ConfigParser.RawConfigParser()
        config.read(configFile)

        for section in config.sections():
            options = config.options(section)
            mission = {}
            for option in options:
                mission[option] = config.get(section, option)

            chapter[section] = mission

        self.chapter.update(chapter)

    def getChapters(self):
        """


        @return:
        """
        chapterList = []
        for chapter, missions in self.chapter.items():
            chapterList.append(chapter)

        chapterList.sort()
        return chapterList

    def getMissions(self, chapter):
        """

        @param chapter:
        @return:
        """
        missions = []
        for mission, missionScript in self.chapter[chapter].items():
            missions.append(mission)

        missions.sort()
        return missions

    def getScript(self, chapter, mission):
        """

        @param chapter:
        @param mission:
        @return:
        """
        return self.chapter[chapter][mission]
