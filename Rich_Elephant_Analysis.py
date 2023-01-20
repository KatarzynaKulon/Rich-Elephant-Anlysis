import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import seaborn as sns
pd.set_option("display.max_rows", None, "display.max_columns", None)

tr_df = pd.read_csv('transactions.csv')

# Transformations
tr_df["Authorization time"] = pd.to_datetime(tr_df["Authorization time"])
# Create a column with binary representation of an error: 0 = no error, 1 = error occured
tr_df['Error_Occurred'] = tr_df['Error Code'].fillna(0)
tr_df["Error_Occurred"] = pd.Series(np.where(tr_df["Error_Occurred"] != 0,1,0),tr_df.index)

# Split the Authorization time column into Date and Time column
tr_df['Date'] = pd.to_datetime(tr_df['Authorization time']).dt.date
tr_df['Time'] = pd.to_datetime(tr_df['Authorization time']).dt.time

# Df w/ total number of errors per day per card provider, per product
new = (tr_df.groupby(['Date','Processed Card Scheme','Processed Card Product']).sum("Error_Occurred"))
new = new.drop(['Transaction ID'],axis = 1)
print(new)

# box plot
ax = sns.boxplot(x='Used Secure3D',y='Transaction amount',data=tr_df)
# bar plot
#ax = sns.catplot(x='Used Secure3D',y='Transaction amount',data=new)
# Bar plot 3D vs Errors


# how many where errors compared to used 3D?
new2 = (tr_df.groupby(['Date','Used Secure3D','Processed Card Scheme','Processed Card Product']).sum("Error_Occurred"))
new2 = new2.reset_index()
#ax = sns.catplot(x='Used Secure3D',y='Error_Occurred',data=new2) #tu pokazuja sie punkty a ja chce bars


# How many 3d are used per card
# Changed used 3D na 0/1 -> barchart: y-count a na x sa producty (karty) i dla kazdej karty 2 slupki (0,1)
new3 = tr_df
new3["Used Secure3D"] = pd.Series(np.where(new3["Used Secure3D"] == "NO" ,0,1),new3.index)
new3 = (tr_df.groupby(['Date','Used Secure3D','Processed Card Scheme','Processed Card Product']).sum("Error_Occurred"))
new3 = new3.reset_index()
# # ax = sns.catplot(x='Used Secure3D',hue='Processed Card Scheme',data=new3,kind='count')
#pd.crosstab(new3['Processed Card Scheme'],new3['Used Secure3D']).plot.bar(stacked=True)


## PLOTS ERRORS OCCURED
errors_grouped_per_card = tr_df.groupby('Processed Card Scheme')['Error_Occurred'].sum()
errors_grouped_per_card = errors_grouped_per_card.to_frame()
errors_grouped_per_card = errors_grouped_per_card.reset_index()
# TOTAL AMOUNT OF ERRORS PER CARD
#ax = sns.barplot(x='Processed Card Scheme',y='Error_Occurred',data=errors_grouped_per_card) #tu pokazuja sie punkty a ja chce bars

## TIMELY PLOTS
# Total number of errors per day
errors_daily = tr_df.groupby('Date')['Error_Occurred'].sum()
#pd.pivot_table(errors_daily.reset_index(),
 #              index='Date', values='Error_Occurred'
  #            ).plot(subplots=True,legend =None)
plt.xlabel("Date")
plt.ylabel("Total number of errors occurred")

# Total number of errors per day/ per card provider
errors_daily_per_card = tr_df.groupby(['Date','Processed Card Scheme'])['Error_Occurred'].sum()

#pd.pivot_table(errors_daily_per_card.reset_index(),
 #              index='Date',columns='Processed Card Scheme', values='Error_Occurred'
  #            ).plot(subplots=False)
plt.xlabel("Date")
plt.ylabel("Total number of errors occurred")
# Total number of errors per day/ per card PRODUCT
errors_daily_per_prod = tr_df.groupby(['Date','Processed Card Scheme','Processed Card Product'])['Error_Occurred'].sum()

#pd.pivot_table(errors_daily_per_prod.reset_index(),
 #              index='Date',columns=['Processed Card Scheme','Processed Card Product'], values='Error_Occurred'
  #            ).plot(subplots=False)
plt.xlabel("Date")
plt.ylabel("Total number of errors occured")
plt.show()

# CORRELATIONS HEAT MAP
corr_df = tr_df.drop("Transaction ID",axis = 1)
corr = corr_df.corr()
sns.heatmap(corr,xticklabels=corr.columns.values,
            yticklabels=corr.columns.values, annot = True)

# PAIRED CORRELATIONS
sns.scatterplot(x="Used Secure3D",y="Error_Occurred", data = tr_df )
plt.show()

# transaction amount per card daily
pd.pivot_table(tr_df.reset_index(),
               index='Date', columns='Processed Card Scheme', values='Transaction amount'
             ).plot(subplots=True)

#dfplot = tr_df
#dfplot.set_index("Date",inplace=True)
#dfplot.groupby('Processed Card Scheme').sum('Error_Occurred').plot(legend=True)
#dfplot = dfplot.groupby(['Date','Processed Card Scheme']).sum('Error_Occurred')
#dfplot = dfplot.reset_index()
#dfplot.set_index("Date",inplace=True)
#dfplot.plot(legend=True)
#plt.show()
#print(dfplot.head(5))

#counter = 0
#for date in new_date.Date.unique().tolist():
#    for provider in new_date['Processed Card Product'].unique().tolist():
