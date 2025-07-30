import numpy as np
import math
from .misc import quadraticFormula

class surface:
    def __init__(self, surface):
        """
        Initialize the surface object with another surface object.
        
        Parameters:
            surface (surface): Another surface object to copy the attributes from.
        """
        self.r_x     = surface.r_x
        self.r_y     = surface.r_y
        self.x       = surface.x
        self.y_min   = surface.y_min
        self.y_max   = surface.y_max
        self.verbose = surface.verbose
        
    def __init__(self, r_x, r_y, x, y_min=None, y_max=None, verbose=False):
        """
        Initialize the surface object with the specified parameters.
        
        Parameters:
            r_x (float): x-radius of the surface.
            r_y (float): y-radius of the surface.
            x (float): x-coordinate of the center of the surface.
            y_min (float): minimum y value of the surface
            y_max (float): maximum y value of the surface
            verbose (bool, optional): Flag indicating whether to print verbose output. Default is False.
        
        Raises:
            ValueError: If either r_x or r_y is 0.
        """
        if r_x == 0 or r_y == 0:
            raise ValueError("Neither r_x or r_y can be 0")
        self.r_x     = r_x
        self.r_y     = abs(r_y)
        self.x       = x
        self.verbose = verbose
        
        self.y_min   = y_min
        self.y_max   = y_max
        if self.y_min != None and self.y_min >  abs(self.r_y) and self.verbose: raise ValueError('y_min is greater than abs(r_y)')
        if self.y_max != None and self.y_max < -abs(self.r_y) and self.verbose: raise ValueError('y_max is less than -abs(r_y)')
        if self.y_min != None and self.y_min < -abs(self.r_y) and self.verbose: print('WARNING: y_min is less than -abs(r_y)... aka it does nothing'  ); self.y_min = None
        if self.y_max != None and self.y_max >  abs(self.r_y) and self.verbose: print('WARNING: y_max is greater than abs(r_y)... aka it does nothing'); self.y_max = None
        if self.y_min == None: self.y_min = -self.r_y
        if self.y_max == None: self.y_max =  self.r_y
            
    def get_points(self, nPoints=1e3, safety=1e-10, reverse=False):
        """
        Generate a list of points on the surface.
        
        Parameters:
            nPoints (int, optional): Number of points to generate on the surface.
            safety (float, optional): Small value to ensure points are within the surface bounds. Default is 1e-10.
            reverse (bool, optional): Return points from small to large y-value if False, reverse if True
        
        Returns:
            list: List of (x, y) points on the surface.
        """

        points = []
        
        limits = [self.y_min+safety,self.y_max-safety]
        if reverse:
            limits = [self.y_max-safety, self.y_min+safety]
            
        for y in np.linspace(limits[0], limits[1], int(nPoints)):
            c_1 = 1/self.r_x**2
            c_2 = -2*self.x/self.r_x**2
            c_3 = self.x**2/self.r_x**2 + y**2/self.r_y**2 - 1
            x = quadraticFormula(self.r_x/abs(self.r_x),c_1,c_2,c_3)
            if x != None:
                points.append((x,y))

        return points
    
    def get_maxTheta(self, opticalRay):
        """
        Calculate the maximum theta bounds between the surface and an optical ray.
        
        Parameters:
            opticalRay (opticalRay): An optical ray object.
        
        Returns:
            list: List of maximum theta bounds between the surface and the optical ray.
        
        Raises:
            ValueError: If the optical ray's x-coordinate is greater than the surface's x-coordinate.
        """
        bounds = []
        
        deltaX = self.x - opticalRay.x
        if deltaX < 0:
            raise ValueError('Optical ray must have x<x_l')
            
        deltaY = self.r_y - opticalRay.y
        bounds.append(math.atan(deltaY/deltaX))
                      
        deltaY = -self.r_y - opticalRay.y
        bounds.append(math.atan(deltaY/deltaX))
        
        return bounds
    
    def get_point_fromY(self, y, errors=[-1e-5,1e-5]):
        sign = self.r_x/abs(self.r_x)
        c_1 = 1/self.r_x**2
        c_2 = -2*self.x/self.r_x**2
        c_3 = self.x**2/self.r_x**2+y**2/self.r_y**2-1
        
        x = quadraticFormula(sign,c_1,c_2,c_3)
        
        nTry = 0
        while x == None and nTry < 2:
            c_3 = self.x**2/self.r_x**2+(y+errors[nTry])**2/self.r_y**2-1
            x = quadraticFormula(sign,c_1,c_2,c_3)
            nTry = nTry + 1
        
        if x == None:
            return None
        else:
            return (x,y)