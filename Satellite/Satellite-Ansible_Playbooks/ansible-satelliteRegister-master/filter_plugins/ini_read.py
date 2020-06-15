from configparser import ConfigParser
import StringIO

class FilterModule(object):
    ''' A filter to read ini formated vars '''
    def filters(self):
        return {
            'ini_read': ini_read
        }

def ini_read(content, section, parameter):
    buf = StringIO.StringIO(content)
    config = ConfigParser()
    config.readfp(buf)
    return config.get(section,parameter)
