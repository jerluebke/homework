#include "a5.hpp"


// Shape

Shape::Shape( double x, double y, std::string type )
    : m_x( x ), m_y( y ), m_type( type )
{}

std::string Shape::get_type()
{ return m_type; }

double Shape::get_x()
{ return m_x; }

double Shape::get_y()
{ return m_y; }

void Shape::set_x( double new_x )
{ m_x = new_x; }

void Shape::set_y( double new_y )
{ m_y = new_y; }



// Rectangle

Rectangle::Rectangle( double a, double b )
    : Shape( a, b, "Rectangle" )
{}

double Rectangle::compute_area()
{ return m_x * m_y; }



// Triangle

Triangle::Triangle( double height, double base )
    : Shape( height, base, "Triangle" )
{}

double Triangle::compute_area()
{ return m_x * m_y / 2.0; }
