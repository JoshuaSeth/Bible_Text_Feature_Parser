from plugins.plugin import Plugin, Setting
from divisions import Passage, Verse
import bible
import run_pane

class HapaxLegomena(Plugin):
    def __init__(self):
        # Define your settings here
        self.settings = {"Maximum Occurences": Setting(
            1, "How many times the word may occur in the given body."),"Lexemes": Setting(
            True, "If the count should count exact words or lexemes of words."), "Save Verses": Setting(
            False, "If you want to save the verses, where the words were found."), "Exclude Passage": Setting(
            False, "It may occur in this passage more than once, as long as it is a hapax to the other passages"), "Text Body": Setting(
            ["New Testament"], "The list of passages you want to check this is a hapax in. For the whole nt just enter 'NT'")}

        # Give a description for choosing this plugin
        self.description = "This plugin counts the number of hapax legomena"

        self.name = "Hapax Legomena counter"

        self.id = "hapax_legomena.HapaxLegomena"

        self.enabled = True

        #Register the run pane to access the progress bar
        for t in run_pane.RunPane.getinstances():
            self.active_run_pane = t

    def ScanPassages(self, passages, thread=None):
        # Set up a state
        self.state={}

        self.resources = {}

        self.state["Verses and words"] = [" "] * len(passages)

        #Determine if we search for words or lemma's
        col_name = "Greek_Word"
        if self.settings["Lexemes"].value == True:
            col_name = "Lexeme"

        #Add a column for each body that is searched in
        self.SetResources(passages)

        index = 0
        for passage in passages:
            #Get a list of the unique words in these passages
            #Either get the lexemes or the greek words
            if self.settings["Lexemes"].value == True:
                words = passage.Lexeme.unique()
            else:
                words = passage.Greek_Word.unique()
            
            #Now with all the words from the passage check if its a hapax
            for word in words:
                #For each body of text this has to be checked against
                for text_body, df in self.resources.items():
                    #Matching rows
                    matches = df[df[col_name] == word]
                    #occurences
                    num_occurences = matches.shape[0]
                    #If it is low enough 
                    if num_occurences <= self.settings["Maximum Occurences"].value:
                        #Then add to the hapaxes of this text Body
                        self.state["Hapax Legomena to "+ text_body][index]+=1
                        
                        #If we want to save the verse occurences
                        if self.settings["Save Verses"].value == True:
                            self.SaveVerse(matches, word, index, passage, col_name)
            index+=1
            #increase the progress bar
            thread.change_value.emit(self.active_run_pane.pbar.value() + len(passage))

        return self.state

    def SaveVerse(self, matches, word, index, passage, col_name):
        #If we want to save the verse occurences        
        #Save the matching verses
        matching_verses = []


        #Also get the verses from the original passage
        matches_orig_passage = passage[passage[col_name] == word]
        #Iterate over the verses that matches
        for row in matches_orig_passage.itertuples():
            #Make a verse for each row and save it's string
            verse_string = Verse(row=row).GetString()
            #Save to the verses list_val
            matching_verses.append(verse_string)

        #Iterate over the verses that matches
        for row in matches.itertuples():
            #Make a verse for each row and save it's string
            verse_string = Verse(row=row).GetString()
            #Save to the verses list_val
            matching_verses.append(verse_string)

        #Make a string from the word and the verses
        word_and_verses = word +": "
        #Add the verses to the word
        for verse_string in matching_verses:
            word_and_verses+= verse_string + ", "
        word_and_verses+ ". "
        #Save this to the cell
        self.state["Verses and words"][index] += word_and_verses

    def SetResources(self, passages):
        #Add a column for each body that is searched in
        for text_body in self.settings["Text Body"].value:
            #If the input is NT df = whole bible
            if text_body.lower() == "new testament" or text_body.lower() == "nt":
                df = bible.bible
            #If input is a passage get a passage and load a passage
            else:
                temp = Passage(text_body)
                df = bible.GetPassage(temp)
            #Save it as a resource
            self.resources[text_body] = df

            #The returned state will have a column for each text body it looks towards
            self.state["Hapax Legomena to " + text_body] = [0] * len(passages)
