from twisted.internet import protocol, reactor
import json
import random,sys

class JsonRpcWrapper:
    def __init__(self,obj,flt=[]):
        self.__object = obj
        self.__filter = flt

    def __render(self,response):
        pass

    # --> { "method": "echo", "params": ["Hello JSON-RPC"], "id": 1}
    # <-- { "result": "Hello JSON-RPC", "error": null, "id": 1}
    def process(self,request):
        jdata={}
        rval = {"result": None,
                    "error":None,
                    "id":None}
        try:
            jdata = json.loads(request)
            rval["id"] = jdata["id"]
        except Exception as strerror:
            rval['error']=strerror.__str__()

        try:
            if 'method' not in jdata:
                raise Exception("No method found.  Invalid request.")

            method = jdata['method']
            params = jdata['params']

#            if not hasattr(self.__object,method):
#                raise Exception("Method '" + method + "' not found!")
            if len(self.__filter) > 0:
                if method not in self.__filter:
                    raise Exception("Method '" + method + "' not found! ONE ONE ONE")

            realMethod = getattr(self.__object,method)
            rawrval = realMethod(*params)
            rval["result"]=rawrval
        except Exception as strerror:
            rval['error']=strerror.__str__()

        return json.dumps(rval) + "\n"

class JsonRpcWrapperProtocol(protocol.Protocol):
    def __init__(self,obj,flt=[]):
        self.__wrapper = JsonRpcWrapper(obj,flt)

    def dataReceived(self,data):
        self.transport.write(self.__wrapper.process(data))


class JsonRpcWrapperFactory(protocol.Factory):
    def __init__(self,obj,flt=[]):
        self.__server = obj
        self.__flt = flt
    def buildProtocol(self,addr):
        return JsonRpcWrapperProtocol(self.__server,self.__flt)

#This is mostly a stub.  Returns a JSON object for a function call
class JsonClientWrapper(object):
    def __init__(self,classy=None):
        super(JsonClientWrapper, self).__init__()
        self.__obj = classy #who knows
        self.__id = 0
        self.wrapped = sys.modules[__name__]

    def __getid(self):
        self.__id += 1
        return self.__id

    def __getattr__(self,name):
        def f(*args):
            rval = {
                "method":name,
                "params":list(args),
                "id":self.__getid()
                    }
            return rval
      #  setattr(self,self.wrapped_name,f)
        return f

#foo = JsonClientWrapper()
#print foo.__getid()
#print foo.thisisatest()
#print foo.bar(1,2,3)
