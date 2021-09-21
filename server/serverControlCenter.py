from serverCall import Call
from serverOperator import Operator
import json
import time

class ControlCenter:

    def __init__(self):
        self._list_operators = self._createOperators()
        self._list_calls_queue = []
        self._list_news_calls = []
        self._online_calls = {}
    
    def _createOperators(self):
        list_operators = []
        operator1 = Operator('A')
        operator2 = Operator('B')
        list_operators.append(operator1)
        list_operators.append(operator2)
        return list_operators
    
    def manageCallsQueue(self):
        operator_available = self._findOperatorAvailable()
        if (self._list_calls_queue != []) and (operator_available is not False):
            call = self._list_calls_queue.pop(0)
            self._online_calls.update({operator_available : call})
            return self._sendResponse(str('Call ' + str(call.getId()) + ' ringing for operator ' + str(operator_available.getId())))
        if self._list_news_calls != []:
            call = self._list_news_calls.pop(0)
            if operator_available is not False:
                self._online_calls.update({operator_available : call})
                return self._sendResponse(str('Call ' + str(call.getId()) + ' ringing for operator ' + str(operator_available.getId())))
            else:
                self._list_calls_queue.append(call)
                return self._sendResponse(str('Call ' + str(call.getId()) + ' waiting in queue'))

    def manageCommands(self, command):
    
        ####Call Command
        if command['command'] == 'call':
            return self._executeCallCommand(command['id'])
        
        ####Answer Command       
        elif command['command'] == 'answer':
            return self._executeAnswerCommand(command['id'])
        
        ####Reject Command 
        elif command['command'] == 'reject':
            return self._executeRejectCommand(command['id'])
            
        ####Hangup Command     
        elif command['command'] == 'hangup':
            return self._executeHangupCommand(command['id'])
        
        else:
            return self._sendResponse(str('Invalid command'))
    
    def _executeCallCommand(self, id):
        if self._findCall(id) is not False:
            return self._sendResponse(str('Invalid id call'))
        new_call = Call(id)
        self._list_news_calls.append(new_call)
        return self._sendResponse(str('Call ' + str(new_call.getId()) + ' received'))
        
    def _executeAnswerCommand(self, id):
        operator = self._findOperatorResponsible(id)
        if operator is False:
            return self._sendResponse(str('Invalid operator'))
        self._online_calls[operator].callComplete()
        return self._sendResponse(str('Call ' + str(self._online_calls[operator].getId()) + ' answered by operator ' + str(operator.getId())))
        
    def _executeRejectCommand(self, id):
        operator = self._findOperatorResponsible(id)
        if operator is False:
            return self._sendResponse(str('Invalid operator'))
        call_reject = self._online_calls.pop(operator)
        self._list_calls_queue.append(call_reject)
        return self._sendResponse(str('Call ' + str(call_reject.getId()) + ' rejected by operator ' + str(operator.getId())))
    
    def _executeHangupCommand(self, id):
        call = self._findCall(id)
        if call is False:
            return self._sendResponse(str('Invalid id call'))
        if call in list(self._online_calls.values()):
            operator = self._findOperatorByCall(call)
            self._online_calls.pop(operator)
        elif call in self._list_calls_queue:
            self._list_calls_queue.pop(self._list_calls_queue.index(call))
        else:
            self._list_news_calls.pop(self._list_news_calls.index(call))
        if call.getComplete() is True:
            return self._sendResponse(str('Call ' + str(call.getId()) + ' finished and operator ' + str(operator.getId()) + ' available'))
        return self._sendResponse(str('Call ' + str(call.getId()) + ' missed'))

    def _findOperatorAvailable(self):
        operator_available = list(filter(lambda operator: operator not in list(self._online_calls.keys()), self._list_operators))
        if operator_available != []:
            return operator_available[0]
        return False

    def _findOperatorByCall(self, value):
        position = list(self._online_calls.values()).index(value)
        return list(self._online_calls.keys())[position]
    
    def _findOperatorResponsible(self, id):
        operator_responsible = list(filter(lambda operator: operator.getId() == id, list(self._online_calls.keys())))
        if operator_responsible != []:
            return operator_responsible[0]
        return False
        
    def _findCall(self, id):
        response = list(filter(lambda call: call.getId() == id, list(self._online_calls.values())))
        if response != []:
            return response[0]
        response = list(filter(lambda call: call.getId() == id, list(self._list_calls_queue)))
        if response != []:
            return response[0]
        response = list(filter(lambda call: call.getId() == id, list(self._list_news_calls)))
        if response != []:
            return response[0]
        return False
    
    def _sendResponse(self, response):
        return json.dumps({'response': str(response)})