#pragma once

#include <string>


// abstract base class, i.e. there can be no instance of this class
class Shape {
public:
    // constructor
    Shape( double x, double y, std::string type );

    // virtual function (indicated by `= 0`) must be overridden by any
    // non-abstract derived class
    virtual double compute_area() = 0;

    // member methods
    std::string get_type();
    double get_x();
    double get_y();
    void set_x( double new_x );
    void set_y( double new_y );

protected:
    // member variables
    // `protected`: can be accessed by derived classes
    double m_x, m_y;
    std::string m_type;
};



// non-abstract derived classes `Rectangle` and `Triangle` with overriden
// method

class Rectangle : public Shape {
public:
    Rectangle( double a, double b );
    double compute_area() override;
};


class Triangle : public Shape {
public:
    Triangle( double height, double base );
    double compute_area() override;
};
