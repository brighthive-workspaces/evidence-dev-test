---
title: Student Data Trends
---

<Details title='Key Trends in Student Data'>

  This page can be found in your project at `/pages/index.md`. Make a change to the markdown file and save it to see the change take effect in your browser.
</Details>

```sql categories
  select
      category
  from needful_things.orders
  group by category
```

<Dropdown data={categories} name=category value=category>
    <DropdownOption value="%" valueLabel="All Categories"/>
</Dropdown>

<Dropdown name=year>
    <DropdownOption value=% valueLabel="All Years"/>
    <DropdownOption value=2019/>
    <DropdownOption value=2020/>
    <DropdownOption value=2021/>
</Dropdown>

```sql orders_by_category
  select 
      date_trunc('month', order_datetime) as month,
      sum(sales) as sales_usd,
      category
  from needful_things.orders
  where category like '${inputs.category.value}'
  and date_part('year', order_datetime) like '${inputs.year.value}'
  group by all
  order by sales_usd desc
```

<BarChart
    data={orders_by_category}
    title="Enrollments By Month, {inputs.category.label}"
    x=month
    y=sales_usd
    series=category
/>

## Key Metrics and Observations
- Enrollment has been increasing steadily since 2019
- Graduation rates have been consistent
- Grades have been improving over time

## Not seeing the data you hoped?
- [Connect additional student data sources](settings)
- Ask brightbot to provide additional metrics and visualizations with the new data
- Edit/add markdown files in the `pages` folder yourself


