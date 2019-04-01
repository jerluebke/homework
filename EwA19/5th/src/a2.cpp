#include "a2.hpp"

// (a)

int sum( int a, int b )
{ return a + b; }

int diff( int a, int b )
{ return a - b; }

int prod( int a, int b )
{ return a * b; }

int quod( int a, int b )
{ return a / b; }

int mod( int a, int b )
{ return a % b; }


// (b)

double pow_wrapper( double x, double y )
{ return pow(x, y); }

double sqrt_of_abs_over_log( double x, int n )
{ return sqrt(fabs(x)) / log(n); }

double my_max( double x, double y )
{ return x > y ? x : y; }

double erf_wrapper( double x )
{ return erf(x); }

unsigned long fac( unsigned int n )
{
    unsigned int i = 1;
    unsigned long res = 1;
    for ( i = 1; i <= n; ++i ) {
        res *= i;
    }
    return res;
}

bool int_is_even( int n )
{ return !(n&1); }
