import copy
import math
from .misc import quadraticFormula
from .misc import limitAngle

class rayPropagator:
    def __init__(self, opticalSystem, opticalRay, yLimits=None, verbose=False):
        """
        Initialize the ray propagator object with the specified parameters.

        Parameters:
            opticalSystem (opticalSystem): The optical system through which the ray will be propagated.
            opticalRay (ray): The optical ray to be propagated.
            yLimits (list): y-limits for optical ray propagation.
            verbose (bool, optional): Flag indicating whether to print verbose output. Default is False.
        """
        self.opticalSystem = opticalSystem
        self.opticalRay    = opticalRay
        self.yLimits       = yLimits
        self.verbose       = verbose
        if self.opticalRay.x > self.opticalSystem.surfaces[0].r_x + self.opticalSystem.surfaces[0].x:
            raise ValueError("x-position of the optical ray is not less than all lenses' x-positions")
        
        for lens in self.opticalSystem.lenses:
            surface_1 = lens.surface_2
            surface_2 = lens.surface_1
            if yLimits != None and surface_1.y_min < yLimits[0]:
                raise ValueError("Lens' y_min is lower than global y_min")
            elif yLimits != None and surface_1.y_max > yLimits[1]:
                raise ValueError("Lens' y_max is greater than global y_max")
        
    def propagateRay(self,nSurfacesPropagate=-1,paraxial=False):
        """
        Propagate the optical ray through the optical system.

        Parameters:
            nSurfacesPropagate (int, optional): Number of surfaces to propagate the ray. Default is -1, which means propagate through all surfaces.
            paraxial (bool, optional): True to use the paraxial appriximation to propagate the ray, False otherwise

        Returns:
            list: List of optical ray states at each step of propagation.
        """
        opticalRay_temp = copy.deepcopy(self.opticalRay)
        steps = [copy.deepcopy(opticalRay_temp)]
            
        if nSurfacesPropagate > len(self.opticalSystem.surfaces): 
            nSurfacesPropagate = -1
            
        self.__translateRay(self.opticalSystem.surfaces[0],opticalRay_temp,paraxial=paraxial)
        steps.append(copy.deepcopy(opticalRay_temp))
        for nSurface in range(0,len(self.opticalSystem.surfaces)-1):
            if nSurfacesPropagate>0 and nSurface+1 > nSurfacesPropagate:
                break
                
            if opticalRay_temp.theta >= 0:
                opticalRay_temp = self.__refractRay(self.opticalSystem.surfaces[nSurface],
                                                    opticalRay_temp,
                                                    self.opticalSystem.refractiveIndices[nSurface],
                                                    self.opticalSystem.refractiveIndices[nSurface+1],
                                                    paraxial=paraxial)
            if opticalRay_temp.theta >= 0:
                opticalRay_temp = self.__translateRay(self.opticalSystem.surfaces[nSurface+1],opticalRay_temp,paraxial=paraxial)
                
            steps.append(copy.deepcopy(opticalRay_temp))
        
        return steps
    
    def __translateRay(self,surface,opticalRay_temp,paraxial=False):
        """
        Translate the optical ray at the surface.

        Parameters:
            surface (surface): The surface at which the ray is to be translated.
            opticalRay_temp (ray): The optical ray to be translated.

        Returns:
            ray: The translated optical ray.
        """
        if paraxial:
            opticalRay_temp
        else:
            if surface.r_x > 0: sign = +1
            if surface.r_x < 0: sign = -1

            m = math.tan(opticalRay_temp.theta)
            c_1 = 1/surface.r_x**2 + m**2/surface.r_y**2
            c_2 = -2*surface.x/surface.r_x**2 + m/surface.r_y**2 * (-2*m*opticalRay_temp.x + 2*opticalRay_temp.y)
            c_3 = surface.x**2/surface.r_x**2 + ((m*opticalRay_temp.x - opticalRay_temp.y)/surface.r_y)**2 - 1
            
            if opticalRay_temp.theta == 0: opticalRay_temp.theta = 1e-5

            x_new = quadraticFormula(sign,c_1,c_2,c_3,self.verbose)
            if x_new != None:
                y_new = m * (x_new - opticalRay_temp.x) + opticalRay_temp.y
                if y_new < surface.y_min:
                    opticalRay_temp.x = (self.yLimits[0]-opticalRay_temp.y)/math.tan(opticalRay_temp.theta)+opticalRay_temp.x
                    opticalRay_temp.y = self.yLimits[0]
                    opticalRay_temp.theta = -99999
                elif y_new > surface.y_max:
                    opticalRay_temp.x = (self.yLimits[1]-opticalRay_temp.y)/math.tan(opticalRay_temp.theta)+opticalRay_temp.x
                    opticalRay_temp.y = self.yLimits[1]
                    opticalRay_temp.theta = -99999
                else:
                    opticalRay_temp.x = x_new
                    opticalRay_temp.y = y_new
            elif x_new == None:
                if self.yLimits == None and self.verbose:
                    print('WARNING: ray translated to invalid point')
                elif self.yLimits != None and limitAngle(opticalRay_temp.theta) < math.pi/2:
                    opticalRay_temp.x = (self.yLimits[1]-opticalRay_temp.y)/math.tan(opticalRay_temp.theta)+opticalRay_temp.x
                    opticalRay_temp.y = self.yLimits[1]
                elif self.yLimits != None:
                    opticalRay_temp.x = (self.yLimits[0]-opticalRay_temp.y)/math.tan(opticalRay_temp.theta)+opticalRay_temp.x
                    opticalRay_temp.y = self.yLimits[0]
                opticalRay_temp.theta = -99999

        return opticalRay_temp
    
    def __refractRay(self,surface,opticalRay_temp,refractiveIndex_i,refractiveIndex_f,paraxial=False):
        """
        Refract the optical ray at the surface.

        Parameters:
            surface (surface): The surface at which the ray is to be refracted.
            opticalRay_temp (ray): The optical ray to be refracted.
            refractiveIndex_i (float): Refractive index of the medium from which the ray is incident.
            refractiveIndex_f (float): Refractive index of the medium into which the ray is refracted.

        Returns:
            ray: The refracted optical ray.
        """
        num = surface.r_y**2/surface.r_x**2*(-opticalRay_temp.x**2+2*surface.x*opticalRay_temp.x-surface.x**2)+surface.r_y**2
        if num <  0: 
            if self.verbose: print('WARNING: num<0:',num)
            num = 0
        if num == 0: 
            if self.verbose: print('WARNING: num==0:',num)
            num = 1e-25
        dydx = surface.r_y**2/surface.r_x**2*(surface.x-opticalRay_temp.x)*num**(-1/2)

        if opticalRay_temp.y < 0: dydx = -dydx
        theta_n = math.atan(-1/dydx)
        
        theta_in = limitAngle(opticalRay_temp.theta,-math.pi/2,math.pi/2) - theta_n
        
        if refractiveIndex_f <= refractiveIndex_i:
            theta_c = limitAngle(math.asin(refractiveIndex_f/refractiveIndex_i))
            if abs(theta_in) >= theta_c:
                if self.verbose:
                    print('WARNING: total internal reflection')
                opticalRay_temp.theta = -99999
                return opticalRay_temp
        
        num2 = refractiveIndex_i/refractiveIndex_f*math.sin(theta_in)
        if abs(num2)>1: 
            raise ValueError('WARNING: total internal reflection, |num2|>1:')
        
        theta_fn = math.asin(num2)
        theta_f = theta_n+theta_fn
                
        opticalRay_temp.update_theta(theta_f)
        
        return opticalRay_temp