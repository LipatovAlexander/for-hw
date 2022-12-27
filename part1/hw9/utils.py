import math
import numpy as np
from HSV.hsv import hsv_to_rgb


def hsv2rgb(h, s, v):
    h /= 360.
    s /= 100.
    v /= 100.
    r, g, b = hsv_to_rgb(h, s, v)
    return round(r * 255), round(g * 255), round(b * 255)
    
    
def pol2cart(radius, angle):
    x = radius * math.cos(math.radians(angle))
    y = radius * math.sin(math.radians(angle))
    return x, y


def cart2pol(x, y):
    radius = math.sqrt(x * x + y * y)
    theta = math.atan(y / x)
    theta = 180 * theta / math.pi
    if np.isnan(theta):
        theta = 0
    if x < 0:
        theta = 180 + theta
    if x > 0 and y < 0:
        theta = 270 + (90 + theta)
    if theta < 0:
        theta = 360 + theta
    return radius, theta


def points_in_circle(radius, x0=0, y0=0):
    x_ = np.arange(x0 - radius - 1, x0 + radius + 1, dtype=int)
    y_ = np.arange(y0 - radius - 1, y0 + radius + 1, dtype=int)
    x, y = np.where((x_[:,np.newaxis] - x0)**2 + (y_ - y0)**2 <= radius**2)
    # x, y = np.where((np.hypot((x_-x0)[:,np.newaxis], y_-y0)<= radius)) # alternative implementation
    for x, y in zip(x_[x], y_[y]):
        yield x, y