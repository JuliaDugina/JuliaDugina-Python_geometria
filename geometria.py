class Dot():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line():
    def __init__(self, dot_a, dot_b):
        self.dot_a = dot_a
        self.dot_b = dot_b
        self.lenght = self.get_lenght()

    def get_lenght(self):
        return ((self.dot_a.x-self.dot_b.x)**2 + (self.dot_a.y-self.dot_b.y)**2)**(0.5)

    def __gt__(self, line2):
        return self.lenght > line2.lenght

    def __ge__(self, line2):
        return self.lenght >= line2.lenght  

    def __lt__(self, line2):
        return self.lenght < line2.lenght

    def __le__(self, line2):
        return self.lenght <= line2.lenght 

    def __eq__(self, line2):
        return self.lenght == line2.lenght

    def __ne__(self, line2):
        return self.lenght != line2.lenght

    def is_intersection(self, line2):
        x1 = self.dot_a.x
        y1 = self.dot_a.y
        x2 = self.dot_b.x
        y2 = self.dot_b.y

        x3 = line2.dot_a.x
        y3 = line2.dot_a.y
        x4 = line2.dot_b.x
        y4 = line2.dot_b.y

        if y2 - y1 != 0:
            q = (x2 - x1) / (y1 - y2)
            sn = (x3 - x4) + (y3 - y4) * q
            if sn == 0:
                return False
            fn = (x3 - x1) + (y3 - y1) * q
            n = fn / sn
        else:
            if (y3 - y4) != 0:
                return False
            n = (y3 - y1) / (y3 - y4)
        cross_x = x3 + (x4 - x3) * n
        cross_y = y3 + (y4 - y3) * n
        #проверка что точка принадлежит обоим отрезкам
        '''
        расстояние от концов отрезка до точки
        пересечения должно быть равно длине отрезка, 
        в случае если точка пересечения принадлежит отрезку
        '''
        l1 = Line(Dot(cross_x, cross_y), self.dot_a)
        l2 = Line(Dot(cross_x, cross_y), self.dot_b)

        l3 = Line(Dot(cross_x, cross_y), line2.dot_a)
        l4 = Line(Dot(cross_x, cross_y), line2.dot_b)
        return (l1.lenght + l2.lenght == self.lenght) and (l3.lenght + l4.lenght == line2.lenght) 


class Triangle():
    def __init__(self, obj_a, obj_b, obj_c):
        if type(obj_a) == Dot and  type(obj_b) == Dot and type(obj_c) == Dot:
            self.dot_a = obj_a
            self.dot_b = obj_b
            self.dot_c = obj_c
            self.line_ab =  Line(obj_a, obj_b)
            self.line_bc =  Line(obj_b, obj_c)
            self.line_ac =  Line(obj_a, obj_c)

        if type(obj_a) == Line and  type(obj_b) == Line and type(obj_c) == Line:
            self.line_ab =  obj_a
            self.line_bc =  obj_b
            self.line_ac =  obj_c
            if not self.is_triangle_exist():
                raise TypeError("Triangle created by lines must contains same dots")
            self.dot_a = self.line_ab.dot_a
            self.dot_b = self.line_bc.dot_a
            self.dot_c = self.line_ac.dot_b

        self.triangle_type = self.get_triangle_type()
        self.triangle_area = self.get_triangle_area()
        self.triangle_perimetr = self.get_triangle_perimetr()
        self.medians = self.get_medians()

    def get_triangle_type(self):
        if round((self.line_bc.lenght**2), 0) == round((self.line_ab.lenght**2), 0) + round((self.line_ac.lenght**2), 0):
            triangle_type = "Прямоугольный"
        elif round((self.line_bc.lenght**2), 0) < round((self.line_ab.lenght**2), 0) + round((self.line_ac.lenght**2), 0):
            triangle_type = "Остроугольный"
        elif round((self.line_bc.lenght**2), 0) > round((self.line_ab.lenght**2), 0) + round((self.line_ac.lenght**2), 0):
            triangle_type = "Тупоугольный"
        return triangle_type

    def get_triangle_area(self):
        p = (self.line_ab.lenght + self.line_bc.lenght + self.line_ac.lenght) / 2
        triangle_area = ((p * (p - self.line_ab.lenght) * (p - self.line_bc.lenght) * (p - self.line_ac.lenght)))**0.5
        return triangle_area

    def get_triangle_perimetr(self):
        triangle_perimetr = self.line_ab.lenght + self.line_bc.lenght + self.line_ac.lenght
        return triangle_perimetr

    def get_medians(self):
        median_line_ac = round(((0.5 * ((self.line_ab.lenght)**2) + 0.5 * ((self.line_bc.lenght)**2) - 0.25 * ((self.line_ac.lenght)**2)) ** 0.5), 2)
        median_line_bc = round(((0.5 * ((self.line_ab.lenght)**2) + 0.5 * ((self.line_ac.lenght)**2) - 0.25 * ((self.line_bc.lenght)**2)) ** 0.5), 2)
        median_line_ab = round(((0.5 * ((self.line_ac.lenght)**2) + 0.5 * ((self.line_bc.lenght)**2) - 0.25 * ((self.line_ab.lenght)**2)) ** 0.5), 2)
        return median_line_ac, median_line_bc, median_line_ab
       
    def is_triangle_exist(self):
        all_unique_dots = set([(self.line_ab.dot_a.x, self.line_ab.dot_a.y), \
        (self.line_ab.dot_b.x, self.line_ab.dot_b.y), \
        (self.line_bc.dot_a.x, self.line_bc.dot_a.y), \
        (self.line_bc.dot_b.x, self.line_bc.dot_b.y), \
        (self.line_ac.dot_a.x, self.line_ac.dot_a.y), \
        (self.line_ac.dot_b.x, self.line_ac.dot_b.y)])
        return len(all_unique_dots) == 3


class Quadrilateral():
    def __init__(self, obj_a, obj_b, obj_c, obj_d):
        if type(obj_a) == Dot and  type(obj_b) == Dot and type(obj_c) == Dot and type(obj_d) == Dot:
            self.dot_a = obj_a
            self.dot_b = obj_b
            self.dot_c = obj_c
            self.dot_d = obj_d
            self.line_ab =  Line(obj_a, obj_b)
            self.line_bc =  Line(obj_b, obj_c)
            self.line_cd =  Line(obj_c, obj_d)
            self.line_da =  Line(obj_d, obj_a)

        if type(obj_a) == Line and  type(obj_b) == Line and type(obj_c) == Line and type(obj_d) == Line:
            self.line_ab =  obj_a
            self.line_bc =  obj_b
            self.line_cd =  obj_c
            self.line_da =  obj_d
            if not self.is_quadrilateral_exist():
                raise TypeError("Quadrilateral created by lines must contains same dots")
            self.dot_a = self.line_ab.dot_a
            self.dot_b = self.line_bc.dot_a
            self.dot_c = self.line_cd.dot_a
            self.dot_d = self.line_da.dot_a
        self.quadrilateral_type = self.get_quadrilateral_type()
        self.quadrilateral_perimetr = self.get_quadrilateral_perimetr()
        self.quadrilateral_area = self.get_quadrilateral_area()

    def is_quadrilateral_exist(self):
        geom_check = self.line_ab.lenght + self.line_bc.lenght + self.line_cd.lenght > self.line_da.lenght \
            and self.line_da.lenght + self.line_bc.lenght + self.line_cd.lenght > self.line_ab.lenght \
            and self.line_da.lenght + self.line_ab.lenght + self.line_cd.lenght > self.line_bc.lenght \
            and self.line_da.lenght + self.line_ab.lenght + self.line_bc.lenght > self.line_cd.lenght
        all_unique_dots = set([(self.line_ab.dot_a.x, self.line_ab.dot_a.y), \
        (self.line_ab.dot_b.x, self.line_ab.dot_b.y), \
        (self.line_bc.dot_a.x, self.line_bc.dot_a.y), \
        (self.line_bc.dot_b.x, self.line_bc.dot_b.y), \
        (self.line_cd.dot_a.x, self.line_cd.dot_a.y), \
        (self.line_cd.dot_b.x, self.line_cd.dot_b.y), \
        (self.line_da.dot_a.x, self.line_da.dot_a.y), \
        (self.line_da.dot_b.x, self.line_da.dot_b.y)])
        return len(all_unique_dots) == 4 and geom_check

#  Диагонали выпуклого четырёхугольника пересекаются, а невыпуклого нет.
    def get_quadrilateral_type(self):
        d1 = Line(self.dot_a, self.dot_c)
        d2 = Line(self.dot_b, self.dot_d)
        if d1.is_intersection(d2):
            return "Выпуклый"
        else:
            return "Не выпуклый"

    def get_quadrilateral_perimetr(self):
        quadrilateral_perimetr = self.line_ab.lenght +  self.line_bc.lenght + self.line_cd.lenght + self.line_da.lenght
        return quadrilateral_perimetr

    def get_quadrilateral_area(self):
        p = self.quadrilateral_perimetr / 2
        quadrilateral_area = ((p - self.line_ab.lenght) * (p - self.line_bc.lenght) * (p - self.line_cd.lenght) * (p - self.line_da.lenght)) ** 0.5   
        return quadrilateral_area


def test_line():
    d0 = Dot(2, 2)
    e0 = Dot(7, 7)
    d1 = Dot(1, 4)
    e1 = Dot(5, 2)
    L0 = Line(d0, e0)
    L1 = Line(d1, e1)
    print('Длина отрезка 1 равна:', round((L0.get_lenght()), 2))
    print('Длина отрезка 2 равна:', round((L1.get_lenght()), 2))
    print('Длина отрезка 1 больше отрезка 2:', L0.__gt__(L1))
    print('Длина отрезка 1 больше, либо равна отрезку 2:', L0.__ge__(L1))
    print('Длина отрезка 1 меньше отрезка 2:', L0.__lt__(L1))
    print('Длина отрезка 1 меньше либо равна отрезку 2:', L0.__le__(L1))
    print('Длина отрезка 1 равна длине отрезка 2:', L0.__eq__(L1))
    print('Длина отрезка 1 не равна длине отрезка 2:', L0.__ne__(L1))
    print('Отрезки 1 и 2 пересекаются:', L0.is_intersection(L1))
    print("\n")

def test_triangle():
    a0 = Dot(2, 2)
    b0 = Dot(3, 5)

    a1 = Dot(1.5, 5)
    b1 = Dot(3, 5)

    a2 = Dot(1.5, 5)
    b2 = Dot(2, 2)

    l1 = Line(a0, b0)
    l2 = Line(a1, b1)
    l3 = Line(a2, b2)

    t = Triangle(l1, l2, l3)
    print('Длина 1 стороны треугольника:', round((t.line_ab.get_lenght()), 2))
    print('Длина 2 стороны треугольника:', round((t.line_bc.get_lenght()), 2))
    print('Длина 3 стороны треугольника:', round((t.line_ac.get_lenght()), 2))
    print('Треугольник существует:', t.is_triangle_exist())
    print('Площадь треугольника:', t.get_triangle_area())
    print('Периметр треугольника:', round((t.get_triangle_perimetr()), 2))
    print('Тип треугольника:', t.triangle_type)
    print('Длины всех медиан треугольника:', t.get_medians())
    print("\n")

def test_quadrilateral():
    a0 = Dot(1, 1)
    b0 = Dot(4, 1)

    a1 = Dot(4, 1)
    b1 = Dot(4, 3)

    a2 = Dot(4, 3)
    b2 = Dot(1, 3)

    a3 = Dot(1, 3)
    b3 = Dot(1, 1)

    l1 = Line(a0, b0)
    l2 = Line(a1, b1)
    l3 = Line(a2, b2)
    l4 = Line(a3, b3)

    q = Quadrilateral(l1, l2, l3, l4)
    print('Длина 1 стороны четырехугольника:', q.line_ab.get_lenght())
    print('Длина 2 стороны четырехугольника:', q.line_bc.get_lenght())
    print('Длина 3 стороны четырехугольника:', q.line_cd.get_lenght())
    print('Длина 4 стороны четырехугольника:', q.line_da.get_lenght())

    print('Четырехугольник существует:', q.is_quadrilateral_exist()) 
    print('Тип четырехугольника:', q.get_quadrilateral_type())
    print('Периметр четырехугольника:', q.get_quadrilateral_perimetr())
    print('Площадь четырехугольника:', q.get_quadrilateral_area())

if __name__ == "__main__":
    test_line()
    test_triangle()
    test_quadrilateral()

