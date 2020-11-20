from plugins.plugin import Plugin, Setting


class StrongsFeatures(Plugin):
    def __init__(self):
        # Define your settings here
        self.settings = {"Criteria: ": Setting(set(["Compound", "Latin origin", "Chaldee origin", "Hebrew origin", "Unknown origin", "Foreign origin"]), "The morphological criteria the word should adhere to."),
        "Save words: ": Setting(False, "If you want to save the words that match these criteria."),
        "Word: ":Setting("", "The morphological criteria should match a form of this lexeme. Leave empty to match criteria for any lexeme.")}

        # Give a description for choosing this plugin
        self.description = "This plugin lets you count with criteria as described by strongs. You can check for latin, Chaldee or other foreign origins from words or search for compound words."

        self.name = "Strongs features counter"

        self.id = "strong_features.StrongsFeatures"

        self.enabled = False


    # Is called when the scan starts
    def OnStartScan(self):
        # Set up a state
        self.state = {}

        # Fill the state with relevant counters
        for word in self.settings[0].value:
            self.state[word] = 0

    def ScanPassages(self, passages):
        root = ET.parse('strongsgreek.xml').getroot()
        
        #For every passage in the list of passages
        for df in passages:
            #If we are looking for a specific word select only the rows with this word
            if self.settings["Word"] != "":
                df = df[df[col_name] == word]
            
            for row in matches.itertuples():
                #Make a verse for each row and save it's string
                verse_string = Verse(row=row).GetString()
                #Save to the verses list_val
                matching_verses.append(verse_string)
        
