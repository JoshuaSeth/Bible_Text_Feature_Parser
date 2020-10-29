from plugins.plugin import Plugin, Setting


class HapaxLegomena(Plugin):
    def __init__(self):
        # Define your settings here
        self.settings = {"Count Lexemes": Setting(
            True, "If the count should count exact words or lexemes of words."), "Only Sum Total": Setting(
            False, "If you want to count each word individually or the sum of these words in the text."), "Save Verses": Setting(
            False, "If you want to save the verses, where the words were found."), "Save Hapaxes": Setting(
            False, "If you want to save the specific hapax legomena that were found."), "Exclude passage": Setting(
            False, "It may occur in this passage more than once, as long as it is a hapax to the other passages"), "Text Body": Setting(
            ["New Testament"], "The list of passages you want to check this is a hapax in. For the whole nt just enter 'NT'")}

        # Give a description for choosing this plugin
        self.description = "This plugin counts the number of hapax legomena"

        self.name = "Hapax Legomena counter"

    # Is called when the scan starts
    def OnStartScan(self):
        # Set up a state
        self.state = {}

        # Fill the state with relevant counters
        for word in self.settings[0].value:
            self.state[word] = 0

    def ScanPassages(self, row):
        print(self.name, "has noted ", row)

        # # Get the greek word
        # word = input["Greek Word"]

        # # If we are coutning lexemes make it the lexeme
        # if self.settings[1].value == True:
        #     word = input["Lexeme"]

        # # IF we are counting this word add to the counter
        # if word in self.state:
        #     self.state[word] += 1
