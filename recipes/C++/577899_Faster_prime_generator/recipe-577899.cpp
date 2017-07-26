#include <boost/dynamic_bitset.hpp>
#include <cmath>
#include <iostream>
#include <vector>

/**
 * Generate all prime numbers up to a limit
 * @param limit test for primality up to this limit, not including the limit
 * @return the prime numbers
 */
std::vector<unsigned long> getPrimes( unsigned long limit )
{
  std::vector<unsigned long> primes;
  
  // special cases
  if ( limit <= 5 )
  {
    if ( limit > 2 )
    {
      primes.push_back( 2 );
      if ( limit > 3 )
      {
	primes.push_back( 3 );
      }
    }      
    return primes;
  }
  
  // multiples of 2 and 3 will not be used, just add them by hand
  primes.push_back( 2 );
  primes.push_back( 3 );
  
  // crossed out nonprimes
  boost::dynamic_bitset<> crossOut( limit );
  
  // add primes to result and cross out nonprimes
  unsigned long crossOutLimit = static_cast<unsigned long>( sqrt( limit ) ) + 1;
  unsigned long i = 5;
  for ( ; i < crossOutLimit; i += 6 )
  {
    for ( unsigned long d = 0; d != 4; d += 2 )
    {
      unsigned long num = i + d;
      if ( !crossOut.test( num ) )
      {
	primes.push_back( num );
	for ( unsigned long j = num * num; j < limit; j += num )
	{
	  crossOut.set( j );
	}
      }
    }
  }
  
  // add extra primes to result 
  for ( ; i < limit - 2; i += 6 )
  {
    for ( unsigned long d = 0; d != 4; d += 2 )
    {
      unsigned long num = i + d;
      if ( !crossOut.test( num ) )
      {
	primes.push_back( num );
      }
    }
  }
  
  // one may be missing
  if ( i < limit && !crossOut.test( i ) )
  {
    primes.push_back( i );
  }
  
  return primes;
}

int main()
{
  unsigned long limit = 10000000;
  std::vector<unsigned long> primes = getPrimes( limit );
  std::cout << "Trere are " << primes.size() << " primes below " << limit << "." << std::endl;
  return 0;
}
