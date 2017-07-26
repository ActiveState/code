## Metropolis-Hastings SamplerOriginally published: 2005-05-13 15:58:00 
Last updated: 2005-05-13 15:58:00 
Author: Flávio Codeço Coelho 
 
The Metropolis-Hastings Sampler is the most common Markov-Chain-Monte-Carlo (MCMC) algorithm used to sample from arbitrary probability density functions (PDF). Suppose you  want to simulate samples from a random variable which can be described by an arbitrary PDF, i.e., any function which integrates to 1 over a given interval. This algorithm will do just that, as illustrated by the Plot done with Matplotlib. Notice how the samples follow the theoretical PDF.