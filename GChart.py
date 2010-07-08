# -*- coding: utf-8 -*-
import webbrowser
import logging

log = logging.getLogger('geocachepython.GChart')

class GChart:
    '''Class GChart
    Allows easy creation of google chart urls, and viewing of these charts.
    '''
    
    options = {}
    base = ''
    
    def __init__(self, base='http://chart.apis.google.com/chart?'):
        self.options = {}
        self.base = base
        pass
    
    def __str__(self):
        return self.url()
    
    def url(self):
        link = self.base
        for option in self.options.items():
            link = link + option[0] + "=" + option[1] + "&"
        link = link[:-1]
        return link
    
    def addOpt(self, option):
        if isinstance(option, dict):
            self.options.update(option)
        elif isinstance(option, list):
            if len(option) % 2 != 0:
                log.error("Wrong number of arguments")
                raise Exception("Wrong number of arguments")
            pairs = [(option[i], option[i+1]) for i in xrange(0,len(option)-1,2)]
            self.options.update(dict(pairs))
    def view(self):
        webbrowser.open(self.url())
        
    def type(self, type):
        if type == "Line":
            self.addOpt({'cht':'l'})
        

#webbrowser.open('http://chart.apis.google.com/chart?cht=lxy&chs=250x150&chd=t:1,2,3,5|1,2,10,4&chds=1,5,1,11&chxt=x,y&chxs=0,ff0000,12,0,lt|1,0000ff,10,1,lt&chxr=0,1,5,1|1,1,11&chf=c,lg,90,FFE7C6,0,76A4FB,1&chm=B,76A4FB,0,0,0')

'''
cht=lxy
chs=250x150
chd=t:1,2,3,5|1,2,10,4
chds=1,5,1,11
chxt=x,y
chxs=0,ff0000,12,0,lt
     1,0000ff,10,1,lt
chxr=0,1,5,1|1,1,11
chf=c,lg,90,FFE7C6,0,76A4FB,1
chm=B,76A4FB,0,0,0
'''

# Check if running as a program
if __name__ == '__main__':
     print "Run Debug Suite"
else:
     # No, I must have been imported as a module
     pass
