import math
import numpy as np


class calculation:
    def __init__(self):
        pass

    def find_slope_and_intercept(self,X, y):
    
        """
        Function: find_slope_and_intercept
        Description: Compute slope and intercept for linear regression.

        Inputs:
            X (list): List of independent variables.
            y (list): List of dependent variables.

        Output:
            float: Slope.
        """
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)

        if len(X) != len(y):
            raise ValueError("X and y must have the same length.")

        if len(set(X)) == 1:
            return np.inf, X[0]

        X_bias = np.c_[np.ones((X.shape[0], 1)), X]
        try:
            params = np.linalg.inv(X_bias.T @ X_bias) @ X_bias.T @ y
        except np.linalg.LinAlgError:
            raise ValueError("Cannot compute linear regression; check input data.")

        return params[1], params[0]


    def point_to_point(self,point1, point2):
    
        """
        Function: point_to_point
        Description: Compute Euclidean distance between two points.

        Inputs:
            point1 (list): The first point.
            point2 (list): The second point.

        Output:
            float: The Euclidean distance between the two points.
        """
        if len(point1) != len(point2):
            raise ValueError("Both points must have the same dimension.")
        distance = math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)))
        return distance


    def point_to_line_segment(self,point, line):
    
        """
        Function: point_to_line_segment
        Description: Compute Euclidean distance, angle and nearest point from a point to a line segment.

        Parameters:
            point (list): The point.
            line (list): The line segment defined by two endpoints.

        Returns:
            Tuple[float, float, Tuple[float, float]]: (distance, angle_deg, nearest_point).
        """
        p = np.array(point, dtype=float)
        a, b = map(np.array, line)
        v = b - a
        l2 = np.dot(v, v)
        if np.isclose(l2, 0):
            raise ValueError("The two endpoints of the segment cannot be the same.")

        t = np.dot(p - a, v) / l2
        t = np.clip(t, 0, 1)
        proj = a + t * v
        dist = np.linalg.norm(p - proj)

        vec_to_p = proj - p
        if np.isclose(np.linalg.norm(vec_to_p), 0) or np.isclose(np.linalg.norm(v), 0):
            angle = 0.0
        else:
            cosang = np.dot(vec_to_p, v) / (np.linalg.norm(vec_to_p) * np.linalg.norm(v))
            angle = math.degrees(math.acos(np.clip(cosang, -1, 1)))

        return dist, angle, (proj[0], proj[1])


    def point_to_line(self,point, line):
    
        """
        Function: point_to_line
        Description: Compute Euclidean distance, angle and nearest point from a point to a line.

        Parameters:
            point (list): The point.
            line (list): The line defined by (slope, intercept).

        Returns:
            Tuple[float, float, Tuple[float, float]]: (distance, angle_deg, nearest_point).
        """
        
        slope, intercept = line
        x0, y0 = point

        if math.isinf(slope):
            x_proj = intercept
            y_proj = y0
        else:
            perp_slope = -1 / slope
            perp_int = y0 - perp_slope * x0
            x_proj = (perp_int - intercept) / (slope - perp_slope)
            y_proj = slope * x_proj + intercept

        dist = math.hypot(x0 - x_proj, y0 - y_proj)
        vec = (x_proj - x0, y_proj - y0)
        base = (1, slope) if not math.isinf(slope) else (0, 1)
        mag_vec = math.hypot(*vec)
        mag_base = math.hypot(*base)
        if np.isclose(mag_vec, 0) or np.isclose(mag_base, 0):
            angle = 0.0
        else:
            cosang = (vec[0]*base[0] + vec[1]*base[1]) / (mag_vec * mag_base)
            angle = math.degrees(math.acos(np.clip(cosang, -1, 1)))

        return dist, angle, (x_proj, y_proj)


    def line_to_line(self,line1, line2):
    
        """
        Function: line_to_line
        Description: Compute Euclidean distance, and closest points between two lines.

        Parameters:
            line1 (list): The first line defined by (x1, y1, x2, y2).
            line2 (list): The second line defined by (x1, y1, x2, y2).

        Returns:
            Tuple[float, Tuple[float, float], Tuple[float, float]]: (distance, point_on_line1, point_on_line2).
        """
        p1, q1 = map(np.array, line1, dtype=float)
        p2, q2 = map(np.array, line2, dtype=float)
        d1, d2 = q1 - p1, q2 - p2
        cross = np.cross(d1, d2)
        if np.isclose(cross, 0):
            t = np.dot(p2 - p1, d1) / np.dot(d1, d1)
            t = np.clip(t, 0, 1)
            c1 = p1 + t * d1
            dists = [(np.linalg.norm(c1 - p2), p2), (np.linalg.norm(c1 - q2), q2)]
            c2 = min(dists, key=lambda x: x[0])[1]
            return float(np.linalg.norm(c1 - c2)), (c1[0], c1[1]), (c2[0], c2[1])
        t1 = np.cross((p2 - p1), d2) / cross
        t2 = np.cross((p2 - p1), d1) / cross
        t1, t2 = np.clip(t1, 0, 1), np.clip(t2, 0, 1)
        c1 = p1 + t1 * d1
        c2 = p2 + t2 * d2
        distance = float(np.linalg.norm(c1 - c2)), (c1[0], c1[1]), (c2[0], c2[1])
        return distance

    def find_angle_and_intersection(self,line1, line2):
    
        """
        Function: find_angle_and_intersection
        Description: Compute the angle between two lines in degrees, and the intersection point.

        Parameters:
            line1 (Tuple[float, float]): The first line defined by (m, b).
            line2 (Tuple[float, float]): The second line defined by (m, b).

        Returns:
            Tuple[float, Tuple[float, float]]: (angle, intersection).
        """
        m1, b1 = line1
        m2, b2 = line2
        if np.isclose(m1, m2):
            return 0.0, None
        if math.isinf(m1) and m2 == 0:
            return 90.0, (b1, b2)
        if math.isinf(m2) and m1 == 0:
            return 90.0, (b2, b1)
        x_int = (b2 - b1) / (m1 - m2)
        y_int = m1 * x_int + b1
        if np.isclose(m1*m2, -1):
            angle = 90.0
        else:
            angle = math.degrees(abs(math.atan((m2 - m1)/(1 + m1*m2))))
        return angle, (x_int, y_int)


    def get_slope_at_certain_angle(self,line=None, slope_intercept=None, angle_degrees=0):
    
        """
        Function: get_slope_at_certain_angle
        Description: Compute the slope of a line after rotating it by a certain angle from the horizontal.
        
        Parameters:
            line (Tuple[Tuple[float, float], Tuple[float, float]]): The line defined by two points.
            slope_intercept (Tuple[float, float]): The line defined by its slope and intercept.
            angle_degrees (float): The angle in degrees to rotate the line.
        
        Returns:
            Tuple[float, float]: The new slope and intercept of the rotated line.

        """
        if line is None and slope_intercept is None:
            raise ValueError("Either 'line' or 'slope_intercept' must be provided.")
        if line is not None:
            (x1, y1), (x2, y2) = line
            dx, dy = x2 - x1, y2 - y1
            if dx == 0 and dy == 0:
                raise ValueError("The two points are the same; cannot form a vector.")
            slope = np.inf if dx == 0 else dy/dx
            mag = math.hypot(dx, dy)
            unit = (dx/mag, dy/mag)
            intercept = None if slope == np.inf else y1 - slope*x1
        else:
            slope, intercept = slope_intercept
            if slope == np.inf:
                unit = (0, 1)
            elif slope == 0:
                unit = (1, 0)
            else:
                mag = math.hypot(1, slope)
                unit = (1/mag, slope/mag)
        rad = math.radians(angle_degrees)
        ux, uy = unit
        nx = ux*math.cos(rad) - uy*math.sin(rad)
        ny = ux*math.sin(rad) + uy*math.cos(rad)
        new_slope = np.inf if np.isclose(nx, 0) else ny/nx
        if slope_intercept is not None:
            if new_slope == np.inf or new_slope == 0:
                return new_slope, intercept
            # rotate intercept about origin
            rx = -intercept*math.sin(rad)
            ry = intercept*math.cos(rad)
            new_int = ry - new_slope*rx
            return new_slope, new_int
        return new_slope, intercept


    def calculate_new_line(self,line, offset_distance=None, offset_point=None):

        """
        Function: calculate_new_line
        Description: Calculate a new line parallel to the given line, offset by a specified distance or through a specific point.

        Parameters:
            line (tuple): A tuple containing the slope and intercept of the line (slope, intercept).
            offset_distance (float, optional): The perpendicular distance to offset the line.
            offset_point (tuple, optional): A point (x, y) through which the new line should pass.

        Returns:
            tuple: A tuple containing the slope and intercept of the new line.
        """

        from numpy import sqrt
        slope, intercept = line
        if slope == np.inf:
            if offset_point is not None:
                return np.inf, offset_point[0]
            if offset_distance is not None:
                return np.inf, intercept + offset_distance
            raise ValueError("Provide offset_distance or offset_point for vertical line.")
        if offset_point is not None:
            x, y = offset_point
            new_int = y - slope*x
        elif offset_distance is not None:
            norm = math.hypot(slope,  -1)
            new_int = intercept + offset_distance*norm
        else:
            raise ValueError("Provide offset_distance or offset_point.")
        return slope, new_int

