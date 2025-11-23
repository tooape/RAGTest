---
pageType: Misc
tags:
  - books
---
---
#books

# The book
["What are embeddings" by Vicki Boykis](http://vickiboykis.com/what_are_embeddings/)

- Abstract: 
	- "Over the past decade, embeddings — numerical representations of machine learning features used as input to deep learning models — have become a foundational data structure in industrial machine learning systems. TF-IDF, PCA, and one-hot encoding have always been key tools in machine learning systems as ways to compress and make sense of large amounts of textual data. However, traditional approaches were limited in the amount of context they could reason about with increasing amounts of data. As the volume, velocity, and variety of data captured by modern applications has exploded, creating approaches specifically tailored to scale has become increasingly important.
	- Google’s Word2Vec paper made an important step in moving from simple statistical representations to semantic meaning of words. The subsequent rise of the Transformer architecture and transfer learning, as well as the latest surge in generative methods has enabled the growth of embeddings as a foundational machine learning data structure. This survey paper aims to provide a deep dive into what embeddings are, their history, and usage patterns in industry."


# Notes
---
## 1. Recommendation as a business problem 
All machine learning systems can be examined in how they solve four critical components: 
1. Input data 
	1. processing from a DB or stream from an application
2. Feature (read: attribute) Engineering 
	1. Examining the data and cleaning it to select the attributes we want to include in our platform
		1. User, geo, clicks on X, etc
	2. Usually the longest step 
3. Model building 
	1. Selecting the important attributes and training the model, iterating and examining until there's an acceptable model. 
4. Model Serving 
	1. How do we serve production users our model. 

### Three types of learning 
- Supervised 
	- Single true answer, model can be evaluated deterministically 
- Unsupervised 
	- No single answer
- Reinforcement 
	- we have an agent moving through an environment and we’d like to understand how to optimally move them through a given environment using explore-exploit techniques
![[Screen Shot 2023-07-27 at 3.02.56 PM.png]]

### Training the model 
- Hyperparameters - parameters whos values control the learning *process*
	- Basically, anything in machine learning and deep learning that you decide their values or choose their configuration before training begins and whose values or configuration will remain the same when training ends is a hyperparameter.
	- Examples
		- Train-test split ratio
		- Learning rate in optimization algorithms (e.g. gradient descent)
		- Choice of optimization algorithm (e.g., gradient descent, stochastic gradient descent, or Adam optimizer)
- Parameters are internal to the model. 
	- they are learned or estimated purely from the data during training as the algorithm used tries to learn the mapping between the input features and the labels or targets.
	- Model training typically starts with parameters being initialized to some values (random values or set to zeros). As training/learning progresses the initial values are updated using an optimization algorithm (e.g. gradient descent). The learning algorithm is continuously updating the parameter values as learning progress but hyperparameter values set by the model designer remain unchanged.
	- At the end of the learning process, model parameters are what constitute the model itself.
	- Examples of parameters
		- The coefficients (or weights) of linear and logistic regression models.
		- Weights and biases of a nn
		- The cluster centroids in clustering
Given some ammount of data we may use to create a model, we will split it into 3 parts. 
- Training data
- Testing data
	- Evaluate the final model with data it's never seen before 
- Validation data 
	- Check our hyperparameters during the model training phase.
### Types of recommenders
- Collaborative filtering 
	- Neighborhood models 
	- matrix factorization 
		- represent users and items as low dimensional vectors 
- Content filtering 
	- uses metadata as additional inputs 
	- useful for cold start on user data
	- can be combined with collab 
- Learn to Rank 
	- learn to rank items in relation to eachother based on known set of preferred rankings. 
- Neural recs
	- using neural networks
	- BERT, Word2Vec

### From words to vectors 
Main steps in any NLP task 
- Encoding 
	- We need a way to represent our non numerical, multimodal data as numbers 
- Vectors
	- we need a way to store the data we've encoded and perform mathematical functions on them
	- Floating point representations 
- Lookup matrices (aka hash table, attention)
	- We use hash maps to to map words to numbers

## 2. Historical Encoding Approaches 
- older methods include: 
	- TF-IDF
	- bag of words
	- LSA
	- LDA
- All count based models focused on counting the occurrence of some term in some text. 
- Encoding methods
	- Ordinal
	- Indicator
	- One-hot
	- 