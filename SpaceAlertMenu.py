from ducklingScriptParser import ducklingScriptParser


class SpaceAlertMenu():

    """

    @param missionList:
    """

    def __init__(self, missionList):
        self.missionList = missionList

    def subMenu(self, menuItems, menuText):
        """

        @param menuItems:
        @param menuText:
        @return:
        """
        i = 1
        formatted_items = []
        for option in menuItems:
            formatted_items.append(str(i) + ") " + option)
            i += 1

        if formatted_items:
            max_width = max(len(item) for item in formatted_items) + 2
            num_cols = max(1, 80 // max_width)
            num_cols = min(num_cols, 3)  # Max 3 columns for better readability

            num_rows = (len(formatted_items) + num_cols - 1) // num_cols

            for r in range(num_rows):
                line = ""
                for c in range(num_cols):
                    index = r + c * num_rows
                    if index < len(formatted_items):
                        line += formatted_items[index].ljust(max_width)
                menuText += line + "\n"

        menuText += "0) Back"
        while True:
            print(menuText)
            selection = input("Make your choice: ")
            if selection.isdigit():
                selection = int(selection)
                if selection == 0:
                    return
                elif 0 < selection < i:
                    return menuItems[selection - 1]

            self.noAction()

    def selectChapter(self):
        """


        @return:
        """
        menuText = "Select a chapter to play:\n"
        menuOptions = self.missionList.getChapters()
        chapter = self.subMenu(menuOptions, menuText)
        return chapter

    def selectMission(self, chapter):
        """

        @param chapter:
        @return:
        """
        menuText = "Select a mission to play:\n"
        missions = self.missionList.getMissions(chapter)
        
        displayOptions = []
        for m in missions:
            try:
                script = self.missionList.getScript(chapter, m)
                lastEventStr = script.split(',')[-1]
                timeStr, _ = ducklingScriptParser.splitEvent(lastEventStr)
                totalSeconds = ducklingScriptParser.convertTime(timeStr)
                duration = "%02d:%02d" % (totalSeconds // 60, totalSeconds % 60)
                displayOptions.append(f"{m} ({duration})")
            except:
                displayOptions.append(m)
            
        selection = self.subMenu(displayOptions, menuText)
        if selection:
            index = displayOptions.index(selection)
            return missions[index]
        return None

    @staticmethod
    def noAction():
        """


        """
        print('Say what Cadette?')

    def main(self):

        """


        @return:
        """
        mainMenuText = "\n Main Menu.\n (s)elect chapter\n (q)uit"

        while True:
            print(mainMenuText)
            selection = input("Your selection: ")
            if selection == "q":
                return None, None
            elif selection == "s":
                chapter = self.selectChapter()
                if chapter is not None:
                    mission = self.selectMission(chapter)
                    if mission is not None:
                        return chapter, mission
