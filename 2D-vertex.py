from math import cos, tan, sin, radians, sqrt
import typing
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class TwoD_():
    def __init__(self, velocity, max_dgree=180, height=0) -> None:
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
        plt.ylabel('이동높이')


        # 그리드 추가
        plt.grid(color = "gray", alpha=.5,linestyle='--')
        plt.axhline(y=0, color='salmon', linewidth=3)
        plt.axvline(x=0, color='salmon', linewidth=3)
        plt.style.use('fivethirtyeight')

        self.x = np.arange(0, self.max_dgree+self.interval, self.interval)
        self.y = list()
        for i in self.x:
            self.y.append(self.vertex_y(i))
        plt.title(f"각도(0~{self.max_dgree})-이동높이 그래프, 발사속도: {self.velocity}m/s, 시작높이: {self.height}m\n", fontweight='bold')


    def vertex_y(self, degree, velocity=None, height=None, g = 10):
        if velocity == None: velocity = self.velocity
        if height == None: height = self.height
        rad = radians(degree)

        # 예외 처리: 수직 발사 (theta = 90)
        # if degree == 90:
        #     max_height = velocity**2 / (2 * 9.8) + height 
        #     return max_height

        # 예외 처리: 수평 발사 (theta = 0)
        if degree == 0:
            return height

        # 꼭짓점y 좌표 계산
        y = height + (velocity**2 * sin(rad)**2) / (2 * g)

        if degree > 180 and degree < 360:
            return -y + height + height

        return y


    def draw_max_point(self):
        max_ver_y = max(self.y)
        if max_ver_y > 0:
            max_x_ver_y = self.x[self.y.index(max_ver_y)]
            plt.scatter(max_x_ver_y, max_ver_y, color="red")
            plt.annotate(f'최고점({max_x_ver_y:.2f}, {max_ver_y:.2f})', (max_x_ver_y, max_ver_y), textcoords="offset points", xytext=(0,10), ha='center', bbox=dict(boxstyle="round", fc=(1, 1, 1, 0.5)))

    def draw_min_point(self, idx:typing.Union[int, None]=None):
        min_ver_y = min(self.y)
        if idx == None:
            min_x_ver_y = self.x[self.y.index(min_ver_y)]
        else:
            min_x_ver_y = self.x[idx]

        plt.scatter(min_x_ver_y, min_ver_y, color="royalblue")
        plt.annotate(f'최저점({min_x_ver_y:.2f}, {min_ver_y:.2f})', (min_x_ver_y, min_ver_y), textcoords="offset points", xytext=(0,10), ha='center', bbox=dict(boxstyle="round", fc=(1, 1, 1, 0.5)))


    def make_graph(self, save=True):
        self.draw_max_point()
        if self.max_dgree == 180:
            self.draw_min_point()
            self.draw_min_point(int(180/self.interval))
        else:
            self.draw_min_point()
        #방정식 추가
        plt.plot(self.x,self.y, color="mediumpurple")

        if save:
            plt.savefig(f"각도-이동높이 0-{self.max_dgree} 그래프.png", format='png')
        plt.show()


    def _animate(self, i):
        if i > self.max_dgree: i == self.max_dgree
        if i == 90.0/self.interval: self.draw_max_point()
        if (i == 0.0): self.draw_min_point()
        if (i == 180/self.interval): self.draw_min_point(int(180/self.interval))
        print(i, end="\r")
        x = self.x[:i+1]
        y = self.y[:i+1]
        plt.plot(x, y, color="mediumpurple")
        plt.title(f"각도(0~{x[-1]})-이동높이 그래프, 발사속도: {self.velocity}m/s, 시작높이: {self.height}m\n", fontweight='bold')
        plt.tight_layout()

    def make_gif_graph(self):
        ani = FuncAnimation(plt.gcf(), self._animate, frames=int(self.max_dgree/self.interval)+(60*int(self.max_dgree/90)), interval=1)
        ani.save(f'./각도-이동높이 0-{self.max_dgree} 그래프.gif', fps=30)
        print('GIF_make_finish')




twoD = TwoD_(
    velocity=55,
    max_dgree=180,
    height=0
)
# twoD.make_gif_graph()
twoD.make_graph(False)