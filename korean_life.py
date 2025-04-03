import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.family':'Malgun Gothic'})
sns.set_theme(style='darkgrid', palette='pastel')

raw_welfare = pd.read_spss('./data/Koweps_hpwc14_2019_beta2.sav')
welfare = raw_welfare.copy()

welfare = welfare.rename(columns={'h14_g3': 'sex',
                                  'h14_g4': 'birth',
                                  'h14_g10': 'marriage_type',
                                  'h14_g11': 'religion',
                                  'p1402_8aq1': 'income',
                                  'h14_eco9': 'code_job',
                                  'h14_reg7': 'code_region'})

welfare['sex'] = np.where(welfare['sex'] == 1, 'male', 'female')

welfare = welfare.assign(age=2019-welfare['birth']+1)

welfare = welfare.assign(ageg = np.where(welfare['age'] < 30, 'young', np.where(welfare['age'] <= 59, 'middle', 'old')))

list_job = pd.read_excel('./data/Koweps_Codebook_2019.xlsx', sheet_name='직종코드')

welfare = welfare.merge(list_job, how='left', on='code_job')

'''
종교 유무에 따른 이혼율 - 종교가 있으면 이혼을 덜 할까?
'''

# 종교 변수 검토 및 전처리
welfare['religion'].dtypes

welfare['religion'].value_counts()

welfare['religion'].isna().sum()

welfare['religion'] = np.where(welfare['religion'] == 1, '종교', '무교')

welfare['religion'].value_counts()

sns.countplot(data=welfare, x='religion')
plt.show()

# 혼인 상태 변수 검토 및 전처리
welfare['marriage_type'].dtypes

welfare['marriage_type'].value_counts()

'''
marriage_type
1.0    7190   유배우
5.0    2357   미혼
0.0    2121   비해당
2.0    1954   사별
3.0     689   이혼
4.0      78   별거
6.0      29   기타
Name: count, dtype: int64
'''

welfare['marriage_type'].isna().sum()

welfare['marriage'] = np.where(welfare['marriage_type'] == 1, '결혼',
                      np.where(welfare['marriage_type'] == 3, '이혼', '기타'))

welfare['marriage'].value_counts()

'''
marriage
결혼    7190
기타    6539
이혼     689
Name: count, dtype: int64
'''

# 이혼 여부별 빈도
## 결혼별 분리
## 결혼별 빈도 구하기
n_divorce = welfare.groupby('marriage', as_index=False).agg(total=('marriage', 'count'))

sns.barplot(data=n_divorce, x='marriage', y='total')
plt.show()

# 종교 유무에 따른 이혼율 분석
## 종교 유무에 따른 이혼율표
### 기타는 제외
### religion별 분리
### marriage 추출
### 비율 구하기

rel_div = welfare.query("marriage != '기타'").groupby('religion', as_index=False)['marriage'].value_counts(normalize=True)
rel_div

'''
  religion marriage  proportion
0       무교       결혼    0.905045
1       무교       이혼    0.094955
2       종교       결혼    0.920469
3       종교       이혼    0.079531
'''

# divorce 추출 -> query
# 연산이 필요 -> assign

rel_div = rel_div.query("marriage == '이혼'").assign(proportion=rel_div['proportion'] * 100).round(1)
rel_div

plt.figure(figsize=(8,6))
sns.barplot(data=rel_div, x='religion', y='proportion', hue='religion', palette="coolwarm")
plt.title("종교 유무에 따른 이혼율", fontsize=16)
plt.xlabel("종교 유무", fontsize=14)
plt.ylabel("이혼율(%)", fontsize=14)
plt.tight_layout()
plt.show()

'''
연령대 및 종교 유무에 따른 이혼율 분석
'''

age_div = welfare.query("marriage != '기타'").groupby('ageg', as_index=False)['marriage'].value_counts(normalize=True)
age_div

'''
     ageg marriage  proportion
0  middle       결혼    0.910302
1  middle       이혼    0.089698
2     old       결혼    0.914220
3     old       이혼    0.085780
4   young       결혼    0.950000
5   young       이혼    0.050000
'''

# 연령대별 이혼율 시각화
## 초년층 제외, 이혼 추출
## 백분율로 바꾸기
## 반올림

age_div = age_div.query("ageg != 'young' & marriage == '이혼'").assign(proportion=age_div['proportion'] * 100).round(1)

sns.barplot(data=age_div, x='ageg', y='proportion')
plt.show()

# 연령대 및 종교 유무에 따른 이혼율표
## 기타 제외, 초년층 제외
## marriage 추출
## 비율 구하기

age_rel_div = welfare.query("ageg != 'young' & marriage != '기타'").groupby(['ageg', 'religion'], as_index=False)['marriage'].value_counts(normalize=True)
age_rel_div

'''
     ageg religion marriage  proportion
0  middle       무교       결혼    0.904953
1  middle       무교       이혼    0.095047
2  middle       종교       결혼    0.917520
3  middle       종교       이혼    0.082480
4     old       무교       결혼    0.904382
5     old       무교       이혼    0.095618
6     old       종교       결혼    0.922222
7     old       종교       이혼    0.077778
'''

# 시각화
## 이혼 추출
## 백분율로 바꾸기
## 반올림

age_rel_div = age_rel_div.query("marriage == '이혼'").assign(proportion=age_rel_div['proportion'] * 100).round(1)
age_rel_div

plt.figure(figsize=(10,6))
sns.barplot(data=age_rel_div, x='ageg', y='proportion', hue='religion', order=['middle', 'old'], palette="coolwarm")
plt.title("연령대 및 종교 유무에 따른 이혼율", fontsize=16)
plt.xlabel("연령대", fontsize=14)
plt.ylabel("이혼율(%)", fontsize=14)
plt.legend(title="종교 유무")
plt.tight_layout()
plt.show()

'''
지역별 연령대 비율 - 어느 지역에 노년층이 많을까?
'''

# 지역 변수 검토 및 전처리
welfare['code_region'].value_counts()
## 지역명 변수 추가
'''
1. 서울 / 2. 수도권(인천/경기), 3. 부산/경남/울산 ... 
'''
list_region = pd.DataFrame({'code_region': [1, 2, 3, 4, 5, 6, 7],
                            'region': ['서울', '수도권(인천/경기)', '부산/경남/울산', '대구/경북',
                                       '대전/충남', '강원/충북', '광주/전남/전북/제주도']})

welfare = welfare.merge(list_region, how='left', on='code_region')
welfare[['code_region', 'region']].head()

# 지역별 연령대 비율
## 지역별 연령대 비율표
### region별 분리
### ageg 추출
### 비율 구하기
region_ageg = welfare.groupby('region', as_index=False)['ageg'].value_counts(normalize=True)
region_ageg

region_ageg = region_ageg.assign(proportion=region_ageg['proportion'] * 100).round(1)
region_ageg

## 시각화 (막대, 누적)
### 막대 그래프
plt.figure(figsize=(10,8))
sns.barplot(data=region_ageg, y='region', x='proportion', hue='ageg', palette="Set2")
plt.title("지역별 연령대 분포", fontsize=16)
plt.xlabel("비율(%)", fontsize=14)
plt.ylabel("지역", fontsize=14)
plt.legend(title="연령대")
plt.tight_layout()
plt.show()

### 누적 그래프 => 피벗 테이블 사용!
'''
          region    ageg  proportion
0          강원/충북     old        45.9
1          강원/충북  middle        30.9
2          강원/충북   young        23.2
3   광주/전남/전북/제주도     old        44.9
4   광주/전남/전북/제주도  middle        31.8
'''

'''
피벗: 행과 열을 회전하여 표의 구성을 변경하는 작업
     누적 그래프 형태로 시각화할 때 사용
1. 지역, 연령대, 비율 <= 추출
2. DataFrame.pivot()
2-1. 지역을 기준으로 index=지역
2-2. 연령대별 컬럼을 구성 columns=[연령대]
2-3. 각 항목의 값을 비율값으로 채우기 위한 values=비율
'''

pivot_df = region_ageg[['region', 'ageg', 'proportion']].pivot(index='region', columns='ageg', values='proportion')
pivot_df

plt.figure(figsize=(10,8))
pivot_df.plot.barh(stacked=True)
plt.title("지역별 연령대 분포", fontsize=12)
plt.xlabel("비율(%)", fontsize=10)
plt.ylabel("지역", fontsize=10)
plt.legend(title="연령대")
plt.tight_layout()
plt.show()

reorder_df = pivot_df.sort_values('old')[['young', 'middle', 'old']]

plt.figure(figsize=(10,8))
reorder_df.plot.barh(stacked=True)
plt.title("지역별 연령대 분포", fontsize=12)
plt.xlabel("비율(%)", fontsize=10)
plt.ylabel("지역", fontsize=10)
plt.legend(title="연령대")
plt.tight_layout()
plt.show()
