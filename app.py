# Importing libraris ill use
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import humanize

plt.style.use('ggplot')


# TODO : Loading the data
data = pd.read_csv('data/superstore.csv' , encoding='latin1')

# TODO : Data Cleaning Phase + managing types
data['Order Date'] = pd.to_datetime(data['Order Date'])
data['Ship Date'] = pd.to_datetime(data['Ship Date'])

col_to_categorize = ['Ship Mode' , 'Sub-Category' , 'Category' , 'Region' , 'Segment' , 'State']
for col in col_to_categorize:
    data[col] = data[col].astype('category')

# Treat duplicate rows
duplicated_sum = data.duplicated().sum()
if duplicated_sum > 0 :
    data.drop_duplicates(inplace=True)

most_occurent_ship_mode = data['Ship Mode'].mode()[0]
most_occurent_segment = data['Segment'].mode()[0]

data['Ship Mode'] = data['Ship Mode'].fillna(most_occurent_ship_mode)
data['Segment'] = data['Segment'].fillna(most_occurent_segment)

# Check if any discounts higher then 1
discount_higher_then_01 = (data['Discount'] > 1).sum()
if discount_higher_then_01 >= 1:
    print("Discount Higher then 1 founded and fixed")
    data['Discount'] = np.where(data['Discount'] > 1 , data['Discount'].median() , data['Discount'])

# TODO : Engineering features
months = list(calendar.month_name)[1:]
data['Year'] = data['Order Date'].dt.strftime("%Y")
data['Month'] = data['Order Date'].dt.strftime("%B")

# Convert Month column to an ordered categorical type
data['Month'] = pd.Categorical(data['Month'] , categories=months , ordered=True)
data.set_index("Row ID" , inplace=True)

# Sort Columns
data.sort_values(by='Year' , ascending=False , inplace=True)


# TODO : What is the most demanded product ?
# ! Get the total order count per product
orders_per_product = data.groupby(by='Product Name' , observed=False).size()
orders_per_product.sort_values(ascending=False , inplace=True)
most_demanded_product = orders_per_product.head(10)

plt.figure(figsize=(14,6))
plt.barh(most_demanded_product.index, most_demanded_product.values)
plt.xlabel('Quantity Sold')
plt.title('Top 10 Most Demanded Products')
plt.gca().invert_yaxis()  # convert the largest on top
plt.savefig("figures/question_1_fig.png") 
plt.show()


# TODO : What region is the most profitable region for the store ?
# ! Get the total profit per region
 
print("=== SALES / PROFIT STATS PER REGION ===")
most_profitable_regions = data.groupby('Region' , observed=False)[[ 'Profit']].sum()
most_profitable_regions.rename(columns={'Profit':'Total Profit'} , inplace=True)
most_profitable_regions['Total Profit'] = round(most_profitable_regions['Total Profit']).astype(int)
most_profitable_regions.sort_values(by='Total Profit' , ascending=False , inplace=True)
print(most_profitable_regions , '\n')

print("🔍 Insight #5: ")
print(f"From Insight #5 we find out that {most_profitable_regions['Total Profit'].idxmax()} is the most profitable Region")
print(f"With {humanize.intword(most_profitable_regions['Total Profit'].max())} USD")
print(f"While the least profitable Region is {most_profitable_regions['Total Profit'].idxmin()} Region")
print(f"With {humanize.intword(most_profitable_regions['Total Profit'].min())} USD \n")

plt.figure(figsize=(12,6))
most_profitable_regions_bars = plt.bar(most_profitable_regions.index , most_profitable_regions['Total Profit'])
plt.bar_label(most_profitable_regions_bars , label_type='edge' , padding=3)
plt.xticks(fontsize=6)
plt.xlabel("Regions")
plt.ylabel("Total Profit in USD")
plt.title("What is the most profitable region for the store ?")
plt.savefig("figures/question_2_fig.png") 
plt.show()

years = data['Year'].unique() 

# TODO : Get monthly Sales trends per year
print("=== PROFIT BY MONTHS OVER THE YEAR ===")
print("SALES :")
sales_by_month_yearly = pd.pivot_table(data , index='Year' , columns='Month' , values='Sales' , aggfunc='sum' , observed=False).round(2)
print(sales_by_month_yearly , '\n')


plt.figure(figsize=(12 ,6))
for year in sales_by_month_yearly.index:
    plt.plot(months , sales_by_month_yearly.loc[year] , label=year , marker='o')
    max_month = sales_by_month_yearly.loc[year].idxmax()
    max_month_value = sales_by_month_yearly.loc[year].max()
    max_month_value_formatted = humanize.intword(max_month_value).replace(" thousand" ,  "k")    
    month_index = months.index(max_month)
    plt.annotate(max_month_value_formatted , xy=(month_index , max_month_value) , xytext=(month_index - 0.4 , max_month_value - 1500)  , arrowprops=dict(arrowstyle='->',color='gray'))
    
plt.ylabel("Profit ($USD)")
plt.title("Total Profit Per Year Over The Months ($USD)")
plt.legend()
plt.savefig("figures/question_3_fig.png") 
plt.show()


# TODO : Find the customer with the most profit in the most profitable state
most_prof_region = most_profitable_regions['Total Profit'].idxmax()
customers_rg = data[data['Region'] == most_prof_region]
profit_per_customers = customers_rg.groupby(['Customer ID' , 'Customer Name' , 'State'] , observed=True)[['Profit']].sum().astype(int).reset_index().set_index('Customer Name')
profit_per_customers.rename(columns={'Profit':'Total Profit'} , inplace=True)
profit_per_customers.sort_values(by='Total Profit' , ascending=False , inplace=True)
top_ten_profitable_customers = profit_per_customers.head(10)
top_customer = top_ten_profitable_customers['Total Profit'].idxmax()
top_customer_value = humanize.intword(top_ten_profitable_customers['Total Profit'].max())

print("=== TOP 10 MOST PROFITABLE WEST CUSTOMERS ===")
print(top_ten_profitable_customers , '\n')

print("🔍 Insight #8: ")
print(f"From this insight we can see that {top_customer} is our most profitable customer")
print(f"Generating us {top_customer_value} USD as Profit")
print(f"For some business suggestions we can offer loyalty programs for top performing customers")

plt.figure(figsize=(12,6))
top_ten_prof_orders_bars = plt.bar(top_ten_profitable_customers.index , top_ten_profitable_customers['Total Profit'])
plt.bar_label(top_ten_prof_orders_bars , label_type='edge' , padding=3)
plt.xticks(fontsize=6)
plt.xlabel("Customer Name")
plt.ylabel("Total Profit in USD")
plt.title("Top 10 most profitable west customers ($USD)")
plt.savefig("figures/question_4_fig.png") 
plt.show()


# TODO : Get the 10 most and least profitable states
print("=== STATE RANKING BY TOTAL PROFIT ===")
profit_per_state = data.groupby('State' , observed=False)[['Profit']].sum().astype(int)
profit_per_state.rename(columns={'Profit':'Total Profit'} , inplace=True)
top_ten_profitable_state_sorted = profit_per_state.sort_values(by='Total Profit' , ascending=False)
top_ten_profitable_state = top_ten_profitable_state_sorted.head(10)
print(top_ten_profitable_state , '\n')

profit_per_state_no_negatives = profit_per_state[profit_per_state['Total Profit'] > 0]
least_10_profitable_state_sorted = profit_per_state_no_negatives.sort_values(by='Total Profit' , ascending=True)
least_10_profitable_state = least_10_profitable_state_sorted.head(10)
print(least_10_profitable_state , '\n')


# Top 10 states
plt.figure(figsize=(15 , 6))
profit_per_top_state_bars = plt.bar(top_ten_profitable_state.index , top_ten_profitable_state['Total Profit'])
plt.bar_label(profit_per_top_state_bars , label_type='edge' , padding=3)
plt.ylabel("Total Profit ($USD)")
plt.title("What are the 10 most profitable states ?")
plt.savefig("figures/question_5(1)_fig.png") 
plt.show()

# Least 10 tates
plt.figure(figsize=(15 , 6))
profit_per_least_state_bars = plt.bar(least_10_profitable_state.index , least_10_profitable_state['Total Profit'])
plt.bar_label(profit_per_least_state_bars , label_type='edge' , padding=3)
plt.ylabel("Total Profit ($USD)")
plt.title("What are the 10 least profitable states?")
plt.savefig("figures/question_5(2)_fig.png") 
plt.show()


