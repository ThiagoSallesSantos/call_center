import cmd
import json

class Commands(cmd.Cmd):

    ## Commands Methods
    def do_call(self, id):
        if id:
            return self._modelResponse('call', id)
        print('\n' + 'command invalid, the id parameter was not passed.' + '\n')
        
    def do_answer(self, id):
        if id:
            return self._modelResponse('answer', id)
        print('\n' + 'command invalid, the id parameter was not passed.' + '\n')
        
    def do_reject(self, id):
        if id:
            return self._modelResponse('reject', id)
        print('\n' + 'command invalid, the id parameter was not passed.' + '\n')
    
    def do_hangup(self, id):
        if id:
            return self._modelResponse('hangup', id)
        print('\n' + 'command invalid, the id parameter was not passed.' + '\n')
    
    ## Helpers Methods
    def help_call(self):
        print('\n' + 'call <id>' + '\n' + 'makes application receive a call whose id is <id>.' + '\n')
        
    def help_answer(self):
        print('\n' + 'answer <id>' + '\n' + 'makes operator <id> answer a call being delivered to it.' + '\n')
        
    def help_reject(self):
        print('\n' + 'reject <id>' + '\n' + 'makes operator <id> reject a call being delivered to it.' + '\n')
        
    def help_hangup(self):
        print('\n' + 'hangup <id>' + '\n' + 'makes call whose id is <id> be finished.' + '\n')
    
    ## Utilies Methods
    def default(self, line):
        print('\n' + 'command invalid "' + str(line) + '", use the help command to see the list of commands.' + '\n')
        
    def _modelResponse(self, command, id):
        return json.dumps({'command': str(command), 'id': str(id)})
