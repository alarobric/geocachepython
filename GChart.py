# -*- coding: utf-8 -*-
import webbrowser

class GChart:
    '''Class GChart
    Allows easy creation of google chart urls, and viewing of these charts.
    '''
    
    options = {}
    
    def __init__(self):
        self.options = {}
        pass
    
    def __str__(self):
        return self.url()
    
    def url(self):
        link = "http://chart.apis.google.com/chart?"
        for option in self.options.items():
            link = link + option[0] + "=" + option[1] + "&"
        link = link[:-1]
        return link
    
    def addOpt(self, option):
        if isinstance(option, dict):
            self.options.update(option)
        elif isinstance(option, list):
            if len(option) % 2 != 0:
                raise Exception("Wrong number of arguments")
            pairs = [(option[i], option[i+1]) for i in xrange(0,len(option)-1,2)]
            self.options.update(dict(pairs))
    def view(self):
        webbrowser.open(self.url())
        
    def type(self, type):
        if type == "Line":
            self.addOpt({'cht':'l'})
        

#webbrowser.open('http://chart.apis.google.com/chart?cht=lxy&chs=250x150&chd=t:1,2,3,5|1,2,10,4&chds=1,5,1,11&chxt=x,y&chxs=0,ff0000,12,0,lt|1,0000ff,10,1,lt&chxr=0,1,5,1|1,1,11&chf=c,lg,90,FFE7C6,0,76A4FB,1&chm=B,76A4FB,0,0,0')

g=GChart()
args = ['cht', 'lxy']
g.addOpt(args)
args = {'chs':'250x150', 'chxt':'x,y', 'chf':'c,lg,90,FFE7C6,0,76A4FB,1', 'chm':'B,76A4FB,0,0,0'}
g.addOpt(args)
args = ['chd', 't:1,2,3,5|1,2,10,4', 'chxr', '0,1,5|1,1,11', 'chds', '1,5,1,11']
g.addOpt(args)
print g
g.view()

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
