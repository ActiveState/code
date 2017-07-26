#include <iostream>
#include <vector>

using namespace std;

typedef unsigned int UI;

const UI MAX_N = 1000000000;
const UI RT_MAX_N = 32000; // square of max prime under this limit should exceed MAX_N
const UI B_SIZE = 20000;   // not sure what optimal value for this is;
                           // currently must avoid overflow when squared

// assumes p, b odd and p*p won't overflow!
void crossOut(UI p, UI b, bool mark[]) {
  UI si = (p - (b % p)) % p;
  if (si & 1)
    si += p;
  if (p*p > b)
    si = max(si, p*p-b);

  for (UI i = si/2; i < B_SIZE/2; i += p)
    mark[i] = true;
  }

// mod 30, (odd) primes have remainders 1,7,11,13,17,19,23,29
// e.g. start with mark[B_SIZE/30]
// and offset[] = {1,7,11...}
// then mark[i] corresponds to 30*(i/8) + b-1 + offset[i%8]
void calcPrimes() {
  int pCount = 1; UI lastP = 2;
  // *** do something with first prime (2) here ***

  vector<UI> smallP; smallP.push_back(2);

  bool mark[B_SIZE/2] = {false};
  for (UI i = 1; i < B_SIZE/2; ++i)
    if (!mark[i]) {
      ++pCount; lastP = 2*i+1;
      // *** do something with the newest prime lastP here ***
      smallP.push_back(lastP);
      if (lastP*lastP <= B_SIZE)
        crossOut(2*i + 1, 1, mark);
      }
    else mark[i] = false;

  for (UI b = 1+B_SIZE; b < MAX_N; b += B_SIZE) {
    for (UI i = 1; smallP[i]*smallP[i] < b+B_SIZE; ++i)
      crossOut(smallP[i], b, mark);
    for (UI i = 0; i < B_SIZE/2; ++i)
      if (!mark[i]) {
        ++pCount; lastP = 2*i + b;
        // *** do something with the newest prime lastP here ***
        if (lastP <= RT_MAX_N)
          smallP.push_back(lastP);
        }
      else mark[i] = false;
    }

  cout << "Found " << pCount << " primes in total.\n";
  cout << "Recorded " << smallP.size() << " small primes, up to " << RT_MAX_N << '\n';
  cout << "Last prime found was " << lastP << '\n';
  }

int main() {
  calcPrimes();
  }
