import pandas as pd
import numpy as np
import random
import folium
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

# 데이터 로드 (샘플 시뮬레이션에서는 사용하지 않음)
df = pd.read_csv('population_housing_density_data.csv')

# 경도
min_x =127.3
max_x =  127.5
# 위도
min_y =  36.2
max_y =  36.5

# 후보 위치 데이터 함수 : 보로노이 연산을 위해 대전 인근에 랜덤 노드를 뿌림
def generate_candidate_locations(num_locations):
    candidate_locations = []

    for _ in range(num_locations):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        candidate_locations.append((x, y))
    return candidate_locations

# 후보지 선정 후, 보로노이 다이어그램 계산
candidate_locations = generate_candidate_locations(1000)
vor = Voronoi(candidate_locations)

# 가중치 설정 : 인구밀도, 주책밀도, 다각형의 넓이를 평가 기준으로 지정하였음
w_population = 0.4
w_housing = 0.2
w_area = 0.4

# 주택 / 인도밀도 샘플 데이터
# 대전 근처 위치(경도,위도)에서 (1,10) 영역의 값을 임의로 100개 생성해주었음
housing_density = []
for _ in range(100):
    latitude = random.uniform(36.2, 36.5)
    longitude = random.uniform(127.3, 127.5)
    density = random.randint(1, 10)
    housing_density.append((latitude, longitude, density))

population_density = []
for _ in range(100):
    latitude = random.uniform(36.2, 36.5)
    longitude = random.uniform(127.3, 127.5)
    density = random.randint(100, 1000)
    population_density.append((latitude, longitude, density))

# 보르노이 다각형 각 영역의 넓이 계산 : 셀 꼭짓점 간 신발끈 연산을 톻하여
# - vor.regions : 각 셀 인덱스 집합
# - vor.virtices[region] : 특정 셀의 꼭지점 정보
polygon_areas = []
for region in vor.regions:
    if len(region) > 0 and -1 not in region:
        vertices = vor.vertices[region]
        polygon_area = abs(np.sum(vertices[:, 0] * np.roll(vertices[:, 1], 1) - vertices[:, 1] * np.roll(vertices[:, 0], 1))) / 2
        polygon_areas.append(polygon_area)

# 부여한 가중치에 따라 최적 입지 선정을 위한 평가 기준 계산
def evaluation_criteria(population_density, housing_density, polygon_area, w_population, w_housing, w_area):
    score = w_population * population_density + w_housing * housing_density + w_area * polygon_area
    return score

# 각 셀의 중심점을 후보지로 선택
charging_station_locations = vor.points


# 충전소 위치 평가 기준 계산
evaluated_locations = []
for location, area in zip(charging_station_locations, polygon_areas):
    x, y = location
    x_index = int((x - min_x) / (max_x - min_x) * len(population_density))
    y_index = int((y - min_y) / (max_y - min_y) * len(housing_density))
    if 0 <= x_index < len(population_density) and 0 <= y_index < len(housing_density):  # 인덱스 범위 체크
        population_density_val = population_density[x_index][2]
        housing_density_val = housing_density[y_index][2]
        evaluated_score = evaluation_criteria(population_density_val, housing_density_val, area, w_population, w_housing, w_area)
        evaluated_locations.append((x, y, evaluated_score))

# 평가 기준에 따라 충전소 위치 정렬
evaluated_locations.sort(key=lambda x: x[2], reverse=True)

if evaluated_locations:
    # 최적의 충전소 위치 선택 (평가 기준 상위 위치)
    num_optimal_locations = 10  # 뽑아내고 싶은 최적 입지 개수 설정
    optimal_location = evaluated_locations[:num_optimal_locations]
    print("Optimal Charging Station Location:", optimal_location)

    # folium을 이용하여 후보지와 최적입지 지도에 시각화
    candidate_map = folium.Map(location=[36.3, 127.4], zoom_start=13)
    for location in candidate_locations:
        folium.CircleMarker((location[1],location[0]), radius=3, color='black', fill=True, fill_color='blue').add_to(candidate_map)

    optimal_map = folium.Map(location=[36.3, 127.4], zoom_start=13)
    for location in optimal_location:
        folium.CircleMarker((location[:2][1],location[:2][0]), radius=3, color='red', fill=True, fill_color='red').add_to(optimal_map)

    # 지도 출력
    candidate_map.save('candidate_locations_map.html')
    optimal_map.save('optimal_locations_map.html')

    # 그래프 그리기
    voronoi_plot_2d(vor)
    candidate_x = [location[0] for location in candidate_locations]
    candidate_y = [location[1] for location in candidate_locations]
    plt.plot(candidate_x, candidate_y, 'ko', label='Candidate Locations')

    optimal_x = [location[0] for location in optimal_location]
    optimal_y = [location[1] for location in optimal_location]
    plt.plot(optimal_x, optimal_y, 'ro', label='Optimal Locations')

    # 위도
    plt.xlabel('Latitude')
    # 경도
    plt.ylabel('longitude')

    plt.title('Charging Station Locations')
    plt.legend()

    # 그래프 출력
    plt.show()
else:
    print("No evaluated locations found.")
