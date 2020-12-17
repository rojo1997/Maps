# -----------------------------------------------------------------------------
# (C) 2020 Ernesto Martinez del Pino, Granada, Spain
# Released under GNU Public Licence (GPL)
# email: ernestomar1997@hotmail.com
# -----------------------------------------------------------------------------
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_perimeter(direction: str) -> np.array:
    direction = direction.replace(' ', '+')
    url = ('https://nominatim.openstreetmap.org/search.php?q=' 
        + direction + '&polygon_geojson=1&format=json')
    response = json.loads(requests.get(url).text)
    if response[0]['geojson']['type'] == 'MultiPolygon':
        return [np.array(polygon[0][:-1]) for polygon in response[0]['geojson']['coordinates']]
    if response[0]['geojson']['type'] == 'Polygon':
        return [np.array(response[0]['geojson']['coordinates'][0][:-1])]

vimplicita = lambda P: np.array([
    - (P[:,3] - P[:,1]) / (P[:,2] - P[:,0]),
    np.ones(P.shape[0]),
    - (P[:,1] - ((P[:,3] - P[:,1]) / (P[:,2] - P[:,0])) * P[:,0])
]).T

def point_in_perimeter(perimeter: np.array, point: np.array) -> bool:
    matrix = np.hstack([
        perimeter[np.mod(np.arange(0,perimeter.shape[0]) + 1,perimeter.shape[0]),:],
        perimeter
    ])
    ecuaciones = vimplicita(matrix)
    xs = matrix[:,0]
    xe = matrix[:,2]
    ys = matrix[:,1]
    ye = matrix[:,3]
    a = ecuaciones[:,0]
    b = ecuaciones[:,1]
    c = ecuaciones[:,2]
    x0 = point[0]
    y0 = point[1]
    n = np.random.exponential(scale = 1.0)
    m = (y0 - n)/x0
    xi = (n + (c/b))/(- m - (a/b))
    yi = m * xi + n
    xc = np.logical_and(np.minimum(xs,xe) < xi, np.maximum(xs,xe) > xi)
    yc = np.logical_and(np.minimum(ys,ye) < yi, np.maximum(ys,ye) > yi)
    gc = np.logical_and(xc,yc)
    if np.count_nonzero(gc) == 0: return False
    return np.count_nonzero(np.sort(xi[gc]) < x0) % 2 == 1

def uniform_polygon(perimeter: list, size: int) -> np.array:
    minimum = np.array([p.min(0) for p in perimeter]).min(0)
    maximum = np.array([p.max(0) for p in perimeter]).max(0)
    points = np.zeros((size,2))
    points[:,0] = np.random.uniform(minimum[0],maximum[0],size)
    points[:,1] = np.random.uniform(minimum[1],maximum[1],size)

    def U(perimeter,point):
        try:
            return [point_in_perimeter(per,point) for per in perimeter].index(True)
        except ValueError:
            return -1
    
    points_acc = []
    indexs = []
    for point in points:
        result = U(perimeter,point)
        if result > -1:
            points_acc.append(point)
            indexs.append(result)
    return np.array(points_acc),np.array(indexs),perimeter

def uniform_city(city: str, size: int):
    perimeter = get_perimeter(city)
    return uniform_polygon(perimeter, size)

city = 'España'

X,indexes,perimeter = uniform_city(city, 10000)

sns.scatterplot(
    x = X[:,0],
    y = X[:,1],
    hue = np.repeat(1,X.shape[0])
)

for i,per in enumerate(perimeter):
    sns.scatterplot(
        x = per[:,0],
        y = per[:,1],
        hue = np.repeat((i+1)*20,per.shape[0])
    )

plt.title(city)
plt.show()