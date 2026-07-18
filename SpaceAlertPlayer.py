#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8, <3.14"
# dependencies = ["pygame"]
# ///

import time
from collections import deque
from threading import Thread
from ducklingScriptParser import ducklingScriptParser
from keypress import KeyReader
import threads

def main():
    #load all chapters and missions
    """


    @return:
    """
    from missionList import missionList
    missionList = missionList()

    #run the menu to make a selection from the available missions
    from SpaceAlertMenu import SpaceAlertMenu
    menu = SpaceAlertMenu(missionList)
    chapter, mission = menu.main()

    if chapter is None and mission is None:
        return False
    else:
        script = missionList.getScript(chapter, mission)
        runGame(script)
        return True

def waitOrAbort(keys, until):
    """Wait until `until`, returning True if 'q' was pressed in the meantime.

    @param keys:
    @param until:
    @return:
    """
    while time.time() < until:
        if keys.key() == 'q':
            return True
        # go easy on the CPU:
        time.sleep(.1)
    return False

def runGame(script):

    # Initilaize the audio, display, and communiquation queu:
    """

    @param script:
    """
    audioQ = deque([])
    displayQ = deque([])
    threadCommunicationQ = deque ([])

    #parse the duckling script
    eventList = ducklingScriptParser().convertScript(script)

    # Start the game NOW:
    startTime = time.time()

    # Spawn the audio thread:
    audioThread = Thread(target=threads.AudioThread, args=(audioQ,threadCommunicationQ), daemon=True)

    # Spawn the display thread:
    displayThread = Thread(target=threads.DisplayThread, args=(displayQ, startTime,threadCommunicationQ), daemon=True)

    aborted = False
    with KeyReader() as keys:
        audioThread.start()
        displayThread.start()

        for timeEvent, event in eventList:
            # Wait for the next event, unless the cadet bails out first.
            if waitOrAbort(keys, startTime + timeEvent):
                threadCommunicationQ.append('ABORT')
                aborted = True
                break

            # Add the que's to the event and run the event
            event.setQs(audioQ, displayQ)
            event.execute()

        if not aborted:
            #Give the mp3s 20 seconds to finish playing
            # Also allow aborting during this wait
            if waitOrAbort(keys, time.time() + 20):
                threadCommunicationQ.append('ABORT')

    #Signal the Thread to end, and wait for it.
    threadCommunicationQ.append('AUDIO-STOP')
    threadCommunicationQ.append('DISPLAY-STOP')
    audioThread.join()
    displayThread.join()

if __name__ == "__main__":
    #play the main until it quits
    play = True
    while play:
        play = main()

    print("Byebye space cadet!")
