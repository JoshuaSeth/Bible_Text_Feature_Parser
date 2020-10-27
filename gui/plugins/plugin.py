class Plugin:
    def __init__(self):
        self.settings = []
        self.name = ""
        self.description = ""
     
    def Note(self, state):
        pass

    def OnStartScan(self):
        # Set up a state
        self.state = {}

class Setting:
    def __init__(self, value, tooltip):
        self.tooltip = tooltip
        self.value = value