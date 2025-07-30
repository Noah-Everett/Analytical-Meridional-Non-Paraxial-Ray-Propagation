from .misc import limitAngle
import math

class opticalRay:
    def __init__(self, opticalRay):
        """
        Constructor for the opticalRay class, initializes the object with another opticalRay object.

        Parameters:
            opticalRay (opticalRay): Another opticalRay object.
        """
        self.x       = opticalRay.x
        self.y       = opticalRay.y
        self.theta   = opticalRay.theta
        self.verbose = opticalRay.verbose
        self.__checkTheta()

    def __init__(self, x, y, theta, verbose=False):
        """
        Constructor for the opticalRay class.

        Parameters:
            x (float): x-coordinate of the optical ray.
            y (float): y-coordinate of the optical ray.
            theta (float): Angle of the optical ray with the x-axis (in radians).
            verbose (bool, optional): Flag indicating whether to print verbose output. Default is False.
        """
        self.x       = x
        self.y       = y
        self.theta   = theta
        self.verbose = verbose
        self.__checkTheta()

    def update_theta(self, theta):
        """
        Update the theta angle of the optical ray.

        Parameters:
            theta (float): New value for the theta angle.

        Returns:
            bool: True if the theta angle is within the valid range, False otherwise.
        """
        self.theta = theta
        return self.__checkTheta()

    def __checkTheta(self):
        """
        Check if the theta angle is within the valid range.

        Returns:
            bool: True if the theta angle is within the valid range, False otherwise.
        """
        self.theta = limitAngle(self.theta, self.verbose)

        if math.cos(self.theta) <= 0:
            raise ValueError('Theta out of bounds')

        return True

# def plotOpticalRay():