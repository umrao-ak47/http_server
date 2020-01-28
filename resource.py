from os import path


class ResourseManager:
    def __init__(self, dir):
        self.__dir = dir
    
    def _create_header(self, http_ver, f_status, f_type):
        header = http_ver
        if f_status == 200:
            header += "200 OK\r\n"
        elif f_status == 404:
            header += "404 Not Found\r\n"
        f_cat = "text"
        images_type = ['png','jpg','jpeg','ico','bmp']
        if f_type in images_type:
            f_cat = "image"
        header += f"Content-Type: {f_cat}/{f_type}; charset: utf-8\r\n"
        header += "\r\n"
        header = header.encode('ascii')
        return header
    
    def _get_file(self, file_path):
        f_data = b""
        try:
            with open(file_path,'rb') as f:
                f_data = f.read()
            print(": Found")
        except FileNotFoundError:
            print(": Not Found")    
        return f_data


    def fetch(self, file_name, http_ver):
        if file_name == "":
            file_name = "index.html"
        if not '.' in file_name:
            file_name += ".html"
        _, f_type = file_name.split('.')
        file_path = path.join(self.__dir, file_name)
        data = self._get_file(file_path)
        f_status = 200
        if data == b"":
            f_status = 404
            f_type = "html"
            data = b"<h1>Page does not found</h1>"
        header = self._create_header(http_ver, f_status, f_type)
        return header+data
