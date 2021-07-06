import math as _math
from tilemapbase import Extent
from tilemapbase.mapping import project
from tilemapbase.mapping import to_lonlat
from pyproj import Proj


class ExtentUTM(Extent):
    def __init__(self,
                 longitude_min,
                 longitude_max,
                 latitude_min,
                 latitude_max,
                 proj_cmd):

        self.utm_project = Proj(proj_cmd)
        xmin, ymin = project(longitude_min, latitude_max)
        xmax, ymax = project(longitude_max, latitude_min)
        super().__init__(xmin, xmax, ymin, ymax)        
        self.project = self.to_utm

    def to_utm(self, x, y):
        lon, lat = to_lonlat(x, y)
        return self.utm_project(lon,lat)
