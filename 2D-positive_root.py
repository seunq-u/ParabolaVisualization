from math import cos, tan, sin, radians, sqrt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation



class TwoD_():
    def __init__(self, velocity, max_dgree=90, height=0) -> None:
        self.max_dgree = max_dgree
        self.velocity = velocity
        self.height = height
        self.interval = 0.5

        plt.figure(figsize=(16,9))

        # 한글 추가
        plt.rcParams['font.family'] ='Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] =False

        # 축 이름 설정

        plt.xlabel('각도')
        plt.ylabel('이동거리')

        # 그리드 추가
        plt.grid(color = "gray", alpha=.5,linestyle='--')
        plt.axhline(y=0, color='salmon', linewidth=3)
        plt.axvline(x=0, color='salmon', linewidth=3)
        plt.style.use('fivethirtyeight')

        self.x = np.arange(0, self.max_dgree+self.interval, self.interval)
        self.y = list()
        for i in self.x:
            self.y.append(self.positive_root(i))
        plt.title(f"각도(0~{self.max_dgree})-이동거리 그래프, 발사속도: {self.velocity}m/s, 시작높이: {self.height}m\n", fontweight='bold')


    def positive_root(self, d, v=None, h=None, g=10):
        if v == None: v = self.velocity
        if h == None: h = self.height

        theta_rad = radians(d)

        # 예외 처리: 수직 발사 (theta = 90)
        if d == 90 or d == 180:
            if h > 0:
                return sqrt(2 * h / g)
            else:
                return 0

        # 근의 공식 계산
        a = -g / (2 * v**2 * cos(theta_rad)**2)
        b = tan(theta_rad)
        c = h
        discriminant = b**2 - 4 * a * c # 판별식

        # 근의 유형 판별
        if discriminant < 0:
            return 0  # 근이 없음
        elif discriminant == 0:
            return -b / (2 * a)  # 중근
        else:
            root1 = (-b + sqrt(discriminant)) / (2 * a)
            root2 = (-b - sqrt(discriminant)) / (2 * a)
        
        if (d // 90) % 2 == 0:
            if root1 > 0:
                return root1
            elif root2 > 0:
                return root2
        else:
            if root1 < 0:
                return root1
            elif root2 < 0:
                return root2


    def draw_max_point(self):
        max_ver_y = max(self.y)
        if max_ver_y > 0:
            max_x_ver_y = self.x[self.y.index(max_ver_y)]
            plt.scatter(max_x_ver_y, max_ver_y, color="red")
            plt.annotate(f'최고점({max_x_ver_y:.2f}, {max_ver_y:.2f})', (max_x_ver_y, max_ver_y), textcoords="offset points", xytext=(0,10), ha='center', bbox=dict(boxstyle="round", fc=(1, 1, 1, 0.5)))

    def draw_min_point(self):
        min_ver_y = min(self.y)
        if min_ver_y < 0:
            min_x_ver_y = self.x[self.y.index(min_ver_y)]
            plt.scatter(min_x_ver_y, min_ver_y, color="royalblue")
            plt.annotate(f'최저점({min_x_ver_y:.2f}, {min_ver_y:.2f})', (min_x_ver_y, min_ver_y), textcoords="offset points", xytext=(0,10), ha='center', bbox=dict(boxstyle="round", fc=(1, 1, 1, 0.5)))

    def make_graph(self):
        self.draw_max_point()
        self.draw_min_point()
        #방정식 추가
        plt.plot(self.x,self.y, color="yellowgreen")

        plt.savefig(f"각도-이동거리 0-{self.max_dgree} 그래프.png", format='png')
        plt.show()


    def _animate(self, i):
        if i > self.max_dgree: i == self.max_dgree
        if i == 45.0/self.interval: self.draw_max_point()
        if i == 135.0/self.interval: self.draw_min_point()
        print(i, end="\r")
        x = self.x[:i+1]
        y = self.y[:i+1]
        plt.plot(x, y, color="yellowgreen")
        plt.title(f"각도(0~{x[-1]})-이동거리 그래프, 발사속도: {self.velocity}m/s, 시작높이: {self.height}m\n", fontweight='bold')
        plt.tight_layout()

    def make_gif_graph(self):
        ani = FuncAnimation(plt.gcf(), self._animate, frames=int(self.max_dgree/self.interval)+int(60*(self.max_dgree/90)), interval=1)
        ani.save(f'./각도-이동거리 0-{self.max_dgree} 그래프.gif', fps=30)
        print('GIF_make_finish')


towD = TwoD_(
    velocity = 55,
    max_dgree = 180)
# towD.make_gif_graph()
towD.make_graph()