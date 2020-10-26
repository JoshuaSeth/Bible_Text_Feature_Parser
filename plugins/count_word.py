from plugin import Plugin, Setting


class CountWord:
    def __init__(self, Plugin):
        # Define your settings here
        self.settings = {"Words": Setting([], "Words you want to count in the text"), "Lexemes": Setting(
            True, "If the count should count exact words or lexemes of words")}
        
        #Give a description for choosing this plugin
        self.description = "This plugin lets you select multiple words and will count their occurences in the text"

    # Is called when the scan starts
    def OnStartScan(self):
        # Set up a state
        self.state = {}

        # Fill the state with relevant counters
        for word in self.settings[0].value:
            self.state[word] = 0

    def Note(self, input):
        # Get the greek word
        word = input["Greek Word"]

        # If we are coutning lexemes make it the lexeme
        if self.settings[1].value == True:
            word = input["Lexeme"]

        # IF we are counting this word add to the counter
        if word in self.state:
            self.state[word] += 1
