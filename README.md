# Overview

Welcome to my analysis of a superstore dataset, focusing on .... . This project was created out of a desire to empower , enhance and showcase my **Python** , **Pandas** , **Matplotlib** skills , it delves into the superstore dataset i got from **Kaggle**.

The data source is [Kaggle Dataset Link](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting) which provides the foundation dataset for my analysis, containing information about a global superstore for 4 years such as customer names, segments, product categories and sub categories, country, sales... . Through a series of **Python** scripts, I explore key questions such as the most demanded product, salary trends...

# The Questions

Below are the questions i want to answer in my project:

1. What is the most demanded product in the store ?
2. What region is the most profitable region for the store ?
3. How does the sales trend monthly for each year ?
4. Who are the top customers for the most profitable region ?
5. What are the top and lowest states in profit ?

# Tools I Used

For my deep dive into the superstore dataset, I harnessed the power of several key tools:

- **Python:** The backbone of my analysis, allowing me to analyze the data and find the insights i wanted , also i used the following libraries throughout the project:
  - **Pandas:** This was used to analyze the data.
  - **Matplotlib:** Used this one to visualize the data.
  - **numpy:** Tiny usage for some operations.
  - **calendar:** Used for months analysis.
- **Jupyter Notebooks:** The tool i used to easily integrate my python scripts and run them.
- **Visual Studio Code:** My go-to for any project.
- **Git & Github:** Essential for version control and sharing my Python code and analysis.

# Data Preparation and Cleanup

This section outlines the steps taken to prepate the data for analysis, ensurng accuracy and usability.

## Import & Loading Data

I start by importing necessary libraries that i'll use throughout the project and then loading the dataset.

```python
# Importing libraris ill use
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import humanize

# TODO : Loading the data
data = pd.read_csv('data/superstore.csv' , encoding='latin1')
```

## Cleaning Data + Managing types

Because the dataset was already cleaned i added up some dummy data so i can apply some cleanings , below the scripts i wrote :

```python
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
```

## Engineering features

Next step is to engineer features that i know i'll use throughout my project :

```python
months = list(calendar.month_name)[1:]
data['Year'] = data['Order Date'].dt.strftime("%Y")
data['Month'] = data['Order Date'].dt.strftime("%B")

# Convert Month column to an ordered categorical type
data['Month'] = pd.Categorical(data['Month'] , categories=months , ordered=True)

data.set_index("Row ID" , inplace=True)
```

# The Analysis

Each jupyter notebook for this project aimed at investigating specific aspect of the dataset to reply to the given question. Here how i approached each one :

## 1️⃣ What is the top demanded product in the store ?

To get the most demanded product in the store i grouped by the `Product Name` and counted the orders for that product , sorted then the result by the total orders count and finally extracted top 10 rows

View my notebook with detailed steps here : [most_demanded_prooducts](most_demanded_products.ipynb)

### Visualize Data

```python
plt.figure(figsize=(14,6))
plt.barh(most_demanded_product.index, most_demanded_product.values)
plt.xlabel('Quantity Sold')
plt.title('Top 10 Most Demanded Products')
plt.gca().invert_yaxis()  # convert the largest on top
plt.savefig("figures/question_1_fig.png")
plt.show()
```

### Insights

As we can see determine using the graph , **Staple envelope** is the most demanded product in the store with total of approximately 50 orders , **Staples** come in the second place with 45 orders , we can also realize that **Staples Equipment** in general are very demanded.

![Question 1](/figures/question_1_fig.png)

## 2️⃣ What region is the most profitable region for the store ?

To find the most profitable region in the dataset for the store first of all i grouped the data by Region focusing on Profit column , and got the sum of the profit per each region then i sorted the result by sum of the profit in descending order

View my notebook with detailed steps here : [most_profitable_region](most_profitable_region.ipynb)

### Visualize Data

```python
plt.figure(figsize=(12,6))
most_profitable_regions_bars = plt.bar(most_profitable_regions.index , most_profitable_regions['Total Profit'])
plt.bar_label(most_profitable_regions_bars , label_type='edge' , padding=3)
plt.xticks(fontsize=6)
plt.xlabel("Region")
plt.ylabel("Total Profit in USD")
plt.title("What is the most profitable region for the store ?")
plt.show()
```

### Insights

As we can see **the most profitable region is The West Region** collecting approximetaly $100k Total Profit over 4 years **while the lowest is The Central Region** with nearly $40k Total Profit.

![Question 1](/figures/question_2_fig.png)

## 3️⃣ How does the sales trend monthly for each year ?

To answer this question i decided to create a pivot table based on the data i have , with the index being the years , the columns are each month while the values will be the sum of the sales in that exact month for that year.

View my notebook with detailed steps here : [sales_trend_monthly_year](/sales_trends_monthly_per_year.ipynb)

### Visualize Data

```python
plt.style.use('ggplot')

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
```

![Question 3](/figures/question_3_fig.png)

### Insights

As we can see we can determine the the sales usually peaks in the last 4 months of the year **September**, **October**, **November**, **December** which makes sense, and also we can grasp that the highest month is **November of 2017** with $118k in sales.

## 4️⃣ Who are the top customers for the most profitable region ?

To find the top customers in the most profitable region (**West**) , first of all i filtered the dataset to include the customers only from the **most profitable region** , grouped the result by customer ID and i also included his name and his state , i renamed the column to `Total Profit` , sorted the values in descending order by `Total Profit` and focused on the top 10 customers.

View my notebook with detailed steps here : [top_10_profitable_customers](/top_10_profitable_customers.ipynb)

### Visualize Data

```python
plt.style.use('ggplot')
plt.figure(figsize=(12,6))
top_ten_prof_orders_bars = plt.bar(top_ten_profitable_customers.index , top_ten_profitable_customers['Total Profit'])
plt.bar_label(top_ten_prof_orders_bars , label_type='edge' , padding=3)
plt.xticks(fontsize=6)
plt.xlabel("Customer Name")
plt.ylabel("Total Profit in USD")
plt.title("Top 10 most profitable west customers ($USD)")
plt.savefig("figures/question_4_fig.png")
plt.show()
```

![Question 4](/figures/question_4_fig.png)

### Insights

As we can the most profitable west customer is **Raymond Buch with total profit for the score approximately** $7k with significent difference of the second most profitable west customer **Jane Waco** with $2k total profit.

## 5️⃣ What are the top and lowest states in profit ?

To make this analysis first there is two parts **Top States** , **Least States** in Total Profit . First i grouped by the dataset by `State` and focused on `Profit` column to get the sum of `Profit` per state , then to get the too state i sorted by total profit in descending order and then extracted the top ten column in the other side for the least profitable states i filtered the dataset to get me only the rows where `Profit` isnt under 0 and then did the exact same steps.

View my notebook with detailed steps here : [top_lowest_10_profitable_states](/top_least_10_profitable_states.ipynb)

### Visualize Data

```python
# Top 10 states
plt.figure(figsize=(15 , 6))
profit_per_top_state_bars = plt.bar(top_ten_profitable_state.index , top_ten_profitable_state['Total Profit'])
plt.bar_label(profit_per_top_state_bars , label_type='edge' , padding=3)
plt.ylabel("Total Profit ($USD)")
plt.title("What are the 10 most profitable states ?")
plt.savefig("figures/question_5(1)_fig.png")
plt.show()
```

![Question 5 (1)](</figures/question_5(1)_fig.png>)

```python
plt.figure(figsize=(15 , 6))
profit_per_least_state_bars = plt.bar(least_10_profitable_state.index , least_10_profitable_state['Total Profit'])
plt.bar_label(profit_per_least_state_bars , label_type='edge' , padding=3)
plt.ylabel("Total Profit ($USD)")
plt.title("What are the 10 least profitable states?")
plt.savefig("figures/question_5(2)_fig.png")
plt.show()
```

![Question 5 (1)](</figures/question_5(2)_fig.png>)

### Insights

As we can determine that most profitable states are **California** , **New York** , **Washington** , **Michigan** with other states The **West** have two states while the **East** have three and **South** two.

While for the lowest states are the likes of **Wyoming** Despite being a **West** State , **West Virginia** , **North and South Dakota** , **Maine**.
