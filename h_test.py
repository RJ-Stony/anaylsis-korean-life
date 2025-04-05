"""
통계 분석 기법을 이용한 가설 검정
"""

# t 검정
# compact 자동차와 suv 자동차의 도시 연비

import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

mpg = pd.read_csv('./data/mpg.csv')

mpg['category'].value_counts()

# 기술 통계 분석
## compact, suv 추출
## category별 분리
## 빈도 구하기
## cty 평균 구하기

com_suv = mpg.query("category in ['compact', 'suv']").groupby('category', as_index=False).agg(total=('category', 'count'), mean=('cty', 'mean'))
com_suv

'''
  category  total      mean
0  compact     47  20.12766
1      suv     62  13.50000
'''

# t 검정
## mpg에서 category가 'compact' => cty
## mpg에서 category가 'suv' => cty
compact = mpg.query("category == 'compact'")['cty']
suv = mpg.query("category == 'suv'")['cty']

# t-test: stats.ttest_ind(compact, suv, equal_var=True)
## equal_var=True: 집단(변수) 분산이 같음
stats.ttest_ind(compact, suv, equal_var=True)
'''
TtestResult(statistic=11.917282584324107, 
            pvalue=2.3909550904711282e-21, 
            df=107.0)
'''

# t 검정
# 일반 휘발유와 고급 휘발유의 도시 연비

# 기술 통계 분석
## r, p 추출
## fl별 분리
## 빈도 구하기
## cty 평균 구하기

rp = mpg.query("fl in ['r', 'p']").groupby('fl', as_index=False).agg(total=('fl', 'count'), mean=('cty', 'mean'))
rp
'''
  fl  total       mean
0  p     52  17.365385
1  r    168  16.738095
'''

regular = mpg.query("fl == 'r'")['cty']
premium = mpg.query("fl == 'p'")['cty']

stats.ttest_ind(regular, premium, equal_var=True)
'''
TtestResult(statistic=-1.066182514588919,
            pvalue=0.28752051088667036,
            df=218.0)
'''

'''
실제로 봤을 때는 차이가 없는데
우연에 의해 이런 정도의 차이가 관찰될 확률이 28%

일반 휘발유와 고급 휘발유를 사용하는 도시 연비 차이가 통계적으로 유의하지 않다

고급 휘발유 도시 연비 평균이 0.6 정도 높지만
이런 정도의 차이는 우연히 발생했을 가능성이 크다
'''

'''
상관 분석 - 두 변수의 관계 분석
상관 분석을 통해 도출된 상관 계수 값으로 관련성 여부 판단 가능

상관 계수는 -1~1 사이의 값
'''

economics = pd.read_csv('./data/economics.csv')

# 실업자 수(unemploy)와 개인 소비 지출(pce)의 상관 관계
economics[['unemploy', 'pce']].corr()
'''
상관 행렬
          unemploy       pce
unemploy  1.000000  0.614518
pce       0.614518  1.000000
'''

# 유의 확률 구하기: stats.pearsonr()
stats.pearsonr(economics['unemploy'], economics['pce'])
'''
PearsonRResult(statistic=0.6145176141932082, 
               pvalue=6.773527303289964e-61)
'''

# 상관 행렬 히트맵: mtcars.csv
mtcars = pd.read_csv('./data/mtcars.csv')

car_cor = mtcars.corr()
car_cor = round(car_cor, 2)
car_cor

plt.rcParams.update({'figure.dpi': '120',
                     'figure.figsize': [7.5, 5.5]})
plt.rcParams['axes.unicode_minus'] = False

sns.heatmap(car_cor, annot=True, cmap='RdBu', square=True)
plt.show()

import numpy as np
mask = np.zeros_like(car_cor)

# 오른쪽 위 대각 행렬을 1로 바꾸기
mask[np.triu_indices_from(mask)] = 1
mask

sns.heatmap(car_cor, annot=True, cmap='RdBu', 
            square=True, mask=mask)
plt.show()

mask_new = mask[1:, :-1]
cor_new = car_cor.iloc[1:, :-1]

sns.heatmap(cor_new, annot=True, cmap='RdBu', 
            square=True, mask=mask_new)
plt.show()
