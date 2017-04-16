import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

# Location is Ann Arbor
data = pd.read_csv("fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv")
data["Year"] = data["Date"].apply(lambda x:int(x[:4]))
data["Day"] = data["Date"].apply(lambda x:x[5:10])
data=data[data["Day"]!="02-29"] #delete Feb 29 record
data["Day"] = pd.to_datetime(data["Day"],format="%m-%d")
data.Data_Value = data.Data_Value/10 #rescale temperatures

# Build 2015-2014 Max and Min record
dataMin = data[(data.Element=="TMIN") & (data.Year<=2014)].pivot_table(
        values="Data_Value",index=["Day"],aggfunc=min)
dataMax = data[(data.Element=="TMAX") & (data.Year<=2014)].pivot_table(
        values="Data_Value",index=["Day"],aggfunc=max)
# Build 2015 Max and Min record
dataMin2015 = data[(data.Element=="TMIN") & (data.Year==2015)].pivot_table(
        values="Data_Value",index=["Day"],aggfunc=min)
dataMax2015 = data[(data.Element=="TMAX") & (data.Year==2015)].pivot_table(
        values="Data_Value",index=["Day"],aggfunc=max)
# Keep only record breaking values for 2015
data2015 = dataMin2015[dataMin2015<dataMin]
data2015 = data2015.append(dataMax2015[dataMax2015>dataMax])

#plot the 3 curves and fill in between
fig, ax = plt.subplots(figsize=(20,10))
plt.plot(dataMax,"-",color="r",zorder=5)
plt.plot(dataMin,"-",color="b",zorder=10)
plt.scatter(data2015.index,data2015, marker="o",
            facecolor="black",edgecolor="black", s=150,zorder=15, alpha=0.6)
ax.fill_between(dataMin.index, dataMin, dataMax, facecolor='grey', alpha=0.25)

#format the x axis labels
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=15))
ax.xaxis.set_major_formatter(mticker.NullFormatter())
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b"))
ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
dstart = dataMin.index[0]
dend = dataMin.index[-1]
plt.xlim([dstart,dend])
for tick in ax.xaxis.get_minor_ticks():
    tick.tick1line.set_markersize(0)
    tick.tick2line.set_markersize(0)
    tick.label1.set_horizontalalignment("center")
    tick.label1.set_fontsize(20)
    tick.label1.set_rotation(45)

#format the y axis labels
#ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d °C "))
ax.yaxis.set_label_text(label="Temperature (°C)",fontsize=20)
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(15)
#    tick.label1.set_rotation(45)

#get rid of the rop and right spines    
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tick_params(top="off",right="off")

#add title and legend
plt.title("2015 Temperatures Breaking The 10 Previous Years Record",fontsize=26)
plt.legend(["2005-2014 Maximum Temperatures","2005-2014 Minimum Temperatures",
            "2015 Record Breaking Temperatures"],
    loc='lower center', bbox_to_anchor=(0.5, 0.1),
    fontsize=16,frameon=False)