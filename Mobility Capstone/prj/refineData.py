import pandas as pd

# 전기차 대수 별 충전소 비율
chargingstation_ratio = pd.read_csv('대수대충전소비.csv')
chargingstation_ratio = chargingstation_ratio.sort_values(by='법정동이름', ascending=True)
chargingstation_ratio = chargingstation_ratio.reset_index(drop=True)
chargingstation_ratio = chargingstation_ratio.drop(index=[21,24,26,34,51,52,53,54,58])
chargingstation_ratio = chargingstation_ratio.reset_index(drop=True)

print(chargingstation_ratio)

# 법정동별 좌표 (위도, 경도)
coord_location = pd.read_csv('위경도정제전.csv')
coord_location = coord_location[coord_location['시도']=='대전광역시']
coord_location = coord_location[coord_location['시군구']=='유성구']
coord_location = coord_location.loc[:, ['읍면동/구', '위도', '경도']]
coord_location = coord_location.sort_values(by='읍면동/구', ascending=True)
coord_location = coord_location[(coord_location['읍면동/구']!='구즉동') & (coord_location['읍면동/구']!='노은1동') & (coord_location['읍면동/구']!='노은2동') & (coord_location['읍면동/구']!='노은3동') &(coord_location['읍면동/구']!='온천1동') & (coord_location['읍면동/구']!='온천2동') & (coord_location['읍면동/구']!='진잠동')]
coord_location = coord_location.reset_index(drop=True)
coord_location = coord_location.drop(index=[52])
coord_location = coord_location.reset_index(drop=True)

print(coord_location)

# 일평균 유동인구 데이터
# 법정동 별로 총합하여 반기별 데이터로 정제하였음
daily_population = pd.read_csv('일평균유동.csv')
daily_population = daily_population.drop('시간대',axis=1)
daily_population = daily_population.drop('기준월',axis=1)
daily_population = daily_population.drop(range(0,1315))
daily_population = daily_population[(daily_population['법정동명']!='수남동')]
daily_population = daily_population.groupby('법정동명')['일평균유동인구'].sum()
yearly_population = daily_population.reset_index()

print(yearly_population)

# 데이터 취합 및 중복 Column 삭제
data_frames = [chargingstation_ratio, coord_location, yearly_population]
merged_data = pd.concat(data_frames,axis=1)
merged_data = merged_data.drop('읍면동/구',axis=1)
merged_data = merged_data.drop('법정동이름',axis=1)
merged_data = merged_data.iloc[:,[5,3,4,0,1,2,6]]

merged_data.to_csv('merged_data.csv', index=False)