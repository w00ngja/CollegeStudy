import pandas as pd
import numpy as np

# 데이터 개수
data_size = 100

# 유동인구 밀도 데이터 생성
population_density_data = np.random.randint(1, 10, size=data_size)

# 주택밀도 데이터 생성
housing_density_data = np.random.randint(1, 10, size=data_size)

# 데이터프레임 생성
df = pd.DataFrame({'PopulationDensity': population_density_data,
                   'HousingDensity': housing_density_data})

# CSV 파일로 저장
df.to_csv('population_housing_density_data.csv', index=False)