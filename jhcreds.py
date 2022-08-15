# This exists just to hold the credentials for the various Twitter accounts

class twtraccount:

    alllines = []

    def __init__(self, line, linename, handle, id, access_key, access_secret):
        self.line = line
        self.linename = linename
        self.handle = handle
        self.id = id
        self.access_key = access_key
        self.access_secret = access_secret
        twtraccount.alllines.append(line)

bakerloo = twtraccount('bakerloo','Bakerloo','bakerloolinebot','1452706506995081220','REMOVED','REMOVED')
central = twtraccount('central','Central','centrallinebot','1450834060629135361','REMOVED','REMOVED')
circle = twtraccount('circle','Circle','circlelinebot','1452729144983408645','REMOVED','REMOVED')
district = twtraccount('district','District','districtlinebot','1452730040316272655','REMOVED','REMOVED')
hammersmithcity = twtraccount('hammersmithcity','Hammersmith & City','hamcitylinebot','1452731443424251905','REMOVED','REMOVED')
jubilee = twtraccount('jubilee','Jubilee','jubileelinebot','1452736217221640196','REMOVED','REMOVED')
metropolitan = twtraccount('metropolitan','Metropolitan','metropolitanbot','1453018304201822209','REMOVED','REMOVED')
northern = twtraccount('northern','Northern','northernlinebot','1453019223651983365','REMOVED','REMOVED')
piccadilly = twtraccount('piccadilly','Piccadilly','piccadillybot','1453019955067293701','REMOVED','REMOVED')
victoria = twtraccount('victoria','Victoria','victorialinebot','1453020626348818448','REMOVED','REMOVED')
waterloocity = twtraccount('waterloocity','Waterloo & City','waterloocitybot','1453098021915348998','REMOVED','REMOVED')

dlr = twtraccount('dlr','DLR','DLR_bot','1462046071924875271','REMOVED','REMOVED')
londonoverground = twtraccount('londonoverground','Overground','overground_bot','1461406075522060292','REMOVED','REMOVED')
tram = twtraccount('tram','Tram','LondonTramBot','1462055498765774855','REMOVED','REMOVED')
elizabeth = twtraccount('elizabeth','Elizabeth','ElizabethLn_bot','1462047954131374087','REMOVED','REMOVED')

tflapp_key = 'REMOVED'

consumer_key = 'REMOVED'
consumer_secret = 'REMOVED'

raspimessengerconsumer_key = "REMOVED"
raspimessengerconsumer_secret = "REMOVED"
raspimessengeraccess_key = 'REMOVED'
raspimessengeraccess_secret = 'REMOVED'