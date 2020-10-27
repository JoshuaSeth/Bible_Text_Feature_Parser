from plugins.plugin import Plugin, Setting


class CountWord(Plugin):
    def __init__(self):
        # Define your settings here
        self.settings = {"Words": Setting([], "Words you want to count in the text."), "Count Lexemes": Setting(
            True, "If the count should count exact words or lexemes of words."), "Only Sum Total": Setting(
            False, "If you want to count each word individually or the sum of these words in the text."), "Exact match": Setting(
            (True, False), "If you want to find exactly this word or want to find this word in another word or only want to find this word in another word and not as exat match"), "Save Verses": Setting(
            False, "If you want to save the verses, where the words were found.")}

        # Give a description for choosing this plugin
        self.description = "This plugin lets you select multiple words and will count their occurences in the text"

        self.name = "Word counter"

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
