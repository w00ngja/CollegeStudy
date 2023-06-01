import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import random
import folium

# 데이터 로드
df = pd.read_csv('population_housing_density_data.csv')

# 후보 위치 데이터
def generate_candidate_locations(num_locations):
    candidate_locations = []
    min_x = 0
    max_x = 10
    min_y = 0
    max_y = 10

    for _ in range(num_locations):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        candidate_locations.append((x, y))
    return candidate_locations

candidate_locations = generate_candidate_locations(1000)


# 보로노이 다이어그램 계산
vor = Voronoi(candidate_locations)

# 유동인구 밀도 및 주택밀도 가져오기
population_density = df['PopulationDensity'].values
housing_density = df['HousingDensity'].values

# 충전소 위치 선택을 위한 평가 기준 함수 정의
def evaluation_criteria(population_density, housing_density):
    # 평가 기준 계산 (예시로는 유동인구 밀도와 주택밀도의 합)
    return population_density + housing_density

# 충전소 위치 선택
charging_station_locations = []
for region in vor.regions:
    if len(region) > 0 and -1 not in region:
        x, y = vor.vertices[region][0]
        if x > 1 and y > 1:  # 예시 조건: x, y 값이 1보다 큰 위치 선택
            charging_station_locations.append((x, y))

# 충전소 위치 평가 기준 계산
evaluated_locations = []
for location in charging_station_locations:
    x, y = location
    x_index = int(x - 1)
    y_index = int(y - 1)
    if x_index < len(population_density) and y_index < len(housing_density):  # 인덱스 범위 체크
        population_density_val = population_density[x_index]
        housing_density_val = housing_density[y_index]
        evaluated_score = evaluation_criteria(population_density_val, housing_density_val)
        evaluated_locations.append((x, y, evaluated_score))

# 평가 기준에 따라 충전소 위치 정렬
evaluated_locations.sort(key=lambda x: x[2], reverse=True)
print(vor)

if evaluated_locations:
    center_lat, center_lon = 36.35368947186556, 127.34152365816226
    map = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # 최적의 충전소 위치 선택 (평가 기준 상위 위치)
    # 최적 입지 뽑아내기
    num_optimal_locations = 10  # 뽑아내고 싶은 최적 입지 개수 설정
    optimal_location = evaluated_locations[:num_optimal_locations]
    print(evaluated_locations)

    # 최적의 충전소 위치 출력
    print("Optimal Charging Station Location:", optimal_location)

    # 그래프 그리기
    voronoi_plot_2d(vor)
    candidate_x = [location[0] for location in candidate_locations]
    candidate_y = [location[1] for location in candidate_locations]
    plt.plot(candidate_x, candidate_y, 'ko', label='Candidate Locations')
    # plt.plot(optimal_location[0], optimal_location[1], 'ro', label='Optimal Location')

    # for loc in optimal_location:
    #     plt.plot(loc[0], loc[1], 'ro', label='Optimal Location')

    plt.plot([loc[0] for loc in optimal_location], [loc[1] for loc in optimal_location], 'ro',
             label='Optimal Location')
    plt.legend()

    # 최적 입지들을 지도에 마커로 표시
    for loc in optimal_location:
        folium.Marker(location=[loc[1], loc[0]], icon=folium.Icon(color='red')).add_to(map)

    # 지도 저장 및 표시
    map.save("map.html")

    # 그래프 축 범위 설정
    plt.xlim(vor.min_bound[0] - 1, vor.max_bound[0] + 1)
    plt.ylim(vor.min_bound[1] - 1, vor.max_bound[1] + 1)

    # 그래프 출력
    plt.show()
else:
    print("No evaluated locations found.")

