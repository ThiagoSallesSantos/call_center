class Call:

    def __init__(self, id):
        self._id = id
        self._complete = False
        
    def callComplete(self):
        self._complete = True
        
    def getId(self):
        return self._id
        
    def getComplete(self):
        return self._complete
        