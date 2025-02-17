// Copyright (c) 1999  
// Utrecht University (The Netherlands),
// ETH Zurich (Switzerland),
// INRIA Sophia-Antipolis (France),
// Max-Planck-Institute Saarbruecken (Germany),
// and Tel-Aviv University (Israel).  All rights reserved. 
//
// This file is part of CGAL (www.cgal.org); you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public License as
// published by the Free Software Foundation; either version 3 of the License,
// or (at your option) any later version.
//
// Licensees holding a valid commercial license may use this file in
// accordance with the commercial license agreement provided with the software.
//
// This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
// WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
//
// $URL: https://github.com/CGAL/cgal/blob/releases/CGAL-4.14.1/Homogeneous_kernel/include/CGAL/Simple_homogeneous.h $
// $Id: Simple_homogeneous.h 0698f79 %aI Sébastien Loriot
// SPDX-License-Identifier: LGPL-3.0+
// 
//
// Author(s)     : Stefan Schirra, Sylvain Pion
 
#ifndef CGAL_SIMPLE_HOMOGENEOUS_H
#define CGAL_SIMPLE_HOMOGENEOUS_H

#include <CGAL/Homogeneous/Homogeneous_base.h>
#include <CGAL/Handle_for.h>
#include <CGAL/Kernel/Type_equality_wrapper.h>
#include <CGAL/Quotient.h>

namespace CGAL {

template < typename RT_, typename FT_, typename Kernel >
struct Homogeneous_base_no_ref_count
  : public Homogeneous_base<RT_, FT_, Kernel >
{
    typedef RT_                                           RT;
    typedef FT_                                           FT;

    // The mechanism that allows to specify reference-counting or not.
    template < typename T >
    struct Handle { typedef T    type; };

    template < typename Kernel2 >
    struct Base {
        typedef Homogeneous_base_no_ref_count<RT_,FT_,Kernel2> Type;
    };
};

template < typename RT_, typename FT_ = Quotient<RT_> >
struct Simple_homogeneous
  : public Type_equality_wrapper<
                Homogeneous_base_no_ref_count<RT_, FT_,
                                              Simple_homogeneous<RT_, FT_> >,
                Simple_homogeneous<RT_, FT_> >
{};

} //namespace CGAL

#endif // CGAL_SIMPLE_HOMOGENEOUS_H
