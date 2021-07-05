import math as _math
from tilemapbase import Extent
from pyproj import Proj



myProj = Proj("+proj=utm +zone=29U, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

def myProj2(x,y):
    x,y = myProj(x,y)
    return (x, y)

def project(longitude, latitude):
    """Project the longitude / latitude coords to the unit square.
    :param longitude: In degrees, between -180 and 180
    :param latitude: In degrees, between -85 and 85
    :return: Coordinates `(x,y)` in the "Web Mercator" projection, normalised
      to be in the range [0,1].
    """
    if longitude < -180 or longitude > 180 or latitude <= -90 or latitude >= 90:
        raise ValueError(f"Longitude/Latitude ({longitude}/{latitude}) is out of valid range [-180,180] / [-90,90].  Did you swap them around?")
    xtile = (longitude + 180.0) / 360.0
    lat_rad = _math.radians(latitude)
    ytile = (1.0 - _math.log(_math.tan(lat_rad) + (1 / _math.cos(lat_rad))) / _math.pi) / 2.0
    return (xtile, ytile)

def to_lonlat(x, y):
    """Inverse project from "web mercator" coords back to longitude, latitude.
    :param x: The x coordinate, between 0 and 1.
    :param y: The y coordinate, between 0 and 1.
    :return: A pair `(longitude, latitude)` in degrees.
    """
    longitude = x * 360 - 180
    latitude = _math.atan(_math.sinh(_math.pi * (1 - y * 2))) * 180 / _math.pi
    return (longitude, latitude)

def to_utm(x, y):
    lon, lat = to_lonlat(x, y)
    return myProj(lon,lat)

class ExtentUTM(Extent):
    def __init__(self, xmin, ymin, xmax, ymax, **kwargs):
        super().__init__(xmin, ymin, xmax, ymax)        
        self.project = to_utm        
        print(xmin, ymin, xmax, ymax)
       
    @staticmethod
    def project_utm(x,y):
        return myProj2(x,y)
    
    @staticmethod
    def from_lonlat(longitude_min, longitude_max, latitude_min, latitude_max):
        """Construct a new instance from longitude/latitude space."""
        xmin, ymin = project(longitude_min, latitude_max)
        xmax, ymax = project(longitude_max, latitude_min)
        return ExtentUTM(xmin, xmax, ymin, ymax)

    # @staticmethod
    # def from_lonlat(longitude_min, longitude_max, latitude_min, latitude_max):
    #     """Construct a new instance from longitude/latitude space."""
    #     xmin, ymin = myProj(longitude_min, latitude_max)
    #     xmax, ymax = myProj(longitude_max, latitude_min)
    #     return Extent(xmin, xmax, ymin, ymax)
    
