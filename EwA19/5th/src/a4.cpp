#include "a4.hpp"

void swap( int *a, int *b )
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}


void square_and_root_of_double( double x, double *sq, double *rt )
{
    *sq = x * x;
    *rt = sqrt(x);  // from cmath, included in a4.hpp
}
