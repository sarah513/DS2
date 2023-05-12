import pandas as pd
#---------------------------------------Drop Duplicates-----------------------------------------------#
data= pd.read_csv('Predict Price of Airline Tickets.csv' , engine='python')
duplicates=data[data.duplicated()]
print(len(duplicates))

# Drop the duplicate rows
data.drop_duplicates(inplace=True)

# Save the cleaned DataFrame to a new Excel file
data.to_csv('cleanData.csv', index=False)
#-------------------------------------Fill Missing Data----------------------------------------------#
data=pd.read_csv('cleanData.csv')

missing_values = data.isnull().sum()
print(missing_values)

#----1 for Route----#
grouped = data.groupby(['Source', 'Destination'])
data['Route'].fillna(grouped['Route'].ffill(), inplace=True)
data.to_csv('cleanData.csv', index=False)

#----2 for Total_Stops----#
data['Total_Stops'].fillna(grouped['Total_Stops'].ffill(),inplace=True)
data.to_csv('cleanData.csv', index=False)

missing_values = data.isnull().sum()
print(missing_values)

#-----------------------------------------------Scale Price ------------------------#
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler

data2=pd.read_csv('Predict Price of Airline Tickets.csv')
data['Price']=data2['Price']
thresholds = {}
for col in data.select_dtypes(include='number'):
    q1, q3 = data[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    thresholds[col] = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    print(thresholds[col])

for col in data.select_dtypes(include='number'):
    outliers = data[col][(data[col] < thresholds[col][0]) | (data[col] > thresholds[col][1])]
    flierprops = dict(markerfacecolor='red', marker='s') if not outliers.empty else dict(markerfacecolor='blue', marker='s')
    sns.boxplot(x=data[col], flierprops=flierprops)
    plt.title(col)
    plt.show()

scaler=RobustScaler()
data['Price']=scaler.fit_transform(data[['Price']])
data.to_csv('cleanData.csv',index=False)
thresholds = {}
for col in data.select_dtypes(include='number'):
    q1, q3 = data[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    thresholds[col] = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    print(thresholds[col])

for col in data.select_dtypes(include='number'):
    outliers = data[col][(data[col] < thresholds[col][0]) | (data[col] > thresholds[col][1])]
    flierprops = dict(markerfacecolor='red', marker='s') if not outliers.empty else dict(markerfacecolor='blue', marker='s')
    sns.boxplot(x=data[col], flierprops=flierprops)
    plt.title(col)
    plt.show()


#------------------------------------------------------Encode categorical data------------------------------#
from sklearn.preprocessing import LabelEncoder
cols_to_encode = ['Airline', 'Source', 'Destination','Total_Stops','Additional_Info']
le= LabelEncoder()
for col in cols_to_encode:
    data[col] = le.fit_transform(data[col])
    # print(data[col])
data.to_csv('cleanData.csv', index=False)



print(data.isnull().sum().sum())



