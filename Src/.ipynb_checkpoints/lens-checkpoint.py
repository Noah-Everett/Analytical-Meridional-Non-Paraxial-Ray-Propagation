import numpy as np

class lens:
    def __init__(self, lens):
        """
        Initialize the lens object with another lens object.
        
        Parameters:
            lens (lens): Another lens object to copy the attributes from.
        """
        self.surface_1       = lens.surface_1
        self.surface_2       = lens.surface_2
        self.refractiveIndex = lens.refractiveIndex
        self.verbose         = lens.verbose
        self.__sortSurfaces()
        
    def __init__(self, surface_1, surface_2, refractiveIndex, verbose=False):
        """
        Initialize the lens object with the specified parameters.
        
        Parameters:
            surface_1 (surface): The first surface of the lens.
            surface_2 (surface): The second surface of the lens.
            refractive_index (float): The refractive index of the lens material.
            verbose (bool, optional): Flag indicating whether to print verbose output. Default is False.
        """
        self.surface_1       = surface_1
        self.surface_2       = surface_2
        self.refractiveIndex = refractiveIndex
        self.verbose         = verbose
        self.__sortSurfaces()
                
    def __sortSurfaces(self):
        """
        Sort the surfaces of the lens based on their x-coordinate.
        This ensures that surface_1 is located to the left of surface_2.
        """
        if self.surface_1.x + self.surface_1.r_x > self.surface_2.x + self.surface_2.r_x:
            self.surface_1, self.surface_2 = self.surface_2, self.surface_1
    
    def get_points(self, nPoints):
        """
        Get the points on each surface of the lens.
        
        Parameters:
            nPoints (int): Number of points to generate on each surface.
        
        Returns:
            tuple: Two lists, each containing (x, y) points on the respective surfaces.
        """
        points = []
        
        for point in self.surface_1.get_points(nPoints):
            points.append(point)
        
        points.append(self.surface_1.get_point_fromY(self.surface_1.y_max))
        points.append(self.surface_2.get_point_fromY(self.surface_2.y_max))

        for point in self.surface_2.get_points(nPoints,reverse=True):
            points.append(point)
            
        points.append(self.surface_2.get_point_fromY(self.surface_2.y_min))
        points.append(self.surface_1.get_point_fromY(self.surface_1.y_min))
        
        return points