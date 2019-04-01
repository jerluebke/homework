#include <cstdio>
#include "a2.hpp"
#include "a3.hpp"
#include "a4.hpp"
#include "a5.hpp"


// remove comments to disable certain parts in the main function
// #define N_A2
// #define N_A3
// #define N_A4
// #define N_A5


// Polymorphism: function is defined for abstract base class, can be called
// with instances of any derived class
void print_shape_properties( Shape *s )
{
    // s->get_type returns a std::string
    // printf requires a c-style string (i.e. char array), which is returned by
    // .data()
    printf("%s with %f, %f has area %f\n",
            s->get_type().data(), s->get_x(), s->get_y(), s->compute_area());
}


int main()
{
    int i, a, b;
    double x, y, square, root;

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


#ifndef N_A3
    std::vector<int> fibs = make_fibs( b );
    printf("AUFGABE 3\n==========\n");
    printf("fibonacci numbers up to %d:\n", b);

    // C++11: for-each loop
    for ( int f : fibs )
        printf("%d\n", f);

    printf("\n\n\n");
#endif


#ifndef N_A4
    printf("AUFGABE 4\n==========\n");
    printf("a = %d, b = %d\n", a, b);
    printf("swapping...\n");
    swap(&a, &b);
    printf("a = %d, b = %d\n", a, b);

    square_and_root_of_double(0.1, &square, &root);
    printf("\nx = %f, x^2 = %f, sqrt(x) = %f\n", 0.1, square, root);
    printf("\n\n\n");
#endif


#ifndef N_A5
    // C++11 constructor call with {...}
    Rectangle rect( a, b );
    Triangle tri( x, y );

    printf("AUFGABE 5\n==========\n");
    print_shape_properties( &rect );
    print_shape_properties( &tri );
    printf("\n\n\n");
#endif

    return 0;
}
