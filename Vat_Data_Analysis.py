import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# getting the dataset from google drive
data = pd.read_csv("https://drive.google.com/uc?export=download&id=1ajzIwFxXsp5QRmk49ilZFfU3nAxQTPby")


data.info()

# Exploratory Data Analysis

# Let's begin some exploratory data analysis! We'll start by checking out missing data!

## Missing Data

# We can use seaborn to create a simple heatmap to see where we are missing data!
sns.heatmap(data.isnull(),yticklabels=False,cbar=False,cmap='viridis')

# Roughly 80 percent of the REFUND_STATUS, REFUND_AMOUNT_CLAIMED,	REFUND_AMOUNT_PAID,	REFUND_ID, and REJECTED_REFUNDS data is 
# missing. The proportion of the missing data is too much to do something useful with at a basic level. We'll probably drop this
# later, or change it to another feature like 1 or 0 .

# Duplicates TPIN
# lets check if they are duplicate tpin

duplicates = data[data.duplicated(subset=['TPIN'], keep=False)]
duplicates.info()

# From the above we can see that we have 228199 tpin are duplicates out of 229120 tpins, which means only 921 are not duplicate.
# Looke close to see what the duplicates data tells.


# Converting the 'TPIN' column to integer using .loc to modify the original DataFrame
duplicates.loc[:, 'TPIN'] = duplicates['TPIN'].astype(int)

# Sorting the DataFrame by 'TPIN' column in ascending order
sorted_duplicates = duplicates.sort_values(by='TPIN')

# Getting the last 5 rows
sorted_duplicates.tail(4)

# With further analysis, we've gained deeper insights into the duplicate TPINs. While the TPINs are duplicated, 
# the values in the other columns are distinct. These duplicates arise from instances where taxpayers have paid
# the VAT tax multiple times.

# Let's continue the EDA on by Visualisation some more of the data! 

# The Relationship between SUM_OF_OUTPUT_INVOICES and SUM_OF_INPUT_INVOICES
plt.figure(figsize=(10,3))
plt.scatter(data['SUM_OF_OUTPUT_INVOICES'],data['SUM_OF_INPUT_INVOICES'],alpha=0.7)
plt.xlabel('Number of output invoices')
plt.ylabel('NUmber of input invoices')
plt.title('Count of input VS Output',size=18)

# The Relationship between REFUND_AMOUNT_CLAIMED and REFUND_AMOUNT_PAID
plt.figure(figsize=(10,3))
plt.scatter(data['REFUND_AMOUNT_CLAIMED'],data['REFUND_AMOUNT_PAID'],alpha=0.7)
plt.xlabel('Refund ammount claimed values')
plt.ylabel('Refund amount paid values')
plt.title('Count of climed VS paid',size=18)


# The types Refund status
plt.figure(figsize=(10,3))
data['REFUND_STATUS'].value_counts().sort_values(ascending=True).plot(kind='barh')


# Data Cleaning
# We aim to clean the missing data, and upon inspection, we've identified 5 columns containing missing values. 
# Specifically, we need to address the missing data in the REFUND_STATUS column. To do so, we'll fill in the 
# missing REFUND_STATUS data with the corresponding values for each status. For instance, where the status is 
# 'APPROVED', missing values will be filled with 6; where there are NaN values, they'll be replaced with 0. 
# We'll apply similar logic for the other possible statuses since REFUND_STATUS can have multiple values.

# Define the mapping of statuses to numeric values

status_mapping = {
    'FULLY_PAID_MANUALLY': 1,
    'INITIATED': 2,
    'REJECTED': 3,
    'FULLY_PAID': 4,
    'RECOMMENDED_APPROVAL': 5,
    'APPROVED': 6,
    'COMPLETED': 7,
    'RECOMMENDED_REJECTION': 8
}

# Replace NaN with 0 and map the statuses to numeric values
data['REFUND_STATUS'] = data['REFUND_STATUS'].map(status_mapping).fillna(0)

# Upon examining the missing data in other columns such as REFUND_AMOUNT_CLAIMED, REFUND_AMOUNT_PAID, and 
# REJECTED_REFUNDS, we observe that the missing values may be due to scenarios where the taxpayer did not 
# claim a refund or the refund was not approved. Instead of dropping these columns, we can address the missing 
# data (NaNs) by filling them with zero.

# Assuming data is your DataFrame
columns_to_fill = ['REFUND_AMOUNT_CLAIMED', 'REFUND_AMOUNT_PAID', 'REJECTED_REFUNDS']

# Fill NaN values with zero for specified columns
data[columns_to_fill] = data[columns_to_fill].fillna(0)

# Upon examining the data, we've identified that the columns TPIN, RETURN_ID, and REFUND_ID contain values 
# that are either increasing numbers or constants, which do not provide any meaningful value for data analysis 
# or model creation. To improve our analysis, we will take the following steps:

# Drop rows where TPIN is missing, as it is a crucial identifier.
# Completely remove the columns RETURN_ID and REFUND_ID from the dataset. et.

# Drop rows where TPIN is missing
data.dropna(subset=['TPIN'], inplace=True)

# Remove the columns RETURN_ID and REFUND_ID
data.drop(columns=['RETURN_ID', 'REFUND_ID'], inplace=True)



# The data has been cleaned and is now ready for further analysis, such as generating a heatmap to show correlation
# between the columns.

import seaborn as sns
plt.figure(figsize=(18,18))
cor = data.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()

data.to_csv('clean_vat_data_v1.csv', index=False)