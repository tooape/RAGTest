---
created: 
tags: 
Related Pages: 
aliases:
---
# Krithika's notes
1. Data Mining - Finding meaningful patterns in present and historical data 1. do they bring their own data? 2. do we integrate with other systems where they may have this data to connect into our system? 3. Sku level insights about revenue and conversion - cart showing the lifecycle of an interaction from impression->view->click->add to cart->purchase. But is this what AJO does today? 4. On the flip side, performance of a rec unit over time - on a chart 5. First time versus repeat shoppers 6. Explain API 7. Variant test for intelligent strategies 2. Natural Language Processing 3. Semantic Search (turn on or off option) 3. Machine Learning - Deeper understanding of the data to power their search and Prex in addition to the existing types 1. Cart abandonment rate? - segmentation based on churn 2. Forecast demand? - what was sales/conversion like last year at the same time? 3. Dynamic pricing? 4. Expanding current rec algorithms (e.g- bought together in the same order) 5. Analyze catalog and recommend data organization templates for the merchant? 1. What are we modeling this on? Do we have a base template that can serve as a starting point? 2. What basic recs/search configs can we recommend? 6. Eventing based on category browse, plug search terms into ML to influence recs 7. Bring your own ML algorithm -

her [page](https://wiki.corp.adobe.com/display/~krchandr/Data+Vision+for+CCDM+and+beyond)


# My notes
## Relevance auto tuner
> As a merchant admin who is not an expert in search and data, i'd like to be shown where my search is underperforming and receive actionable info about how I might fix it. This way I can improve my site, keep tabs on search performance without having to consult outside help, or raise a support ticket. 


### Milestone 1 - Knowing bad data when we see it 
The beating heart of the solution to this problem is being able to identify queries which have poor ranking or recall, and the SKUs that are causing these queries to be so low performing. 

Queries which are low performing might exhibit: 
- CTR much lower than site average 
	- Shoppers are not buying anything from these queries
- CTR coming from products in low ranking 
	- Shoppers are having to scroll around to find what they wanted
- Strong performing products not being bought 
	- SKUs with good sales history are not being bought in this result set



### Milestone 2 - 