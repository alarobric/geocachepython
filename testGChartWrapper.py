# -*- coding: utf-8 -*-

from GChartWrapper import GChart

print "Hello"
dataset = (1, 2, 3)
dataset2 = [[1,1],[2,2],[3,10],[5,4]]
G = GChart('p3', dataset, encoding='text').label('1', '2', '3').color('00dd00')
G = GChart('lxy', dataset2, encoding='text', chds='0,11').label('1', '2', '3', '4').color('00dd00')
G.axes.type('xy')

print str(G)
G.show()
