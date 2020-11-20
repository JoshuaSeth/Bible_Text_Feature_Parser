class Plugin:
    def __init__(self):
        self.settings = []
        self.name = ""
        self.description = ""
        self.ui = None
        self.enabled = False
        self.id = ""

    def OnStartScan(self):
        # Set up a state
        self.state = {}
    
    def GetAsDict(self):
        l = [self.name, [], self.description, self.enabled, self.id]
        for key, setting in self.settings.items():
            l[1].append(setting.value)
        return l


class Setting:
    def __init__(self, value, tooltip):
        self.tooltip = tooltip
        self.value = value

    #This function presuposses this setting is a list
    def OnListValChange(self, input_list):
        self.value = input_list.GetContents()
        print(self.value)
    
    def Tick(self):
        self.value = not self.value
        print(self.value)

    def OnIntChanged(self):
        print(self, self.value)
        self.value = self.ui.value()