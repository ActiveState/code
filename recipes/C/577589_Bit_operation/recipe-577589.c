/*
   Copyright 2011 Shao-Chuan Wang <shaochuan.wang AT gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
*/
#include <stdio.h>
#include <stdlib.h>

typedef struct {
  int size;
  unsigned int *b; 
} packed_bits;

#define INT_NBITS (sizeof(unsigned int)*8)
#define INT_MAX_BIT_MASK (1 << (INT_NBITS-1))


packed_bits *new_bits(unsigned int n_int)
{
  packed_bits *p;
  unsigned int *b_array = calloc(n_int, sizeof(unsigned int));
  if (!b_array)
    return NULL;
  p = malloc(sizeof(packed_bits));
  if (!p) {
    free(b_array);
    return NULL;
  }
  p->size = n_int;
  p->b = b_array;
  return p;
}

int left_shift(packed_bits *p)
{
  int i;
  unsigned int *b;
  if (!p)
    return -1;
  b = p->b;
  for (i = p->size-1;i >= 0;i--) {
    b[i] = b[i] << 1;
    if (i-1 >=0 && b[i-1] & INT_MAX_BIT_MASK)
      b[i]++;
  }
  return 0;
}

int right_shift(packed_bits *p)
{
  int i;
  unsigned int *b;
  if (!p)
    return -1;
  b = p->b;
  for (i = 0;i < p->size;i++) {
    b[i] = b[i] >> 1;
    if (i+1 < p->size && (b[i+1] & 1))
      b[i] |= INT_MAX_BIT_MASK;
  }
  return 0;  
}

unsigned int read_bit(packed_bits *p, unsigned int n)
{
  unsigned int offset = n % INT_NBITS;
  unsigned int idx = n / INT_NBITS;
  unsigned int *b;
  if (!p)
    return -1;
  b = p->b;
  return (b[idx] & (1 << offset)) != 0;
}

/* n starts from 0 */
int set_bit(packed_bits *p, unsigned int n)
{
  unsigned int offset = n % INT_NBITS;
  unsigned int idx = n / INT_NBITS;
  unsigned int *b;
  if (!p)
    return -1;
  b = p->b;
  b[idx] |= (1<<offset);
  return 0;
}

int clear_bit(packed_bits *p, unsigned int n)
{
  unsigned int offset = n % INT_NBITS;
  unsigned int idx = n / INT_NBITS;
  unsigned int *b;
  if (!p)
    return -1;
  b = p->b;
  b[idx] &= ~(1<<offset);

  return 0;
}

void print_bits(packed_bits *p)
{
  int j;
  unsigned int *b;
  if (!p)
    return;
  b = p->b;
  for (j = (INT_NBITS * p->size) - 1; j >= 0; j--) {
    printf("%d", read_bit(p, j));
    if (j % INT_NBITS==0)
      printf("\n");
  }
  printf("\n");
  return;
}

int main(int argc, char *argv[])
{
  int n_int = 4;
  packed_bits *p = new_bits(n_int);
  if (!p) {
    fprintf(stderr, "Out of memory!\n");
    return EXIT_FAILURE;
  }
  
  set_bit(p, 1);
  set_bit(p, 127);
  print_bits(p);
  
  return 0;
}
