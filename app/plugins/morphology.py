from plugins.plugin import Plugin, Setting


class CountMorphology(Plugin):
    def __init__(self):
        # Define your settings here
        self.settings = {"Criteria: ": Setting(set(["male", "female"]), "The morphological criteria the word should adhere to."),
        "Save words: ": Setting(False, "If you want to save the words that match these criteria."),
        "Word: ":Setting("", "The morphological criteria should match a form of this lexeme. Leave empty to match criteria for any lexeme.")}

        # Give a description for choosing this plugin
        self.description = "This plugin lets you count words which match morphological criteria"

        self.name = "Morphological forms counter"

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
