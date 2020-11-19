class Plugin:
    def __init__(self):
        self.settings = []
        self.name = ""
        self.description = ""
        self.ui = None
        self.enabled = False
     
    def Note(self, state):
        pass

    def OnStartScan(self):
        # Set up a state
        self.state = {}

class Setting:
    def __init__(self, value, tooltip):
        self.tooltip = tooltip
        self.value = value

    #This function presuposses this setting is a list
    def OnListValChange(self, input_list):
        self.value = input_list.GetContents()
    
    def Tick(self):
        self.value = not self.value
        print(self.value)

    def OnIntChanged(self):
        print(self, self.value)
        self.value = self.ui.value()