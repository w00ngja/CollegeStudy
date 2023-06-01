import pandas as pd
import numpy as np
import random
import folium
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

# 데이터 로드
df = pd.read_csv('population_housing_density_data.csv')

# 위도
min_x = 36.2
max_x = 36.5

# 경도
min_y = 127.3
max_y = 127.5

# 후보 위치 데이터
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

# 가중치 설정
w_population = 0.4  # 인구밀도 가중치
w_housing = 0.2  # 주택밀도 가중치
w_area = 0.4  # 다각형 면적 가중치

# 주택밀도 데이터 예시 (100개)
housing_density = []
for _ in range(100):
    latitude = random.uniform(36.2, 36.5)  # 대전 근처 위도 범위 예시
    longitude = random.uniform(127.3, 127.5)  # 대전 근처 경도 범위 예시
    density = random.randint(1, 10)  # 임의의 주택밀도 예시
    housing_density.append((latitude, longitude, density))

# 인구밀도 데이터 예시 (100개)
population_density = []
for _ in range(100):
    latitude = random.uniform(36.2, 36.5)  # 대전 근처 위도 범위 예시
    longitude = random.uniform(127.3, 127.5)  # 대전 근처 경도 범위 예시
    density = random.randint(100, 1000)  # 임의의 인구밀도 예시
    population_density.append((latitude, longitude, density))

# 평가 기준에 사용할 다각형의 넓이 계산
polygon_areas = []
for region in vor.regions:
    if len(region) > 0 and -1 not in region:
        vertices = vor.vertices[region]
        polygon_area = abs(np.sum(vertices[:, 0] * np.roll(vertices[:, 1], 1) - vertices[:, 1] * np.roll(vertices[:, 0], 1))) / 2
        polygon_areas.append(polygon_area)

# 충전소 위치 선택을 위한 평가 기준 함수 정의
def evaluation_criteria(population_density, housing_density, polygon_area, w_population, w_housing, w_area):
    # 평가 기준 계산
    score = w_population * population_density + w_housing * housing_density + w_area * polygon_area
    return score

# 보로노이 다각형 중심점을 후보지로 선택
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
        folium.CircleMarker(location, radius=3, color='black', fill=True, fill_color='blue').add_to(candidate_map)

    optimal_map = folium.Map(location=[36.3, 127.4], zoom_start=13)
    for location in optimal_location:
        folium.CircleMarker(location[:2], radius=3, color='red', fill=True, fill_color='red').add_to(optimal_map)

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

    # 경도
    plt.xlabel('Longitude')

    # 위도
    plt.ylabel('Latitude')


    plt.title('Charging Station Locations')
    plt.legend()

    # 그래프 출력
    plt.show()
else:
    print("No evaluated locations found.")
