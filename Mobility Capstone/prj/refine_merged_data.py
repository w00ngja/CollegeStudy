import pandas as pd
import numpy as np
import folium
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# 데이터 로드
# 법정동이름 | 위도 | 경도 | 전기차등록대수 | 충전소 수 | 전기차등록대수 대 충전소 비율 (퍼센트) | 연평균유동인구 | 보로노이 다각형 영역 크기
df = pd.read_csv('merged_data.csv')

# 좌표 추출 및 보로노이 연산
points = [(df.iloc[i].경도,df.iloc[i].위도) for i in range(df.shape[0])]
vor = Voronoi(points)

# 다각형 꼭짓점 인덱스(vor.regions)를 이용한 다각형 영역 넓이 계산
areas = []
for region in vor.regions:
    if len(region) > 0:
        polygon = Polygon(vor.vertices[region])
        area = polygon.area
        areas.append(area)

# 데이터 배열화 및 다각형 넓이 벡터 추가
df_array = np.array(df)
points = np.array(points)
areas = np.array(areas).reshape(52,1)

df_array = np.hstack((df_array,areas))
df_length = df_array.shape[0]

# 평가 스코어 부여 위한 항목별 정렬
# 전기차 대수 대 충전소 비율은 오름차순, 나머지 데이터는 내림차순
def sort(arr, column_idx, order):
    if order == 'ascending':
        return arr[arr[:,column_idx].argsort()[::1]]
    elif order == 'descending':
        return arr[arr[:,column_idx].argsort()[::-1]]
    else:
        return print("올바른 정렬순서를 입력해주세요")

sorted_charging_ratio = sort(df_array, 5, 'ascending')
sorted_foot_traffic = sort(df_array,6,'descending')
sorted_polygon_areas = sort(df_array,7,'descending')

# 항목별 스코어(인덱스) 부여
def evaluate_cr_score(arr):
    dst = np.array([])
    result = arr
    for i in range(df_length):
        if arr[:,3][i] == 0:
            dst = np.append(dst,50)
        else:
            dst = np.append(dst,i)

    result = np.hstack((arr,dst.reshape(df_length,1)))
    return result[result[:,0].argsort()[::1]]

def evaluate_normal_score(arr,column_idx):
    result = arr[arr[:, column_idx].argsort()[::-1]]
    dst = np.array([])
    for i in range(df_length):
            dst = np.append(dst,i)

    result = np.hstack((result,dst.reshape(df_length,1)))
    return result[result[:,0].argsort()[::1]]

cr_score = evaluate_cr_score(sorted_charging_ratio)
ft_score = evaluate_normal_score(cr_score,6)
pa_score = evaluate_normal_score(ft_score,7)

# 항목별 스코어 합산 후, 최종 스코어로 오름차순 정렬
final_score = pa_score[:,8] + pa_score[:,9] + pa_score[:,10]
final_score = np.hstack((pa_score,final_score.reshape(df_length,1)))
sorted_final_score = final_score[final_score[:, 11].argsort()[::1]]

if __name__ == "__main__":
    # 최종 스코어 상위 10개 지역 선정
    num_optimal_locations = 10
    optimal_locations = sorted_final_score[:num_optimal_locations]
    print("유성구 신규 충전소 설치 최적 입지 :",optimal_locations[:,0])

    # 보로노이 다각형 및 입지 그래프 시각화 (matplot)
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax)

    candidate_x = [location[2] for location in df_array]
    candidate_y = [location[1] for location in df_array]
    ax.plot(candidate_x, candidate_y, 'ko', label='Candidate Locations')

    optimal_x = [location[2] for location in optimal_locations]
    optimal_y = [location[1] for location in optimal_locations]
    ax.plot(optimal_x, optimal_y, 'ro', label='Optimal Locations')

    # 지도에 후보 입지 및 선정 입지 맵핑 (folium)
    result_map = folium.Map(location=[36.3686748,127.3463467], zoom_start=13)

    for i in range(df_length):
        folium.CircleMarker((df_array[:,1][i], df_array[:,2][i]), radius=20, color='black', fill=True,
                        fill_color='black').add_to(result_map)

    for i in range(num_optimal_locations):
        folium.CircleMarker((optimal_locations[:,1][i], optimal_locations[:,2][i]), radius=20, color='red', fill=True,
                        fill_color='red').add_to(result_map)

    result_map.save('ChargingStationOptimalLocations.html')

    # 그래프 범례 및 레이블 지정
    plt.xlabel('Longtitude')
    plt.ylabel('Latitude')

    plt.title('Charging Station Locations')
    plt.legend()

    plt.show()

