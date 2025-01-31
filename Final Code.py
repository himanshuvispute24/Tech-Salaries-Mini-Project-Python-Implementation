import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium

#Load the dataset
df = pd.read_csv("salaries_clean.csv")
print(df.head())

print(df.shape)

missing_values = df.isnull().sum()
print("Missing values per column:\n", missing_values)

# 2.Handling missing value

#Imputation for critical columns
df['annual_base_pay'].fillna(df['annual_base_pay'].median(), inplace=True)

# Imputation for `total_experience_years` and `employer_experience_years` with median
df['total_experience_years'].fillna(df['total_experience_years'].median(), inplace=True)
df['employer_experience_years'].fillna(df['employer_experience_years'].median(), inplace=True)

# Imputation for `employer_name`
df['employer_name'].fillna('A stranger', inplace=True)

#Imputation for `employer_name`
df['employer_name'].fillna('A stranger', inplace=True)

# Imputation for categorical columns with fashion
df['location_state'].fillna(df['location_state'].mode()[0], inplace=True)
df['location_country'].fillna(df['location_country'].mode()[0], inplace=True)
df['location_latitude'].fillna(df['location_latitude'].mode()[0], inplace=True)
df['location_longitude'].fillna(df['location_longitude'].mode()[0], inplace=True)
df['job_title_rank'].fillna(df['job_title_rank'].mode()[0], inplace=True)

# Delete rows with missing values in remaining critical columns
df.dropna(subset=['annual_base_pay'], inplace=True)

# Remove columns with many missing value
df.drop(columns=['comments'], inplace=True)

#Imputation of bonds with the median
df['signing_bonus'].fillna(0, inplace=True)  # Assign 0 to those who did not receive signing_bonus
df['annual_bonus'].fillna(0, inplace=True)   # Assign 0 to those who did not receive annual_bonus
df['stock_value_bonus'].fillna(0, inplace=True)  # Assign 0 to those who did not receive stock_value_bonus

# You can also check how the DataFrame looked after imputation
print("Missing values after imputing bonuses:\n", df.isnull().sum())

print(df.shape)

## 1.3. Duplicate values
print("Duplicate values before deleting:", df.duplicated().sum())
df.drop_duplicates(inplace=True)
print("Duplicate values after deleting:", df.duplicated().sum())

## 1.4. Categorical inconsistencies
#\df['job_title'].unique()# = df['job_title'].str.strip().str.lower()  # Unifying uppercase/lowercase letters and spaces

## 1.5. abnormal data
# We define a limit for abnormal salaries and correct or eliminate
salary_threshold = 200000  # Salary threshold example
df2 = df[df['annual_base_pay'] < salary_threshold]

print(df.shape)
print(df2.shape)

df['annual_base_pay'].max()

# 2. Data Exploration

#SummaryStatistics
#print(df['salary'].describe())

## 2.1. Uni variate Visualization #1: Salary Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['annual_base_pay'], bins=30, kde=True)
plt.title('Annual Base Salary Distribution',fontsize=16)
plt.xlabel('Annual Base Salary',fontsize=12)
plt.ylabel('Frequency')
plt.show()

# 2. Data Exploration

## 2.1. Uni variate Visualization #1: Salary Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df2['annual_base_pay'], bins=30, kde=True)
plt.title('Annual Base Salary Distributio')
plt.xlabel('Annual Base Salary')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x=df2['annual_base_pay'])
plt.title('Boxplot of Annual Base Salary')
plt.xlabel('Annual Base Salary')
plt.show()

## 2.5. Multivariate visualization #3: Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df2, x='total_experience_years', y='annual_base_pay', hue='job_title_category')
plt.title('Annual Base Salary vs Years of Experience')
plt.xlabel('Years of Experience')
plt.ylabel('Annual Base Salary')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

plt.figure(figsize=(10, 6))
sns.violinplot(x='job_title_category', y='annual_base_pay', data=df2)
plt.title('Distribution of Annual Base Salary by Job Category')
plt.xlabel('Job Category')
plt.ylabel('Annual Base Salary')
plt.xticks(rotation=45)
plt.show()


#Interactive Salary Map
#Sample dataset (replace with your actual data)
data = {
    'location_country': ['US', 'CA', 'OM', 'SE', 'JE'],
    'location_latitude': [37.77,36.36,41.47,38,43.1],
    'location_longitude': [-122.41,-94.2,-81.67,-97,-89.5],
    'annual_base_pay': [120000, 80000, 25000, 90000, 85000]  # Average salaries in USD
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a base map centered at a global view
m = folium.Map(location=[20, 0], zoom_start=2)

# Add markers for each country
for idx, row in df.iterrows():
    folium.Marker(
        location=[row['location_latitude'], row['location_longitude']],  # Latitude and Longitude
        popup=f"{row['location_country']}: ${row['annual_base_pay']:,.2f}",  # Popup text
        tooltip=row['location_country']  # Tooltip on hover
    ).add_to(m)

# Save the map to an HTML file
m.save('global_salary_map.html')



