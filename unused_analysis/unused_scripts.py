# print("=== STATES WITH NEGATIVE PROFIT ===")
# states_negative_profit = data.groupby('State' , observed=False)[['Total Profit']].sum()
# states_negative_profit = states_negative_profit.loc[states_negative_profit['Total Profit'] < 0]
# states_negative_profit.sort_values(by='Total Profit' , ascending=True , inplace=True)
# print(states_negative_profit, '\n')


# print("=== YEARLY TOTAL SALES AND PROFIT ===")
# sales_profit_year = data.groupby('Year')[['Sales' , 'Profit']].agg({'Sales' : 'sum' , 'Profit' : 'sum'})
# print(sales_profit_year , '\n')
# top_year = sales_profit_year['Profit'].idxmax()
# top_year_value = humanize.intword(sales_profit_year['Profit'].max())
# least_year = sales_profit_year['Profit'].idxmin()
# least_year_value = humanize.intword(sales_profit_year['Profit'].min())

# print("🔍 Insight #7: ")
# print(f"From this insight we clearly see that the store made the most Profit in {top_year}")
# print(f"With {top_year_value} USD as Profit")
# print(f"While the least profitable year is {least_year}")
# print(f"With {least_year_value} USD as Profit")
# print(f"Business Suggestions : We can analyze why {top_year} performed that well , and why its better then the others , and based on that we make decisions the upcoming year.\n")

# plt.figure(figsize=(8,6))
# sales_per_year = plt.bar(sales_profit_year.index  , sales_profit_year['Sales'] , color='red' , edgecolor='black' )
# profit_per_year = plt.bar(sales_profit_year.index , sales_profit_year['Profit'] , color='blue' , edgecolor='black' )
# plt.ylabel("Sales Per Year")
# plt.title("Sales trends over the year")
# plt.bar_label(sales_per_year , fmt='%.0f' , label_type='edge' , padding=3)
# plt.bar_label(profit_per_year , fmt='%.0f' , label_type='edge' , padding=3)
# plt.legend()
# plt.show()


# print("=== SALES / PROFIT STATS PER CATEGORY ===")
# sales_profit_category_stats = pd.pivot_table(data , index='Category' , values=['Sales' , 'Profit'] , aggfunc={'Sales' : stats_metrics , 'Profit' : stats_metrics} , observed=False)
# sales_profit_category_stats = sales_profit_category_stats.round(2)
# print(sales_profit_category_stats , '\n')

# print("🔍 Insight #2: ")
# print(f"From this insight we find out that Technology category is the most profitable category in the store since it has the highest profit sum and the highest sales Sum")
# print(f"With {humanize.intword(sales_profit_category_stats.loc['Technology' , ('Profit' , 'sum')])} USD for Profit")
# print(f"With {humanize.intword(sales_profit_category_stats.loc['Technology' , ('Sales' , 'sum')])} USD for Sales\n")
# print(f"Business Suggestion : Here we can think of increasing the marketing campaigns related to Technology products")

# # print("=== SALES / PROFIT STATS PER Sub-Category ===")
# # grouped_sub_category = data.groupby('Sub-Category' , observed=False)[['Sales' , 'Profit']].agg({'Sales' : stats_metrics , 'Profit' : stats_metrics})
# # grouped_sub_category = grouped_sub_category.round(2)
# # print(grouped_sub_category , '\n') 

# print("=== SALES / PROFIT STATS PER SEGMENT")
# grouped_segment = data.groupby('Segment' , observed=False)[['Sales' , 'Profit']].agg({'Sales' : stats_metrics  , 'Profit' : stats_metrics})
# grouped_segment = grouped_segment.round(2)
# grouped_segment['Profitability Score (%)'] = round((grouped_segment['Profit' , 'sum'] / grouped_segment['Sales' , 'sum']) * 100 , 2)
# print(grouped_segment , '\n')

# print("🔍 Insight #3: ")
# print(f"From this insight we can clearly see through profitability score that {grouped_segment['Profitability Score (%)'].idxmax()} is the most profitable Segment")
# print(f"With %{grouped_segment['Profitability Score (%)'].max()}")
# print(f"While the lowest profitable Segment is {grouped_segment['Profitability Score (%)'].idxmin()}")
# print(f"With %{grouped_segment['Profitability Score (%)'].min()}")
# print(f"Business Suggestion : We can increase the focus on the products that {grouped_segment['Profitability Score (%)'].idxmax()} Segment usually buys\n")


# print("=== SALES / PROFIT STATS PER SHIP MODE ===")
# grouped_ship_mode = data.groupby('Ship Mode' , observed=False)[['Sales' , 'Profit']].agg({'Sales' : stats_metrics , 'Profit' : stats_metrics})
# grouped_ship_mode = grouped_ship_mode.round(2)
# grouped_ship_mode.sort_values(by=('Profit' , 'sum') , ascending=False , inplace=True)
# print(grouped_ship_mode , '\n')

# print("🔍 Insight #4: ")
# print(f"As we can see {grouped_ship_mode[('Profit' , 'sum')].idxmax()} is the most profitable Ship Mode")
# print(f"With {humanize.intword(grouped_ship_mode[('Profit' , 'sum')].max())} USD as profit")
# print(f"While the least profitable ship mode is {grouped_ship_mode[('Profit' , 'sum')].idxmin()}")
# print(f"With {humanize.intword(grouped_ship_mode[('Profit' , 'sum')].min())} USD as profit")
# print(f"Business suggestion : From this insight we can think of improving more the perks of Same Day Ship Mode \n")


# # Product And Category analysis

# print("=== TOTAL PROFIT PER SUB-CATEGORY ===")
# total_profit_per_subcat = data.groupby('Sub-Category' , observed=False)[['Profit']].sum().reset_index().set_index('Sub-Category')
# total_profit_per_subcat.sort_values(by='Profit' , ascending=False , inplace=True)
# top_sub_category = total_profit_per_subcat['Profit'].idxmax()
# top_sub_category_value = humanize.intword(total_profit_per_subcat['Profit'].max())
# least_sub_category = total_profit_per_subcat['Profit'].idxmin()
# least_sub_category_value = humanize.intword(total_profit_per_subcat['Profit'].min())
# print(total_profit_per_subcat , '\n')

# print("=== NEGATIVE PROFIT SUB-CATEGORY -- under performing category ===")
# negative_profit = total_profit_per_subcat.query("Profit < 0")
# print(negative_profit , '\n')

# print("=== SALES / PROFIT PER STATE ===")
# grouped_state = data.groupby('State' , observed=False)[['Sales' , 'Profit']].agg({'Sales' : stats_metrics , 'Profit' : stats_metrics}).round(2)
# top_ten_state_sales = grouped_state.sort_values(by=('Sales' , 'sum') , ascending=False).head(10)
# top_ten_state_profit = grouped_state.sort_values(by=('Profit' , 'sum') , ascending=False).head(10)
# print("- TOP 10 BY SALES - ")
# print(top_ten_state_sales , '\n')
# print("- TOP 10 BY PROFIT - ")
# print(top_ten_state_profit , '\n')

# least_ten_state_sales = grouped_state.sort_values(by=('Sales' , 'sum') , ascending=True).head(10)
# least_ten_state_profit =  grouped_state.sort_values(by=('Profit' , 'sum') , ascending=True).head(10)
# print("- LEAST 10 BY SALES - ")
# print(least_ten_state_sales , '\n')
# print("- LEAST 10 BY PROFIT - ")
# print(least_ten_state_profit , '\n')

# top_state = top_ten_state_profit[('Profit', 'sum')].idxmax()
# top_state_value = humanize.intword(top_ten_state_profit[('Profit' , 'sum')].max())
# least_state = least_ten_state_profit[('Profit', 'sum')].idxmin()
# least_state_value = humanize.intword(least_ten_state_profit[('Profit' , 'sum')].min())

# print("🔍 Insight #6: ")
# print(f"From insight #6 we can clearly identify that the most profitable State is {top_state}")
# print(f"With {top_state_value} USD as Profit")
# print(f"While the lowest profitable state is {least_state}")
# print(f"With {least_state_value} USD as Profit")
# print(f"For some Business suggestions , we can think of increasing the marketing and concentrate more about {least_state} market.\nFor {top_state} we can analyze what make it a good State and apply the same strategy for underperforming State\n")
