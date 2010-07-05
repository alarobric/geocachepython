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

'''
a5e8b5 Alberni–Clayoquot Regional District (Port Alberni)
730ce7 Regional District of Bulkley–Nechako (Burns Lake)
b5a5e8 Capital Regional District (Victoria)
0cb6e7 Cariboo Regional District (Williams Lake)
e8c9a5 Central Coast Regional District (Bella Coola)
c0e70c Regional District of Central Kootenay (Nelson)
e7b60c Regional District of Central Okanagan (Kelowna)
0ce7d5 Columbia–Shuswap Regional District (Salmon Arm)
ba6060 Comox Valley Regional District (Courtenay)
a5e6e8 Cowichan Valley Regional District (Duncan)
0ce71b Regional District of East Kootenay (Cranbrook)
e8a5a9 Fraser Valley Regional District (Chilliwack)
0c88e7 Regional District of Fraser – Fort George (Prince George)
dba5e8 Metro Vancouver (Greater Vancouver Regional District) (Burnaby)
ac0ce7 Regional District of Kitimat–Stikine (Terrace)
e7820c Regional District of Kootenay Boundary (Trail)
d4e8a5 Regional District of Mount Waddington (Port McNeill)
a5e8cf Regional District of Nanaimo (Nanaimo)
e7e40c Regional District of North Okanagan (Coldstream)
e70cb1 Northern Rockies Regional District (Fort Nelson)
e7540c Regional District of Okanagan–Similkameen (Penticton)
d50ce7 Peace River Regional District (Dawson Creek)
e8dea5 Powell River Regional District (Powell River)
0ce797 Skeena – Queen Charlotte Regional District (Prince Rupert)
e8a5d4 Squamish–Lillooet Regional District (Pemberton)
e70c2b Stikine Region (n/a)
b3e8a5 Strathcona Regional District (Campbell River)
e8c3a5 Sunshine Coast Regional District (Sechelt)
0cdfe7 Thompson–Nicola Regional District (Kamloops)
'''