

# code to plot time spent every day from data exported by forest app
# TODO: cleanup... oh dear.
# 	remove failed attempts from list

# instructions: export your .csv from app, run

import pandas as pd
import matplotlib.pyplot as plt
import datetime

filename = "test.csv"

# pandas magic:
kwargs = {
    "sep": ",", # specifices that it's a space separeted file
    "names": ["st", "et", "tag", "note", "type", "succ"], # names the columns
    "parse_dates": [0,1], # combine columns 2 and 3 into a datetime col
   # "index_col": "st", # set the datetime column as the index
    }


df = pd.read_csv(filename, **kwargs)

#df['delta'] = df['et'] - df['st']
#df['delta']=df['delta']/np.timedelta64(1,'D')

print(df)

print(df.dtypes)
#df = df["2017-02-17 23:02:31":"2017-02-17 23:02:51"]
# plot it using pandas built in wrapper for matplotlib.pyplot
#df[0].plot()
# show the plot
#plt.show()

# dates...
# https://stackoverflow.com/questions/17465045/can-pandas-automatically-recognize-dates

def conv(x):
	return datetime.datetime.strptime(x,'%a %b %d %H:%M:%S %Z%z %Y') 

def bconv(x):
	if x == "False":
		return False
	return True 

#....


start_ind = 2

st = list(df['st'])[start_ind:]
st = list(map(conv, st))
et = list(df['et'])[start_ind:]
et = list(map(conv, et))
succ = list(df['succ'])[start_ind:]
succ = list(map(bconv, succ))
#print(succ)
#print(et)

diff = []
for i in range(len(st)):
	diff.append(int((et[i]-st[i]).total_seconds()))
print(diff)
# .total_seconds()

def ind(x):
	return str(x.year)+'/'+str(x.month)+'/'+str(x.day)

star = ind(st[0])
keys = pd.date_range(end = pd.datetime.today(), start = star, freq='D').to_pydatetime().tolist()
print(keys)



dic = {}
for k in keys:
	dic[ind(k)] = 0


for i in range(len(st)):
	dic[ind(st[i])] = dic[ind(st[i])]+diff[i]

# to min
for k in dic.keys():
	dic[k] = int(dic[k]/60)

#print(list(dic.values()))

x = [datetime.datetime.strptime(d,'%Y/%m/%d').date() for d in dic.keys()]
y = list(dic.values())

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))

plt.plot(x,y)
plt.gcf().autofmt_xdate()

plt.axhline(y=360, color='r', linestyle='-')
plt.axhline(y=120, color='r', linestyle='-')

plt.show()








