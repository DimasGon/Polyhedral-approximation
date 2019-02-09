from numpy import array
from math import cos, sin, pi
from numpy import linalg, array
import matplotlib.pyplot as plt


class Approximation:
    """Представление внутреннего и внешего многогранников, аппроксиммирующих окружность\
    \n\nТочки на окружности имеют представление {угол фи: (координата x, координата y)}\
    \n\nХорды (они же стороны внетренней аппроксимации) имеют представление\
    {длина хорды: (угол фи откуда выпущена, угол фи куда зашла)}\
    \nХорды отсортированы по углу фи, из которого выпущены"""

    points = dict()
    chords = dict()

    def __init__(self, *args):
        self.points = dict()
        self.chords = dict()
        for phi in args:
            self.points[phi] = (cos(phi), sin(phi))
        self.points = dict(sorted(self.points.items(),  key = lambda k: k[0]))
        prev_phi = None
        prev_coord = None
        for phi, coord in self.points.items():
            cur_phi = phi
            cur_coord = coord
            if prev_coord:
                length = ((cur_coord[0] - prev_coord[0]) ** 2 + (cur_coord[1] - prev_coord[1]) ** 2) ** 0.5
                self.chords[prev_phi] = (cur_phi, length)
            else:
                first_phi = cur_phi
                first_coord = cur_coord
            prev_phi = cur_phi
            prev_coord = cur_coord
        length = ((first_coord[0] - prev_coord[0]) ** 2 + (first_coord[1] - prev_coord[1]) ** 2) ** 0.5
        self.chords[prev_phi] = (first_phi, length)
        self.chords = dict(sorted(self.chords.items(),  key = lambda k: k[0]))

    def get_points(self):
        """Возвращает все точки в формате {угол фи: (координата x, координата y), ...}"""
        return self.points
    
    def get_chords(self):
        """Возвращает все хорды в формате {угол фи откуда выпущена: (угол фи куда зашла, длина хорды)}, ..."""
        return self.chords
    
    def get_chords_lengths(self):
        """Возвращает список длин хорд"""
        lengths = dict()
        for from_phi, (in_phi, length) in self.chords.items():
            lengths[length] = (from_phi, in_phi)
        return lengths
    
    def get_coordinates(self, target=None):
        """Возвращает все координаты x и y в формате [(x1, y1), (x2, y2), ...] если target не указана\
        \nВозвращает список всех x и список всех y, если target указан"""
        x = list(); y = list()
        for _, x_y in self.points.items():
            x_tmp, y_tmp = x_y
            x.append(x_tmp); y.append(y_tmp)
        if target:
            return x, y
        else:
            return list(zip(x, y))

    def set_new_point(self):
        """Ищет максимальную длины хорды. Находит новую phi как среднее арифметическое между тем откуда хорда начинается и куда идёт.\
        \nЗатем добавляет точку с углом new_phi ко всем точкам и изменяет хорды"""
        lengths = dict()
        for from_phi, (in_phi, length) in self.chords.items():
            lengths[length] = (from_phi, in_phi)
        min_length = max(lengths)
        from_phi, in_phi = lengths[min_length]
        if abs(from_phi - in_phi) > pi:
            new_phi = (from_phi + in_phi) / 2 + pi
        else:
            new_phi = (from_phi + in_phi) / 2
        self.points[new_phi] = (cos(new_phi), sin(new_phi))
        length = ((self.points[from_phi][0] - self.points[new_phi][0]) ** 2 + (self.points[from_phi][1] - self.points[new_phi][1]) ** 2) ** 0.5
        self.chords[from_phi] = (new_phi, length)
        self.chords[new_phi] = (in_phi, length)
        self.points = dict(sorted(self.points.items(),  key = lambda k: k[0]))
        self.chords = dict(sorted(self.chords.items(),  key = lambda k: k[0]))
        return new_phi

    def external_approximation(self):
        x_y = self.get_coordinates()
        prev_tangent_xy = None
        prev_tangent_const = None
        external_approx_points = list()
        for x, y in x_y:
            cur_tangent_xy = [-x, -y]
            cur_tangent_const = [-x * x - y * y]
            if not prev_tangent_xy:
                first_tangent_xy = cur_tangent_xy
                first_tangent_const = cur_tangent_const
            else:
                coord_xy = [cur_tangent_xy, prev_tangent_xy]
                coord_const = [cur_tangent_const, prev_tangent_const]
                external_approx_points.append(linalg.solve(coord_xy, coord_const).tolist())
            prev_tangent_xy = cur_tangent_xy
            prev_tangent_const = cur_tangent_const
        coord_xy = [prev_tangent_xy, first_tangent_xy]
        coord_const = [prev_tangent_const, first_tangent_const]
        external_approx_points.append(linalg.solve(coord_xy, coord_const).tolist())
        for ind, val in enumerate(external_approx_points):
            external_approx_points[ind] = [val[0][0], val[1][0]]
        return external_approx_points

def solve(points, target=None):

    approx = Approximation(*points)
    new_phi = None
    if target is None:
        new_phi = approx.set_new_point()
    external_polygon = plt.Polygon(approx.external_approximation())
    external_polygon.set_facecolor('green')
    _, ax = plt.subplots()
    ax.add_artist(external_polygon)
    circle = plt.Circle((0, 0), 1)
    circle.set_facecolor('white')
    circle.set_edgecolor('black')
    ax.add_artist(circle)
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    # x, y = approx.get_coordinates(target='x y')
    # plt.scatter(x, y)
    polygon_inside = plt.Polygon(approx.get_coordinates())
    polygon_inside.set_facecolor('red')
    ax.add_artist(polygon_inside)
    plt.savefig('graph.png', format='png', dpi=450)
    plt.clf()
    
    return new_phi, approx.get_coordinates()

if __name__ == "__main__":
    pass