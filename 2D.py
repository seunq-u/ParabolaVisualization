from math import cos, tan, sin, radians, sqrt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


# 포물선 방정식 함수
def positive_root(d, v, h, g=10):
    """
    분수 물줄기 포물선 운동 방정식의 양의 근(지면에 닿을 때 x값)을 계산하는 함수

    Args:
        g: 중력 가속도 (m/s^2)
        v: 초기 속도 (m/s)
        theta: 발사 각도 (degrees)
        h: 초기 높이 (m)

    Returns:
        양의 근 (m) 또는 None (근이 없거나 음수일 경우)
    """
    theta_rad = radians(d)

    # 예외 처리: 수직 발사 (theta = 90)
    if d == 90:
        if h > 0:
            return sqrt(2 * h / g)
        else:
            return 0

    # 근의 공식 계산
    a = -g / (2 * v**2 * cos(theta_rad)**2)
    b = tan(theta_rad)
    c = h
    discriminant = b**2 - 4 * a * c

    # 근의 유형 판별
    if discriminant < 0:
        return 0  # 근이 없음
    elif discriminant == 0:
        return -b / (2 * a)  # 중근
    else:
        root1 = (-b + sqrt(discriminant)) / (2 * a)
        root2 = (-b - sqrt(discriminant)) / (2 * a)
    if root1 > 0:
        return root1
    elif root2 > 0:
        return root2
    else:
        return 0  # 양의 근이 없음

def vertex(degree, velocity, height, g = 10):
    """
    분수 물줄기 포물선 운동의 꼭짓점 좌표를 계산하는 함수
    Args: degree: 발사 각도 (degrees), velocity: 초기 속도 (m/s), height: 초기 높이 (m)
    Returns: 꼭짓점 좌표 (x, y) (m)
    """
    theta_rad = radians(degree)

    # 예외 처리: 수직 발사 (theta = 90)
    # if degree == 90:
    #     max_height = velocity**2 / (2 * 9.8) + height 
    #     return 0, max_height

    # 예외 처리: 수평 발사 (theta = 0)
    if degree == 0:
        return (0, height)

    # 꼭짓점 좌표 계산
    
    x = (velocity**2 * sin(theta_rad) * cos(theta_rad)) / g
    y = height + (velocity**2 * sin(theta_rad)**2) / (2 * g)

    return (x, y)

def rgb_to_hex(r, g, b):
    r, g, b = int(r), int(g), int(b)
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

def number_to_rainbow(number, total_numbers):
    """
    전체 개수로 무지개 색상 범위를 나누고, 인덱스에 해당하는 색상을 반환하는 함수

    Args:
        number: 0부터 total_numbers-1까지의 정수
        total_numbers: 전체 개수

    Returns:
        RGB 색상 코드 (tuple)
    """
    if number < 0 or number >= total_numbers:
        raise ValueError("입력 값은 0부터 total_numbers-1 사이의 정수여야 합니다.")

    # 빨강, 주황, 노랑, 초록, 파랑, 남색, 보라 순서로 색상 범위 설정
    color_ranges = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
    num_colors = len(color_ranges)

    # 입력 숫자에 해당하는 색상 범위 찾기
    idx = int(number * num_colors / total_numbers)
    start_color = color_ranges[idx]
    end_color = color_ranges[idx + 1] if idx < num_colors - 1 else color_ranges[idx]

    # 색상 범위 내에서 선형 보간하여 RGB 값 계산
    t = (number * num_colors / total_numbers - idx)  
    r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
    g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
    b = int(start_color[2] + (end_color[2] - start_color[2]) * t)

    return rgb_to_hex(r, g, b)

def parabolic(degree, velocity, height):
    """포물선 방정식 
    -input: degree(발사각), velocity(발사속도), height(발사대 높이)
    -output: x(x값 배열), y(y값 배열), start(그래프 시작), end(그래프 끝)
    """
    start = 0
    end = positive_root(degree, velocity, height)

    r = radians(degree)
    x = np.arange(0, end + (end * 5 / 100), 0.2)
    y = -(10/(2*cos(r)*cos(r)*velocity*velocity))*x*x + tan(r)*x + height
    # print(f"{x=}"); print(f"{y=}")

    return (x, y, start, end)

### 
def print_one_parabolic(degree, velocity, height, color: tuple, display_point:list):
    """_summary_

    Args:
        degree (_type_): _description_
        velocity (_type_): _description_
        height (_type_): _description_
        color (tuple[int, int, int]): _description_
        display_point (list[bool]):  [발사 지점 표시, 꼭짓점 표시, 착지 지점 표시]

    Returns:
        tuple[float, float]: [착지 지점 x좌표, 최대 높이(꼭짓점) y좌표]
    """
    graph_name = f"각도: {degree}, 발사속도: {velocity}, 시작높이: {height}"
    # 방정식 구하기
    x, y, _, end = parabolic(degree=degree, velocity=velocity, height=height)

    # 최고점 구하기 
    vertex_x, vertex_y = vertex(degree=degree, velocity=velocity, height=height)

    #방정식 추가
    plt.title(graph_name, fontweight='bold')
    plt.plot(x,y, color=color)

    # 발사 지점 표시
    if display_point[0]:
        plt.scatter(0, height, color=color); plt.annotate(f'발사지점(0, {int(height)})', (0, height), textcoords="offset points", xytext=(0,10), ha='center', bbox=dict(boxstyle="round", fc="0.8"))
    # 꼭짓점 표시
    if display_point[1]:
        plt.scatter(vertex_x, vertex_y, color=color); plt.annotate(f'최고점({vertex_x:.2f}, {vertex_y:.2f})', (vertex_x, vertex_y), textcoords="offset points", xytext=(0,10), ha='center', bbox=dict(boxstyle="round", fc="0.8"))
    # 착지 지점 표시
    if display_point[2] and end is not None:
        plt.scatter(end, 0, color=color); plt.annotate(f'착지 지점({end:.2f}, 0)', (end, 0), textcoords="offset points", xytext=(0,-20), ha='center', bbox=dict(boxstyle="round", fc=(1, 1, 1, 0.5)))

    # plt.xlim(-40, (max_pr:=positive_root(45, velocity, height))+max_pr*0.1)
    # plt.ylim(0, (max_vy:=vertex(45, velocity, height)[1])+max_vy*0.1)
    if vertex_y !=0:
        plt.ylim(0, vertex_y+(vertex_y*10/100))
    return end, vertex_y



def draws_mult_parabolic(data: list):
    """_summary_

    Args:
        data (dict): 최대 256개의 리스트
    """
    if len(data) > 256:
        return ValueError("data는 256개 이하까지만 가능합니다.")
    end_list = []
    vertex_y_list = []

    for idx, val in enumerate(data):
        end, vertex_y = print_one_parabolic(degree=val["dgree"], velocity=val["velocity"], height=val["height"], display_point=val["display_point"], color=number_to_rainbow(idx, len(data)))
        end_list.append(end)
        vertex_y_list.append(vertex_y)

    # # 그래프 범위 제한
    end = max(end_list)
    vertex_y = max(vertex_y_list)
    plt.xlim(-40, end+(end*50/100))
    if vertex_y !=0:
        plt.ylim(0, vertex_y+(vertex_y*10/100))
    return end_list, vertex_y_list



plt.figure(figsize=(16,9))
# plt.style.use('fivethirtyeight')


# 한글 추가
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# 축 이름 설정
plt.xlabel(f'이동거리')
plt.ylabel(f'이동높이')
# 그리드 추가
plt.grid(color = "gray", alpha=.5,linestyle='--')
plt.axhline(y=0, color='r', linewidth=1)
plt.axvline(x=0, color='r', linewidth=1)



data = [
    {
        "dgree" : 0,
        "velocity" : 40,
        "height" : 0,
        "display_point" : [False, True, True]
    },
    {
        "dgree" : 30,
        "velocity" : 40,
        "height" : 0,
        "display_point" : [False, True, True]
    },
    {
        "dgree" : 45,
        "velocity" : 40,
        "height" : 0,
        "display_point" : [False, True, True]
    },
    {
        "dgree" : 60,
        "velocity" : 40,
        "height" : 0,
        "display_point" : [False, True, True]
    },
    {
        "dgree" : 90,
        "velocity" : 40,
        "height" : 0,
        "display_point" : [False, True, True]
    }
]

def make_spet():
    plt.title(f"수직높이-수평거리 스펙트럼 | 발사속도: 55m/s | 발사높이: 0m\n", fontweight='bold')
    data = []
    for i in range(0,90):
        data.append({
        "dgree" : i,
        "velocity" : 55,
        "height" : 0,
        "display_point" : [False, False, False]
        })

    draws_mult_parabolic(make_spet())

    # return data


def make_image_each():
    data = []
    for i in range(0,90):
        data.append({
        "dgree" : i,
        "velocity" : 55,
        "height" : 0,
        "display_point" : [False, False, False]
        })
        end_list, vertex_y_list = draws_mult_parabolic(data)
        plt.axvline(x=0, color='r', linewidth=1)
        plt.title(f'{i}도 발사, 도달높이: {vertex_y_list[-1]:.2f}m, 도달거리: {end_list[-1]:.2f}m', fontweight='bold')
        plt.xlabel(f'이동거리')
        plt.ylabel(f'이동높이')
        plt.savefig(f'2D/{i}.png', format='png')
        plt.clf()
    return data



def _animate(i, *frags):
    print(i, end="\r")
    if i>90:
        i = 90
    end, vertex_y = print_one_parabolic(degree=i, velocity=frags[0], height=frags[1], color=number_to_rainbow(i, 91), display_point=frags[2])

    plt.axvline(x=0, color='r', linewidth=1)
    plt.title(f'{i}도 발사, 도달높이: {vertex_y:.2f}m, 도달거리: {end:.2f}m, 발사속도: {frags[0]}m/s, 발사높이: {frags[1]}m\n', fontweight='bold')

def make_image_ani(velocity, height=0):
    plt.style.use('fivethirtyeight')
    
    data = (velocity, height, [0,0,0])

    ani = FuncAnimation(plt.gcf(), _animate, frames=150, interval=1, fargs=data)
    ani.save('./animation_single2.gif', fps=15)
    print('GIF_make_finish')


# draws_mult_parabolic(data)
# plt.title(f"수직높이-수평거리 그래프 | 발사속도: {data[0]['velocity']}m/s | 발사높이: {data[0]['height']}m\n", fontweight='bold')
# plt.savefig("./030456090.png", format="png")

make_image_ani(
    velocity=55, height=0
)


# 범례(이름) 표기
# plt.legend()

# 창 크기



# 출력
# plt.show()