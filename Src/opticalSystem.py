from .surface import surface
from .lens import lens

class opticalSystem:
    def __init__(self, lenses, finalSurface, refractiveIndex, verbose=False):
        """
        Initialize the optical system object with the specified parameters.
        
        Parameters:
            lenses (list): List of lens objects.
            finalSurface (surface): The final surface of the optical system.
            refractiveIndices (list): List of refractive indices of the lenses and the final surface.
            verbose (bool, optional): Flag indicating whether to print verbose output. Default is False.
        """
        self.lenses       = lenses
        self.finalSurface = finalSurface
        self.verbose      = verbose
        self.__sort_lenses()
        self.__check_lensOverlap()
        self.__check_lensOverlap_finalSurface()
        self.__check_finalSurface()
        self.surfaces = []
        
        for lens in lenses:
            self.surfaces.append(lens.surface_1)
            self.surfaces.append(lens.surface_2)
        self.surfaces.append(self.finalSurface)
        self.__check_surfaces_length()
        
        self.refractiveIndices = [refractiveIndex]
        for lens in lenses:
            self.refractiveIndices.append(lens.refractiveIndex)
            self.refractiveIndices.append(refractiveIndex)
    
    def add_lens(self, lens):        
        """
        Add a lens to the optical system.
        
        Parameters:
            lens (lens): The lens to be added.
        """
        self.lenses.append(lens)
        self.__sortLenses()
        self.__check_lensOverlap()
        self.__check_lensOverlap_finalSurface()
        self.__check_finalSurface()
        self.__check_surfaces_length()
        self.__update_surfaces_order(lens)
    
    def __sort_lenses(self):
        """
        Sort the lenses in ascending order based on the x-coordinate of the first surface.
        """
        self.lenses.sort(key=lambda lens: lens.surface_1.x + lens.surface_1.r_x)

    def __check_lensOverlap(self):
        """
        Check if there is any overlap between adjacent lenses.
        
        Returns:
            bool: True if there is no overlap, False otherwise.
        
        Raises:
            ValueError: If lens overlap is detected.
        """
        for i in range(len(self.lenses) - 1):
            lens_1 = self.lenses[i]
            lens_2 = self.lenses[i + 1]
            surface_1 = lens_1.surface_2
            surface_2 = lens_2.surface_1
            if surface_1.x + surface_1.r_x > surface_2.x + surface_2.r_x:
                raise ValueError("Lens overlap detected")
            surface_1_points = surface_1.get_points(2)
            surface_2_points = surface_2.get_points(2)
            if surface_1_points[0][0] > surface_2_points[0][0]:
                raise ValueError("Lens overlap detected")
                
        return True
    
    def __check_lensOverlap_finalSurface(self):
        """
        Check if there is any overlap between the final surface and the last lens.
        
        Returns:
            bool: True if there is no overlap, False otherwise.
        
        Raises:
            ValueError: If lens overlap is detected.
        """
        lastLensSurface = self.lenses[-1].surface_2.r_x + self.lenses[-1].surface_2.x
        if lastLensSurface > self.finalSurface.r_x + self.finalSurface.x:
            raise ValueError("Lens overlap detected")
        
        surface_1_points = self.lenses[-1].surface_2.get_points(2)
        surface_2_points = self.finalSurface.get_points(2)
        if surface_1_points[0][0] > surface_2_points[0][0]:
            raise ValueError("Lens overlap detected")
            
        return True
    
    def __check_finalSurface(self):
        """
        Check if the final surface has the greatest radius + x-coordinate among all surfaces.
        
        Returns:
            bool: True if the condition is met, False otherwise.
        
        Raises:
            ValueError: If the condition is not met.
        """
        lastLensSurface = self.lenses[-1].surface_2.r_x + self.lenses[-1].surface_2.x
        if lastLensSurface > self.finalSurface.r_x + self.finalSurface.x:
            raise ValueError("Final surface does not have greatest radius+x")
            
        return True
    
    def __update_surfaces_order(self, lens):        
        """
        Update the order of the surfaces after adding a new lens.
        
        Parameters:
            lens (lens): The newly added lens.
        """
        # O(N) (linear) implementation
        # could use bisection to make faster for large N
        for surface in self.surfaces:
            if surface.r_x + surface.x > lens.surface_1.r_x + lens.surface_2.x:
                self.surfaces.append(lens_surface_1)
                self.surfaces.append(lens_surface_2)
                break
                
    def __check_surfaces_length(self):
        """
        Check if the list of surfaces is empty.
        
        Raises:
            ValueError: If the list of surfaces is empty.
        """
        if len(self.surfaces) == 0:
            raise ValueError("Surfaces cannot be empty")
            
    def get_points_surfaces(self, nPoints):
        """
        Get the points on each surface of the optical system.
        
        Parameters:
            nPoints (int): Number of points to generate on each surface.
        
        Returns:
            list: List of lists, where each inner list contains (x, y) points on a surface.
        """
        points = []
        for surface in self.surfaces:
            points.append(surface.get_points(nPoints))
            
        return points
    
    def get_points_lenses(self, nPoints):        
        """
        Get the points on each lens of the optical system.
        
        Parameters:
            nPoints (int): Number of points to generate on each surface.
        
        Returns:
            list: List of lists, where each inner list contains (x, y) points on a lens.
        """
        points = []
        for lens in self.lenses:
            points.append(lens.get_points(nPoints))
        points.append(self.surfaces[-1].get_points(nPoints))
            
        return points
    
def constructOpticalSystem(lens_parameters, verbose=False):
    """
    Construct the optical system from the specified parameters.
    """
    surfaces = []
    lenses   = []
    for nLens in range(len(lens_parameters)):
        if nLens != len(lens_parameters)-1:
            surfaces.append(surface(lens_parameters[nLens][0][0],lens_parameters[nLens][0][1],
                                    lens_parameters[nLens][4] - lens_parameters[nLens][0][0] - lens_parameters[nLens][1]/2,
                                    lens_parameters[nLens][0][2],lens_parameters[nLens][0][3],verbose=verbose))
            surfaces.append(surface(lens_parameters[nLens][3][0],lens_parameters[nLens][3][1],
                                    lens_parameters[nLens][4] - lens_parameters[nLens][3][0] + lens_parameters[nLens][1]/2,
                                    lens_parameters[nLens][3][2],lens_parameters[nLens][3][3],verbose=verbose))
            lenses.append(lens(surfaces[-2],surfaces[-1],lens_parameters[nLens][2],verbose)) 
        else:
            surfaces.append(surface(lens_parameters[nLens][0][0],lens_parameters[nLens][0][1],lens_parameters[nLens][0][2],
                                    lens_parameters[nLens][0][3],lens_parameters[nLens][0][4],verbose=verbose))
    OS = opticalSystem(lenses,surfaces[-1],lens_parameters[-1][1],verbose)
    return surfaces, lenses, OS

def plotOpticalSystem(ax, color, OS, nPoints, plotLenses=True):
    if plotLenses: surfaces_points = OS.get_points_lenses  (nPoints)
    else         : surfaces_points = OS.get_points_surfaces(nPoints)

    surfaces_plot = []
    if plotLenses:
        for nLens in range(len(OS.lenses)+1):
            surfaces_plot.append(ax.plot([x for x,y in surfaces_points[nLens]], [y for x,y in surfaces_points[nLens]], color=color, linewidth=2.5)[0])
        
    return surfaces_plot
