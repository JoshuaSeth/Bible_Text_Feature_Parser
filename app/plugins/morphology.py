from plugins.plugin import Plugin, Setting
import pandas as pd
from divisions import Verse


class CountMorphology(Plugin):
    def __init__(self):
        # Define your settings here
        self.settings = {"Criteria: ": Setting(set(["Feminine", "Masculine", "Adjective", "Accusative", "Plural", "Singular", "Neuter", "Numerical Indiclinable", "Neuter", "Comparative", "Superlative", "Person Gentilic", "Location Gentilic", "Negative", "Location", "Dative", "Genitive", "Nominative", "Vocative", "Adverb", "Contracted Form", "Interrogative", "Conditional Particle", "Reciprocal Pronoun", "Conjunction", "Conjunctive Particle", "Demonstrative Pronoun", "Reflexive Pronoun", "First", "Second", "Third", "Accusative", "Interrogative Pronoun", "Correlative Pronoun", "Noun", "Title", "Person", "Personal Pronoun", "Preposition", "Particle", "Disjunctive Particle", "Correlative or Interrogative Pronoun", "Relative Pronoun", "Possessive Pronoun", "Definite Article", "Verb", "Second Aorist", "Active", "Passive", "Indicative", "Imperative", "Optative", "Participle", "Subjunctive", "Middle Deponent", "Middle", "Passive Deponent", "Infinitive", "No Voice Stated", "Second Future", "Second Pluperfect", "Second Present", "Second Perfect", "Aorist", "Future", "Imperfect", "Attic Form", "Pluperfect", "Present", "Perfect", "No Tense Stated", "Indefinite Pronoun"]), "The morphological criteria the word should adhere to."),
        "Save Words: ": Setting(False, "If you want to save the words that match these criteria."),
        "Word: ":Setting("", "The morphological criteria should match a form of this lexeme. Leave empty to match criteria for any lexeme.")}

        # Give a description for choosing this plugin
        self.description = "This plugin lets you count words which match morphological criteria"

        self.name = "Morphological forms counter"

        self.id = "morphology.CountMorphology"
        
        self.enabled = True

        #Load the mappings
        self.mappings = pd.read_csv("data/rmac.tsv", sep="\t")
        self.mappings = pd.Series(self.mappings.Description.values,index=self.mappings.RMAC).to_dict()


    # Is called when the scan starts
    def OnStartScan(self):
        pass

        

    def ScanPassages(self, passages, thread=None):
        # Set up a state
        self.state = {}

        # Fill the state with relevant counters
        self.state["Total"] = [0] * len(passages)

        #If saving words and verses
        if self.settings["Save Words: "].value == True:
            self.state["Morphology Verses and Words"]= [" "] * len(passages)

        #For each passage
        index = 0
        for df in passages:
            #Each word
            for id, row in df.iterrows():
                #Assume a match until counterevidence
                match = True
                rmac = row["RMac"]
                for criteria in self.ui.cbb.GetContent():
                    #Get contents from the optional dropdown
                    if not criteria.lower() in self.mappings[rmac].lower():
                        match = False

                #If we have a match!
                if match:
                    self.state["Total"][index] += 1
                
                    #If we save the locations
                    if self.settings["Save Words: "].value == True:
                        #Make a verse and add the word to it
                        verse_string = Verse(row=row).GetString() + ":" + row["Greek_Word"] + ", "
                        #Add it to the state
                        self.state["Morphology Verses and Words"][index]+= verse_string
                #increase the progress bar
                thread.change_value.emit(1)


            #Track
            index+=1
        return self.state

