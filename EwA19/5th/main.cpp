#include <cstdio>
#include "a2.hpp"
#include "a3.hpp"

#define N_A2


int main()
{
    int i, a, b;
    double x, y;

    a = 1337;
    b = 42;
    x = 6.283;
    y = 1.414;

#ifndef N_A2
    printf("AUFGABE 2\n==========\n");
    printf("a = %d, b = %d\n", a, b);
    printf("sum(a, b) = %d\n", sum(a, b));
    printf("diff(a, b) = %d\n", diff(a, b));
    printf("prod(a, b) = %d\n", prod(a, b));
    printf("quod(a, b) = %d\n", quod(a, b));
    printf("mod(a, b) = %d\n\n", mod(a, b));
    printf("x = %f, y = %f, n = %d\n", x, y, b);
    printf("x^y = %e\n", pow_wrapper(x, y));
    printf("sqrt(|x|)/ln(n) = %f\n", sqrt_of_abs_over_log(x, b));
    printf("max(x, y) = %f\n", my_max(x, y));
    printf("erf(x) = %e\n", erf_wrapper(x));
    printf("%d! = %ld\n", b, fac(b));
    printf("%d is%s even...\n", a, int_is_even(a) ? "" : " not");
    printf("%d is%s even...\n", b, int_is_even(b) ? "" : " not");
    printf("\nEven Integers from [1, 100]...\n");
    for ( i = 1; i <= 100; ++i )
        if ( int_is_even(i) )
            printf("%d\n", i);
    printf("\n\n\n");
#endif

    std::vector<int> fibs = make_fibs( b );
    printf("AUFGABE 3\n==========\n");
    printf("fibonacci numbers up to %d:\n", b);
    for ( int f : fibs )
        printf("%d\n", f);

    return 0;
}
