class alert():
    def __init__(self, topic, constraint, state):
        self.topic = topic
        self.constraint = constraint
        self.state = state

    def getTopic(self):
        return self.topic

    def getConstraint(self):
        return self.constraint

    def getState(self):
        return self.state

    def setState(self, st):
        self.state = st

    def updateConstraint(self, con):
        self.constraint = con