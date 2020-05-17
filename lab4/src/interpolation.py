def interpolate (y1, y2, x, x_max, type_of_interpolation):
    if type_of_interpolation == "linear":
        return lin_int (y1, y2, x, x_max)
    elif type_of_interpolation == "spline":
        return spline_int (y1, y2, x, x_max)

def lin_int (y1, y2, x, x_max):
    return y1 + (float (y2 - y1) / x_max) * x

def spline_int (y1, y2, x, x_max):
    a = y1 - y2
    b = y2 - y1
    t = x / x_max
    return (1 - t) * y1 + t * y2 + t * (1 - t) * ((1 - t) * a + t * b)

