from plugins.plugin import Plugin, Setting


class CountWord(Plugin):
    def __init__(self):
        # Define your settings here
        self.settings = {"Search Terms: ": Setting([], "Words you want to count in the text."), "Count Lexemes": Setting(
            True, "If the count should count exact words or lexemes of words."), "Only Sum Total": Setting(
            False, "If you want to count each word individually or the sum of these words in the text."), "Exact match": Setting(
            (True, False), "If you want to find exactly this word or want to find this word in another word or only want to find this word in another word and not as exat match"), "Save Verses": Setting(
            False, "If you want to save the verses, where the words were found.")}

        # Give a description for choosing this plugin
        self.description = "This plugin lets you select multiple words and will count their occurences in the text"

        self.name = "Word counter"

        # Set up a state
        #The state will save the results so for every item a column
        self.state = {}

    def ScanPassages(self, passages_df_list):
        # Fill the state with relevant counters
        for word in self.settings["Search Terms: "].value:
            self.state[word] = [0] * len(passages_df_list)

        #Determine if we search for words or lemma's
        col_name = "Greek Word"
        if self.settings["Count Lexemes"].value == True:
            print('counting lexeemes')
            col_name = "Lexeme"

        #For each search term
        for word, list_val in self.state.items():
            #Check in each passage df
            index = 0
            for df in passages_df_list:
                #Count the amount of occurences of this word in the passage
                num_word_in_col = df[df[col_name] == word].shape[0]

                print(num_word_in_col)

                #Save this to the state at the passage index
                self.state[word][index] = num_word_in_col 

                index+=1

        print(self.state)

        return self.state
        

        

        
    
