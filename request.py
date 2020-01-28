class RequestParser:
    def __init__(self):
        self.__req = None
        self.__content = None
    
    def get_request(self):
        return self.__req
    
    def get_content(self):
        return self.__content
    
    def parse(self, data):
        try:
            data = data.split('\r\n')
            request = data[0]
            req = request.split(' ')
            self.__req = {'type': req[0],'path': req[1][1:],'http-ver':req[2]}
            data.pop(0)
            content = {}
            for x in data:
                field, *val = x.split(':')
                val = ':'.join(val)
                content[field] = val
            self.__content = content
        except Exception as err:
            self.__req = None
            self.__content = None
            print("Could not parse data from request")
            print("Error: ",err)
        