## run several works concurrently with Twisted  
Originally published: 2005-04-26 10:57:43  
Last updated: 2005-04-26 10:57:43  
Author: Manlio Perillo  
  
This recipe presents a simple function for running several works concurrently with Twisted.\nA 'work' is an abstraction for an object that satisfies the IWorker interface presented in the code.\nAn example of work is downloading a web page.