books = {40: "Matthew", 41: "Mark", 42: "Luke", 43: "John", 44:"Acts"}

def GetBookNr(name):
    for key, val in books.items():
        if val==name:
            return key
    return None