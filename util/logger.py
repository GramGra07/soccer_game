from Python.pyGame.soccer.trackers.trackers import Tracker


def log(text):
    print(text)
    with open(Tracker.fileName, "a") as f:
        f.write(text + "\n")