// Copyright (c) 2010 GeometryFactory (France).
// All rights reserved.
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
// $URL: https://github.com/CGAL/cgal/blob/releases/CGAL-4.14.1/Intersections_3/include/CGAL/Intersections_3/Ray_3_Tetrahedron_3.h $
// $Id: Ray_3_Tetrahedron_3.h 1622410 %aI Andreas Fabri
// SPDX-License-Identifier: LGPL-3.0+
//
//
// Author(s)     : Sebastien Loriot
//

#ifndef CGAL_INTERSECTIONS_3_RAY_3_TETRAHEDRON_3_H
#define CGAL_INTERSECTIONS_3_RAY_3_TETRAHEDRON_3_H

#include <CGAL/Ray_3.h>
#include <CGAL/Tetrahedron_3.h>

#include <CGAL/Intersections_3/internal/Tetrahedron_3_Unbounded_3_do_intersect.h>

namespace CGAL {
  CGAL_DO_INTERSECT_FUNCTION(Ray_3, Tetrahedron_3, 3)
}

#endif // CGAL_INTERSECTIONS_3_RAY_3_TETRAHEDRON_3_H
