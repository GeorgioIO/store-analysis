# Importing libraris ill use
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import humanize


# TODO : Loading the data
data = pd.read_csv('data/superstore.csv' , encoding='latin1')

print(data.head()) # To see first 5 rows
print(data.tail()) # To see last 5 rows
print(data.describe()) # statistical function of each column
print(data.info()) # to see the number of not null in a column and what is its type


# TODO : Data Cleaning Phase + managing types

data['Order Date'] = pd.to_datetime(data['Order Date'])
data['Ship Date'] = pd.to_datetime(data['Ship Date'])

col_to_categorize = ['Ship Mode' , 'Sub-Category' , 'Category' , 'Region' , 'Segment' , 'State']
for col in col_to_categorize:
    data[col] = data[col].astype('category')

# After adding dummy row with missing values and duplicates

print(data.isnull().sum()) # Here we find out that Ship mode and segmet have one null values , and also Segment 

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
# to ensure the months appear in a calendar order (Jan -> Dec) When pivoting or sorting
data['Month'] = pd.Categorical(data['Month'] , categories=months , ordered=True)
data.set_index("Row ID" , inplace=True)

print("=== DATAFRAME AFTER ENGINEERING FEATURES===\n" , data)

# Sort Columns
data.sort_values(by='Year' , ascending=False , inplace=True)

#TODO : EDA Exploratory Data Analysis

# # TODO : 1. Summary Statistics of numeric Values , Sales , quantity , Discount , Profit
print("=== SALES STATS ====")
sales_related_col = data[['Sales']]
total_sales = round(sales_related_col.sum().iloc[0])
average_sales = round(sales_related_col.mean().iloc[0] , 2)
median_sales = round(sales_related_col.median().iloc[0] , 2)
sales_stats = pd.DataFrame({'Total Sales ($)' : [total_sales] , 'Average Sales' : [average_sales] , 'Median Sales' : [median_sales]})
print(sales_stats , '\n')

print("=== PROFITS STATS ===")
profits_related_col = data[['Profit']]
total_profits = round(profits_related_col.sum().iloc[0])
average_profits = round(profits_related_col.mean().iloc[0])
median_profits = round(profits_related_col.median().iloc[0])
profits_stats = pd.DataFrame({'Total Profit ($)' : [total_profits] , 'Average Profit' : [average_profits] , 'Median Profit' : [median_profits]})
print(profits_stats , '\n')

print("🔍 Insight #1: ")
print(f"As we can see the Total Sales of the store is {humanize.intword(total_sales)} USD while The Total Profit is {humanize.intword(total_profits)} USD \n")



stats_metrics = ['sum' , 'mean']
print("=== SALES / PROFIT STATS PER CATEGORY ===")
sales_profit_category_stats = pd.pivot_table(data , index='Category' , values=['Sales' , 'Profit'] , aggfunc={'Sales' : stats_metrics , 'Profit' : stats_metrics} , observed=False)
sales_profit_category_stats = sales_profit_category_stats.round(2)
print(sales_profit_category_stats , '\n')

print("🔍 Insight #2: ")
print(f"From this insight we find out that Technology category is the most profitable category in the store since it has the highest profit sum and the highest sales Sum")
print(f"With {humanize.intword(sales_profit_category_stats.loc['Technology' , ('Profit' , 'sum')])} USD for Profit")
print(f"With {humanize.intword(sales_profit_category_stats.loc['Technology' , ('Sales' , 'sum')])} USD for Sales\n")
print(f"Business Suggestion : Here we can think of increasing the marketing campaigns related to Technology products")

# print("=== SALES / PROFIT STATS PER Sub-Category ===")
# grouped_sub_category = data.groupby('Sub-Category' , observed=False)[['Sales' , 'Profit']].agg({'Sales' : stats_metrics , 'Profit' : stats_metrics})
# grouped_sub_category = grouped_sub_category.round(2)
# print(grouped_sub_category , '\n') 

print("=== SALES / PROFIT STATS PER SEGMENT")
grouped_segment = data.groupby('Segment' , observed=False)[['Sales' , 'Profit']].agg({'Sales' : stats_metrics  , 'Profit' : stats_metrics})
grouped_segment = grouped_segment.round(2)
grouped_segment['Profitability Score (%)'] = round((grouped_segment['Profit' , 'sum'] / grouped_segment['Sales' , 'sum']) * 100 , 2)
print(grouped_segment , '\n')

print("🔍 Insight #3: ")
print(f"From this insight we can clearly see through profitability score that {grouped_segment['Profitability Score (%)'].idxmax()} is the most profitable Segment")
print(f"With %{grouped_segment['Profitability Score (%)'].max()}")
print(f"While the lowest profitable Segment is {grouped_segment['Profitability Score (%)'].idxmin()}")
print(f"With %{grouped_segment['Profitability Score (%)'].min()}")
print(f"Business Suggestion : We can increase the focus on the products that {grouped_segment['Profitability Score (%)'].idxmax()} Segment usually buys\n")


print("=== SALES / PROFIT STATS PER SHIP MODE ===")
grouped_ship_mode = data.groupby('Ship Mode' , observed=False)[['Sales' , 'Profit']].agg({'Sales' : stats_metrics , 'Profit' : stats_metrics})
grouped_ship_mode = grouped_ship_mode.round(2)
grouped_ship_mode.sort_values(by=('Profit' , 'sum') , ascending=False , inplace=True)
print(grouped_ship_mode , '\n')

print("🔍 Insight #4: ")
print(f"As we can see {grouped_ship_mode[('Profit' , 'sum')].idxmax()} is the most profitable Ship Mode")
print(f"With {humanize.intword(grouped_ship_mode[('Profit' , 'sum')].max())} USD as profit")
print(f"While the least profitable ship mode is {grouped_ship_mode[('Profit' , 'sum')].idxmin()}")
print(f"With {humanize.intword(grouped_ship_mode[('Profit' , 'sum')].min())} USD as profit")
print(f"Business suggestion : From this insight we can think of improving more the perks of Same Day Ship Mode \n")

print("=== SALES / PROFIT STATS PER REGION ===")
grouped_region = data.groupby('Region' , observed=False)[['Sales' , 'Profit']].agg({'Sales' : stats_metrics , 'Profit' : stats_metrics}).round(2)
grouped_region.sort_values(by=('Profit' , 'sum') , ascending=False , inplace=True)
print(grouped_region , '\n')

print("🔍 Insight #5: ")
print(f"From Insight #5 we find out that {grouped_region[('Profit' , 'sum')].idxmax()} is the most profitable Region")
print(f"With {humanize.intword(grouped_region[('Profit' , 'sum')].max())} USD")
print(f"While the least profitable Region is {grouped_region[('Profit' , 'sum')].idxmin()} Region")
print(f"With {humanize.intword(grouped_region[('Profit' , 'sum')].min())} USD \n")

print("=== SALES / PROFIT PER STATE ===")
grouped_state = data.groupby('State' , observed=False)[['Sales' , 'Profit']].agg({'Sales' : stats_metrics , 'Profit' : stats_metrics}).round(2)
top_ten_state_sales = grouped_state.sort_values(by=('Sales' , 'sum') , ascending=False).head(10)
top_ten_state_profit = grouped_state.sort_values(by=('Profit' , 'sum') , ascending=False).head(10)
print("- TOP 10 BY SALES - ")
print(top_ten_state_sales , '\n')
print("- TOP 10 BY PROFIT - ")
print(top_ten_state_profit , '\n')

least_ten_state_sales = grouped_state.sort_values(by=('Sales' , 'sum') , ascending=True).head(10)
least_ten_state_profit =  grouped_state.sort_values(by=('Profit' , 'sum') , ascending=True).head(10)
print("- LEAST 10 BY SALES - ")
print(least_ten_state_sales , '\n')
print("- LEAST 10 BY PROFIT - ")
print(least_ten_state_profit , '\n')

top_state = top_ten_state_profit[('Profit', 'sum')].idxmax()
top_state_value = humanize.intword(top_ten_state_profit[('Profit' , 'sum')].max())
least_state = least_ten_state_profit[('Profit', 'sum')].idxmin()
least_state_value = humanize.intword(least_ten_state_profit[('Profit' , 'sum')].min())

print("🔍 Insight #6: ")
print(f"From insight #6 we can clearly identify that the most profitable State is {top_state}")
print(f"With {top_state_value} USD as Profit")
print(f"While the lowest profitable state is {least_state}")
print(f"With {least_state_value} USD as Profit")
print(f"For some Business suggestions , we can think of increasing the marketing and concentrate more about {least_state} market.\nFor {top_state} we can analyze what make it a good State and apply the same strategy for underperforming State\n")

# Product And Category analysis

print("=== TOTAL PROFIT PER SUB-CATEGORY ===")
total_profit_per_subcat = data.groupby('Sub-Category' , observed=False)[['Profit']].sum().reset_index().set_index('Sub-Category')
total_profit_per_subcat.sort_values(by='Profit' , ascending=False , inplace=True)
top_sub_category = total_profit_per_subcat['Profit'].idxmax()
top_sub_category_value = humanize.intword(total_profit_per_subcat['Profit'].max())
least_sub_category = total_profit_per_subcat['Profit'].idxmin()
least_sub_category_value = humanize.intword(total_profit_per_subcat['Profit'].min())
print(total_profit_per_subcat , '\n')

print("=== NEGATIVE PROFIT SUB-CATEGORY -- under performing category ===")
negative_profit = total_profit_per_subcat.query("Profit < 0")
print(negative_profit , '\n')

print("=== BAD MARGIN SUB-CATEGORY WITH HIGH SALES BUT LOW PROFIT OR NEGATIVE PROFIT ===")
sub_category_sales_profit = data.groupby('Sub-Category' , observed=False)[['Sales' , 'Profit']].agg({'Sales' : 'sum' , 'Profit' : 'sum'})
# TO DECIDE HIGH SALES we will consider the one above median sales LOW SALES below it , same for profit
# HIGH SALES IF Sales > median sales else LOW
# HIG PROFIT IF Profit > media Profit else LOW
median_sales_per_subcat = sub_category_sales_profit['Sales'].median()
median_profit_per_subcat = sub_category_sales_profit['Profit'].median()
bad_margin_subcat = sub_category_sales_profit.query("Sales > @median_sales_per_subcat & Profit < @median_profit_per_subcat")
print(bad_margin_subcat , '\n')

print("🔍 Insight #6: ")
print(f"From this insight we identify that the most profitable Sub-Category is {top_sub_category}")
print(f"With {top_sub_category_value} USD as Profit")
print(f"While the least profitable Sub-Category is {least_sub_category}")
print(f"With {least_sub_category_value} USD as Profit")
print("For some business suggestions , we can increase profits of under performing Sub-category by applying discounts on them or maybe increasing their marketing , buying stocks of high performing Sub-Category is a choice \n")

# Time Series Analysis

# TODO : Get monthly Sales trends per year
years = data['Year'].unique() 

print("=== YEARLY TOTAL SALES AND PROFIT ===")
sales_profit_year = data.groupby('Year')[['Sales' , 'Profit']].agg({'Sales' : 'sum' , 'Profit' : 'sum'})
print(sales_profit_year , '\n')
top_year = sales_profit_year['Profit'].idxmax()
top_year_value = humanize.intword(sales_profit_year['Profit'].max())
least_year = sales_profit_year['Profit'].idxmin()
least_year_value = humanize.intword(sales_profit_year['Profit'].min())

print("🔍 Insight #7: ")
print(f"From this insight we clearly see that the store made the most Profit in {top_year}")
print(f"With {top_year_value} USD as Profit")
print(f"While the least profitable year is {least_year}")
print(f"With {least_year_value} USD as Profit")
print(f"Business Suggestions : We can analyze why {top_year} performed that well , and why its better then the others , and based on that we make decisions the upcoming year.\n")

print("=== SALES / PROFIT BY MONTHS OVER THE YEAR ===")

print("SALES :")
sales_by_month_yearly = pd.pivot_table(data , index='Year' , columns='Month' , values='Sales' , aggfunc='sum' , observed=False).round(2)
print(sales_by_month_yearly , '\n')
print("PROFIT")
profit_by_month_yearly = pd.pivot_table(data , index='Year' , columns='Month' , values='Profit' , aggfunc='sum' , observed=False).round(2)
print(profit_by_month_yearly , '\n')

# Geographical Analysis
print("=== STATE RANKING BY TOTAL SALES ===")
sales_per_state = data.groupby('State' , observed=False)[['Sales']].sum().astype(int)
total_sales_per_state = sales_per_state.sort_values(by='Sales' , ascending=False)
total_sales_per_state = total_sales_per_state.head(10)
print(total_sales_per_state , '\n')

least_sales_per_state = sales_per_state.sort_values(by='Sales' , ascending=True)
least_sales_per_state = least_sales_per_state.head(10)
print(least_sales_per_state , '\n')

print("=== STATES WITH NEGATIVE PROFIT ===")
states_negative_profit = data.groupby('State' , observed=False)[['Profit']].sum()
states_negative_profit = states_negative_profit.loc[states_negative_profit['Profit'] < 0]
states_negative_profit.sort_values(by='Profit' , ascending=True , inplace=True)
print(states_negative_profit, '\n')

print("=== REGION WISE CONTRIBUTION FOR TOTAL SALES AND PROFIT ===")
print("Total Sales of all region is" , total_sales , "$")
sales_per_region = data.groupby('Region' , observed=False)[['Sales' , 'Profit']].sum().round(2)
sales_per_region.rename(columns={'Sales' : 'Sales Contribution (%)' , 'Profit' : 'Profit Contribution (%)'} , inplace=True)
region_contribution = round((sales_per_region / sales_per_region.sum()) * 100 , 2)
print(region_contribution , '\n')

labels_for_pie = ['Central' , 'East' , 'South' , 'West']
colors_for_pie = ['#1f77b3' , '#2ca02c', '#ff7f0e' , '#d62728']

plt.pie(region_contribution['Sales Contribution (%)'] , labels=labels_for_pie , colors=colors_for_pie , autopct='%.2f %%')
plt.title('Sales Contribution Per Region')
plt.show()

plt.pie(region_contribution['Profit Contribution (%)'] , labels=labels_for_pie , colors=colors_for_pie , autopct='%.2f %%')
plt.title("Profit Contribution Per Region")
plt.show()

# Orders And Customers Analysis
# TODO : Find the Customer with the most profit
profit_per_customers = data.groupby(['Customer Name' , 'State'] , observed=True)[['Profit']].sum().astype(int).reset_index().set_index('Customer Name')
profit_per_customers.sort_values(by='Profit' , ascending=False , inplace=True)
top_ten_profitable_customers = profit_per_customers.head(10)
least_ten_profitable_customers = profit_per_customers.tail(10)
top_customer = top_ten_profitable_customers['Profit'].idxmax()
top_customer_value = humanize.intword(top_ten_profitable_customers['Profit'].max())
least_customer = least_ten_profitable_customers['Profit'].idxmin()
least_customer_value = humanize.intword(least_ten_profitable_customers['Profit'].min())

print("=== TOP 10 MOST PROFITABLE CUSTOMERS ===")
print(top_ten_profitable_customers , '\n')

print("=== TOP 10 LEAST PROFITABLE CUSTOMERS ===")
print(least_ten_profitable_customers , '\n')

print("🔍 Insight #8: ")
print(f"From this insight we can see that {top_customer} is our most profitable customer")
print(f"Generating us {top_customer_value} USD as Profit")
print(f"For some business suggestions we can offer loyalty programs for top performing customers")

profitability_scores_per_order = data.groupby('Order ID')[['Sales' , 'Profit']].sum()
# TODO: Create Profitability score per order 
profitability_scores_per_order['Profitability Score (%)'] = round((profitability_scores_per_order['Profit'] / profitability_scores_per_order['Sales']) * 100 , 2)
top_ten_profitable_orders = profitability_scores_per_order.sort_values(by='Profit' , ascending=False).head(10)
least_ten_profitable_orders = profitability_scores_per_order.sort_values(by='Profit' , ascending=False).tail(10)

print("=== TOP TEN PROFITABLE ORDERS ===")
print(top_ten_profitable_orders , '\n')

print("=== TOP TEN LEAST PROFITABLE ORDERS ===")
print(least_ten_profitable_orders , '\n')
