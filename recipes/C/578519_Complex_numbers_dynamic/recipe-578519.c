#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>

int main() {
    _Complex double *c1, *c2, *sum, *prod, *c1csin, *c2csin, *c1ccos, *c2ccos;
    c1 = (_Complex double *) malloc (sizeof(_Complex double));
    c2 = (_Complex double *) malloc (sizeof(_Complex double));
    sum = (_Complex double *) malloc (sizeof(_Complex double));
    prod = (_Complex double *) malloc (sizeof(_Complex double));
    c1csin = (_Complex double *) malloc (sizeof(_Complex double));
    c2csin = (_Complex double *) malloc (sizeof(_Complex double));
    c1ccos = (_Complex double *) malloc (sizeof(_Complex double));
    c2ccos = (_Complex double *) malloc (sizeof(_Complex double));

    *c1 = 1.3 + 2.5i;
    *c2 = -2.7 + 0.3i;
    
    printf("c1 = %g + %gi\n", creal(*c1), cimag(*c1));
    printf("c2 = %g + %gi\n", creal(*c2), cimag(*c2));
    
    *sum = *c1 + *c2;
    *prod = *c1 * (*c2);
    
    printf("c1 + c2 = %g + %gi\n", creal(*sum), cimag(*sum));
    printf("c1 * c2 = %g + %gi\n", creal(*prod), cimag(*prod));
    
    *c1csin = csin(*c1);
    *c2csin = csin(*c1);
    
    printf("csin(c1) = %g + %gi\n", creal(*c1csin), cimag(*c1csin));
    printf("csin(c2) = %g + %gi\n", creal(*c1csin), cimag(*c1csin));

    *c1ccos = ccos(*c1);
    *c2ccos = ccos(*c1);
    
    printf("ccos(c1) = %g + %gi\n", creal(*c1ccos), cimag(*c1ccos));
    printf("ccos(c2) = %g + %gi\n", creal(*c1ccos), cimag(*c1ccos));
    
    return 0;
}
