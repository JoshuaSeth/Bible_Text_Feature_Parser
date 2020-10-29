from plugins.plugin import Plugin, Setting
from divisions import Verse

class CountWord(Plugin):
    def __init__(self):
        # Define your settings here
        self.settings = {"Search Terms: ": Setting([], "Words you want to count in the text."), "Count Lexemes": Setting(
            True, "If the count should count exact words or lexemes of words."), "Only Sum Total": Setting(
            False, "If you want to count each word individually or the sum of these words in the text."), "Exact Match": Setting(
            True, "If you want to find exactly this word or want to find this word in another word."), "Save Verses": Setting(
            False, "If you want to save the verses, where the words were found.")}

        # Give a description for choosing this plugin
        self.description = "This plugin lets you select multiple words and will count their occurences in the text"

        self.name = "Word counter"

        

    def ScanPassages(self, passages_df_list):
        #Needs to have any assignment for code curther
        total_col_header ="-"

        # Set up a state
        #The state will save the results so for every item a column
        self.state = {}

        #If we want to count each word separately
        if self.settings["Only Sum Total"].value == False:
            # Fill the state with relevant counters
            for word in self.settings["Search Terms: "].value:
                self.state[word] = [0] * len(passages_df_list)
        #If we just want the Total
        else:
            #Make a string with the first and last word
            first_word = self.settings["Search Terms: "].value[0]
            last_word  = self.settings["Search Terms: "].value[len(self.settings["Search Terms: "].value)-1]
            total_col_header = "Total (" + first_word + "..." + last_word + ")"

            #Give the state only this word
            self.state[total_col_header] = [0] * len(passages_df_list)
        
        #If we want to save where it was found
        if self.settings["Save Verses"].value == True:
            #Add another column where this is saved to the state
            self.state["Verses and words"] = [" "] * len(passages_df_list)

        #Determine if we search for words or lemma's
        col_name = "Greek Word"
        if self.settings["Count Lexemes"].value == True:
            col_name = "Lexeme"

        index = 0
        #Check in each passage df
        for df in passages_df_list:
            #For each search term
            for word in self.settings["Search Terms: "].value: 
                #If this is not the verse tracking column and not the totals column
                if word != "Verses and words" and word != total_col_header:
                    #If we want exactl matches
                    if self.settings["Exact Match"].value == True:
                        #Get The occurences of this word in the passage
                        matches = df[df[col_name] == word]
                    #If it only needs to contain
                    else:
                        #Get it when it is in the coluumn
                        matches = df[df[col_name].str.contains(word)]
                    
                    #Count the number of matches
                    num_word_in_col = matches.shape[0]

                    #If counting each word
                    if self.settings["Only Sum Total"].value == False:
                        #Save this to the state at the passage index
                        self.state[word][index] = num_word_in_col 
                    #If counting Total
                    if self.settings["Only Sum Total"].value == True:
                        #Add this to the total for the passage
                        print(self.state[total_col_header][index], num_word_in_col)
                        self.state[total_col_header][index] += num_word_in_col
                    
                    #If we want to save the verse occurences
                    if self.settings["Save Verses"].value == True:
                        #Save the matching verses
                        matching_verses = []
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
            index+=1

        return self.state
        

        

        
    
