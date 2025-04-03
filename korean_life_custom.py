# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:40:40 2025

@author: Roh Jun Seok

주제(자유) 하나 잡고
하위 목표는 3개 이상 잡고,
전체 주제에 대한 결론 도출

h14_g3(성별), 
h14_g11(종교), 
h14_g10(혼인상태), 
h14_g4(태어난 연도), 
p1402_8aq1(소득), 
h14_eco9(직업 코드), 
h14_reg7(지역 코드)
제외
"""

'''
하위 목표 결론 도출을 위한 시각화 자료
pdf로 제출 (17:40까지)
aiffall@naver.com
'''

'''
주제: 근로 조건과 삶의 질의 관계

하위 목표 1. 근로시간 유형(h14_eco6)과 건강 상태(h14_med2)의 관계
- 과연 장시간 근로자가 건강이 더 안 좋을까?
- 건강이 좋지 않은 사람들이 시간제 근로를 선택하는 경향이 있나?

하위 목표 2. 비경제활동 사유(h14_eco11)와 건강검진 횟수(h14_med8)의 관계
- 경제활동을 하지 않는 사람들이 건강검진을 더 적게 받을까?

하위 목표 3. 사업장 규모(h14_eco10)와 근로 지속 가능성(h14_eco_7_2)의 관계
- 대기업일수록 근로 안정성이 높아질까?
- 간접고용(하청, 용역 등)이 해고 위험성이 더 높은지 분석

하위 목표 4. 고용 관계(h14_eco5_1)와 근로계약기간 설정 여부(h14_eco_7_1)의 관계
- 직접고용, 간접고용, 특수고용 중 어떤 것에 정규직이 더 많을까?
- 계약기간이 없는 근로자가 더 안정적인 고용 형태인가?

하위 목표 5. 경제활동 참여 상태(h14_eco4_1)와 의료 이용 횟수(h14_med3, h14_med4)의 관계"
- 경제활동 상태(취업자 vs. 실업자 vs. 비경제활동인구)별로 의료기관 방문 횟수 차이가 있을까?
- 경제활동을 하지 않는 사람(비경제활동인구)이 의료기관을 더 자주 방문할까?
- 고용 형태(상용직, 임시직, 일용직, 자영업자 등)에 따라 의료기관 방문 횟수가 다른가?
- 안정적인 직업(상용직 vs. 고용주)과 불안정한 직업(임시직, 일용직, 실업자) 간 의료 이용 패턴이 다른가?
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='darkgrid')

raw_welfare = pd.read_spss('./data/Koweps_hpwc14_2019_beta2.sav')
wf = raw_welfare.copy()

wf.head()
wf.shape
wf.info()

wf = wf.rename(columns={'h14_med2': 'health_type',
                        'h14_med3': 'num_treat',
                        'h14_med4': 'num_hospital',
                        'h14_med8': 'num_checkup',
                        'h14_eco4': 'status_eco',
                        'h14_eco5_1': 'employ_rel',
                        'h14_eco6': 'work_hour',
                        'h14_eco_7_1': 'contract_type',
                        'h14_eco_7_2': 'work_sustain',
                        'h14_eco10': 'business_size',
                        'h14_eco11': 'reason_dont_work'
                        })

'''
근로시간형태: 1. 시간제 / 2. 전일제
건강상태: 1.아주 건강하다 / 2.건강한 편이다 / 3.보통이다 / 
        4.건강하지 않은 편이다 / 5.건강이 아주 안 좋다
        
비경제활동사유: 1. 근로무능력 / 2. 군복무 / 3. 정규교육기관 학업 / 4. 진학준비 /
             5. 취업준비 / 6. 가사 / 7. 양육 / 8. 간병 / 9. 구직활동포기 / 
             10. 근로의사 없음 / 11. 기타
1년간 건강검진 횟수	: 횟수

사업장규모: 1. 1~4명 / 2. 5~9명 / 3. 10~29명 / 4. 30~49명 / 
          5. 50~69명 / 6. 70~99명 / 7. 100~299명 / 8. 300~499명
          9. 500~999명 / 10. 1000명 이상 / 11. 잘 모르겠다.

고용관계:	1. 직접고용 / 2. 간접고용 / 3. 특수고용

근로계약기간 설정여부: 1. 계약기간이 정해져 있음 / 2. 계약기간이 정해져 있지 않음

근로지속가능성: 1. 특별한 사유(본인의 중대한 과실, 폐업 등 사업체 자체의 소멸 또는 
   고용조정, 천재지변 등)가 없는 한 계속 근로가 가능함 
             2. 본인의 의사와 무관하게 회사의 사정에 따라 언제든지 해고될 수 있음

경제활동 참여상태(12월 31일기준): 1. 상용직 임금근로자 / 2. 임시직 임금근로자 /
                             3. 일용직 임금근로자 / 
                             4. 자활근로, 공공근로, 노인일자 / 5. 고용주 /
                             6. 자영업자 / 7. 무급가족종사자
                             8. 실업자(지난 4주간 적극적으로 구직활동을 함)
                             9. 비경제 활동인구

1년간 의료기관 이용 외래진료횟수: 횟수
1년간 의료기관 이용 입원횟수: 횟수
'''

'''
하위 목표 1. 근로시간 유형(h14_eco6)과 건강 상태(h14_med2)의 관계
- 과연 장시간 근로자가 건강이 더 안 좋을까?
- 건강이 좋지 않은 사람들이 시간제 근로를 선택하는 경향이 있나?

근로시간형태: 1. 시간제 / 2. 전일제
건강상태: 1.아주 건강하다 / 2.건강한 편이다 / 3.보통이다 / 
        4.건강하지 않은 편이다 / 5.건강이 아주 안 좋다
'''

# 변수 검토 및 전처리
wh_ht = wf[['work_hour', 'health_type']].copy()
wh_ht = wh_ht.dropna()

wh_ht.dtypes
wh_ht['work_hour'].value_counts()
wh_ht['health_type'].value_counts()

wh_ht['work_hour'] = np.where(wh_ht['work_hour'] == 1, '시간제', '전일제')
wh_ht['work_hour'].value_counts()

wh_ht['health_type'] = np.where((wh_ht['health_type'] == 1) | (wh_ht['health_type'] == 2), 'healthy',
                       np.where((wh_ht['health_type'] == 4) | (wh_ht['health_type'] == 5), 'unhealthy', 'normal'))
wh_ht['health_type'].value_counts()

plt.rcParams.update({'font.family':'Malgun Gothic'})

# 색상 매핑
color_mapping = {'healthy': 'cornflowerblue', 'normal': 'lightgray', 'unhealthy': 'lightcoral'}

# 근로시간 유형별 건강 상태 분포 (막대 그래프)
plt.figure(figsize=(8, 5))
sns.countplot(data=wh_ht, x='work_hour', hue='health_type',
              palette=color_mapping, hue_order=['healthy', 'normal', 'unhealthy'])
plt.title("근로시간 유형별 건강 상태 분포")
plt.xlabel("근로시간 유형")
plt.ylabel("건수")
plt.legend(title="건강 상태")
plt.show()

# 근로시간 유형별 건강 상태 비율 (비율 스택 바 차트)
cross_tab = pd.crosstab(wh_ht['work_hour'], wh_ht['health_type'], normalize='index')

ax = cross_tab[['healthy', 'normal', 'unhealthy']].plot(
    kind='bar', stacked=True, figsize=(8, 5), color=[color_mapping['healthy'], color_mapping['normal'], color_mapping['unhealthy']]
)
plt.title("근로시간 유형별 건강 상태 비율")
plt.xlabel("근로시간 유형")
plt.ylabel("비율")
plt.legend(title="건강 상태")
plt.xticks(rotation=0)
plt.show()

# 근로시간 유형별 건강 상태 분포 (파이 차트)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for i, work_type in enumerate(wh_ht['work_hour'].unique()):
    data = wh_ht[wh_ht['work_hour'] == work_type]['health_type'].value_counts()
    axes[i].pie(data, labels=data.index, autopct='%1.1f%%', 
                colors=[color_mapping[label] for label in data.index])
    axes[i].set_title(f"{work_type} 근로자의 건강 상태 분포")

plt.show()

'''
전일제(풀타임) 근로자의 경우, 78.5%가 'healthy', 5.7%가 'unhealthy'
시간제(파트타임) 근로자는 51.0%가 'healthy', 19.7%가 'unhealthy'

시간제 근로자가 전일제 근로자보다 건강이 나쁜 비율이 더 높음.
장시간 근로자가 건강이 더 안 좋다는 가설은 명확하게 성립 X
오히려 시간제 근로자의 건강이 더 나쁜 경향
'''

'''
시간제 근로자의 'unhealthy' 비율이 전일제 근로자보다 훨씬 높음(19.7% vs. 5.7%)
시간제 근로자의 'normal' 비율도 더 높음(29.3% vs. 15.8%)

건강이 좋지 않은 사람들이 시간제 근로를 선택하는 경향?
건강 문제로 인해 풀타임 근무를 하기 어려운 사람들이 시간제 근로를 선택할 가능성이 큼
'''

'''
하위 목표 2. 비경제활동 사유(h14_eco11)와 건강검진 횟수(h14_med8)의 관계
- 경제활동을 하지 않는 사람들이 건강검진을 더 적게 받을까?
비경제활동사유: 1. 근로무능력 / 2. 군복무 / 3. 정규교육기관 학업 / 4. 진학준비 /
             5. 취업준비 / 6. 가사 / 7. 양육 / 8. 간병 / 9. 구직활동포기 / 
             10. 근로의사 없음 / 11. 기타
1년간 건강검진 횟수	: 횟수
'''

# 변수 검토 및 전처리
rdw_nc = wf[['reason_dont_work', 'num_checkup']].copy()
rdw_nc.isna().sum()
rdw_nc = rdw_nc.dropna()

rdw_nc = rdw_nc[(rdw_nc['num_checkup'] != 10) & (rdw_nc['num_checkup'] != 3)]

rdw_nc.dtypes
rdw_nc['reason_dont_work'].value_counts()
rdw_nc['num_checkup'].value_counts()

rdw_nc['work_reason'] = np.select(
    [
        rdw_nc['reason_dont_work'].isin([1, 9, 10]),  # 건강 문제 그룹
        rdw_nc['reason_dont_work'].isin([3, 4, 5]),   # 교육·취업 준비 그룹
        rdw_nc['reason_dont_work'].isin([6, 7, 8]),   # 돌봄·가사 그룹
        rdw_nc['reason_dont_work'].isin([2, 11])      # 기타 그룹
    ],
    [
        '건강문제',   # 건강 문제
        '교육취업',  # 교육·취업 준비
        '돌봄가사', # 돌봄·가사
        '기타'           # 기타 (군복무 등)
    ],
    default='기타'
)

rdw_nc['work_reason'].value_counts()
rdw_nc['num_checkup'].value_counts()

# 비경제활동 사유별 건강검진 횟수 분포 (박스플롯)
plt.figure(figsize=(8, 5))
sns.boxplot(data=rdw_nc, x='work_reason', y='num_checkup', hue='work_reason', 
            palette='coolwarm', order=['건강문제', '교육취업', '돌봄가사', '기타'], dodge=False)
plt.title("비경제활동 사유별 건강검진 횟수 분포")
plt.xlabel("비경제활동 사유")
plt.ylabel("건강검진 횟수")
plt.xticks(rotation=0)
plt.show()

# 비경제활동 사유별 건강검진 횟수 평균 비교 (바 차트)
plt.figure(figsize=(8, 5))
sns.barplot(data=rdw_nc, x='work_reason', y='num_checkup', hue='work_reason', 
            palette='coolwarm', 
            order=['건강문제', '교육취업', '돌봄가사', '기타'], 
            estimator=lambda x: sum(x)/len(x),
            errorbar=None)
plt.title("비경제활동 사유별 평균 건강검진 횟수")
plt.xlabel("비경제활동 사유")
plt.ylabel("평균 건강검진 횟수")
plt.xticks(rotation=0)
plt.show()

# 비경제활동 사유별 건강검진 횟수 히스토그램
plt.figure(figsize=(8, 5))
sns.histplot(data=rdw_nc, x='num_checkup', hue='work_reason', element='step', palette='coolwarm', bins=10)
plt.title("비경제활동 사유별 건강검진 횟수 분포")
plt.xlabel("건강검진 횟수")
plt.ylabel("빈도")
plt.show()

'''
전반적으로 건강검진 횟수는 낮은 편
대부분의 비경제활동 그룹에서 건강검진 횟수가 0~1회로 매우 적음

교육이나 취업 준비 그룹이 특히 건강검진을 가장 적게 받는 경향
건강 문제나 돌봄/가사 그룹은 평균적으로 건강검진 횟수가 더 높음

경제활동을 하지 않는다고 해서 건강검진을 덜 받는다고 단정 불가
- 건강 상태나 생활 패턴에 따라 건강검진 횟수가 달라질 수 있음
'''

'''
하위 목표 3. 사업장 규모(h14_eco10)와 근로 지속 가능성(h14_eco_7_2)의 관계
- 대기업일수록 근로 안정성이 높아질까?
- 간접고용(하청, 용역 등)이 해고 위험성이 더 높은지 분석

사업장규모: 1. 1~4명 / 2. 5~9명 / 3. 10~29명 / 4. 30~49명 / 
          5. 50~69명 / 6. 70~99명 / 7. 100~299명 / 8. 300~499명
          9. 500~999명 / 10. 1000명 이상 / 11. 잘 모르겠다.
          
근로지속가능성: 1. 특별한 사유(본인의 중대한 과실, 폐업 등 사업체 자체의 소멸 또는 
             고용조정, 천재지변 등)가 없는 한 계속 근로가 가능함 
             2. 본인의 의사와 무관하게 회사의 사정에 따라 언제든지 해고될 수 있음
'''

# 변수 검토 및 전처리
bs_ws = wf[['business_size', 'work_sustain']].copy()
bs_ws.isna().sum()

bs_ws = bs_ws.dropna()
bs_ws.shape

bs_ws['business_size'].value_counts()

bs_ws = bs_ws[bs_ws['business_size'] != 11]

bs_ws['business_size_group'] = np.select(
    [
        bs_ws['business_size'].isin([1, 2, 3, 4]),  # 소규모 사업장 (1~49명)
        bs_ws['business_size'].isin([5, 6, 7]),      # 중간규모 사업장 (50~299명)
        bs_ws['business_size'].isin([8, 9, 10])     # 대규모 사업장 (300명 이상)
    ],
    [
        '소규모',  # 1~49명
        '중간규모', # 50~299명
        '대규모'   # 300명 이상
    ],
    default='기타'
)

bs_ws['business_size_group'].value_counts()

bs_ws['work_sustain'] = np.where(bs_ws['work_sustain'] == 1, '근로가능', '해고가능')
bs_ws['work_sustain'].value_counts()

color_mapping = {'근로가능': 'cornflowerblue', '해고가능': 'lightcoral'}

# 사업장 규모별 근로 지속 가능성 분포 (막대 그래프)
plt.figure(figsize=(8, 5))
sns.countplot(data=bs_ws, x='business_size_group', hue='work_sustain', 
              palette=color_mapping, order=['소규모', '중간규모', '대규모'])
plt.title("사업장 규모별 근로 지속 가능성 분포")
plt.xlabel("사업장 규모")
plt.ylabel("건수")
plt.legend(title="근로 지속 가능성")
plt.xticks(rotation=0)
plt.show()

# 사업장 규모별 근로 지속 가능성 비율 (스택 바 차트)
cross_tab = pd.crosstab(bs_ws['business_size_group'], bs_ws['work_sustain'], normalize='index')

# 원하는 순서로 인덱스 정렬
cross_tab = cross_tab.reindex(['소규모', '중간규모', '대규모'])

# 스택 바 차트 그리기
cross_tab[['근로가능', '해고가능']].plot(
    kind='bar', stacked=True, figsize=(8, 5), 
    color=[color_mapping['근로가능'], color_mapping['해고가능']]
)
plt.title("사업장 규모별 근로 지속 가능성 비율")
plt.xlabel("사업장 규모")
plt.ylabel("비율")
plt.legend(title="근로 지속 가능성")
plt.xticks(rotation=0)
plt.show()

'''
대기업일수록 근로 안정성이 높아지는 경향
사업장 규모가 클수록 구조조정이나 폐업의 가능성이 낮고, 해고율도 감소
소규모 사업장은 고용 불안정성이 높은 것으로 추정

=> 대기업일수록 근로 안정성이 높다?!
'''

'''
하위 목표 4. 고용 관계(h14_eco5_1)와 근로계약기간 설정 여부(h14_eco_7_1)의 관계
- 직접고용, 간접고용, 특수고용 중 어떤 것에 정규직이 더 많을까?
- 계약기간이 없는 근로자가 더 안정적인 고용 형태인가?

고용관계:	1. 직접고용 / 2. 간접고용 / 3. 특수고용
근로계약기간 설정여부: 1. 계약기간이 정해져 있음 / 2. 계약기간이 정해져 있지 않음
'''

# 변수 검토 및 전처리
er_ct = wf[['employ_rel', 'contract_type']].copy()
er_ct.isna().sum()

er_ct = er_ct.dropna()
er_ct.shape

er_ct['employ_rel'].value_counts()

er_ct['employ_rel'] = np.where(er_ct['employ_rel'] == 1, '직접고용', 
                      np.where(er_ct['employ_rel'] == 2, '간접고용', '특수고용'))
er_ct['employ_rel'].value_counts()

er_ct['contract_type'] = np.where(er_ct['contract_type'] == 1, '기간제',
                                  '무기계약')
er_ct['contract_type'].value_counts()

# 색상 매핑 수정
color_mapping = {'기간제': 'lightcoral', '무기계약': 'cornflowerblue'}
employ_color_mapping = {'직접고용': 'cornflowerblue', '간접고용': 'lightcoral', '특수고용': 'lightgray'}

# 고용 유형별 계약 유형 분포 (막대 그래프)
plt.figure(figsize=(8, 5))
sns.countplot(data=er_ct, x='employ_rel', hue='contract_type', palette=color_mapping, 
              order=['직접고용', '간접고용', '특수고용'])
plt.title("고용 유형별 계약 유형 분포")
plt.xlabel("고용 유형")
plt.ylabel("건수")
plt.legend(title="계약 유형")
plt.xticks(rotation=0)
plt.show()

cross_tab = pd.crosstab(er_ct['employ_rel'], er_ct['contract_type'], normalize='index')

cross_tab = cross_tab.reindex(['직접고용', '간접고용', '특수고용'])  # 원하는 순서로 정렬
cross_tab.plot(kind='bar', stacked=True, figsize=(8, 5), color=[color_mapping['기간제'], color_mapping['무기계약']])
plt.title("고용 유형별 계약 유형 비율")
plt.xlabel("고용 유형")
plt.ylabel("비율")
plt.legend(title="계약 유형")
plt.xticks(rotation=0)
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
employment_categories = ['직접고용', '간접고용', '특수고용']

for i, category in enumerate(employment_categories):
    data = er_ct[er_ct['employ_rel'] == category]['contract_type'].value_counts()
    colors = [color_mapping[label] for label in data.index]
    axes[i].pie(data, labels=data.index, autopct='%1.1f%%', colors=colors)
    axes[i].set_title(f"{category} 근로자의 계약 유형 분포")

plt.show()

# 히트맵을 위한 교차 테이블 생성
heatmap_data = pd.crosstab(er_ct['employ_rel'], er_ct['contract_type'], normalize='index')

plt.figure(figsize=(6, 4))
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("고용 유형별 계약 유형 비율")
plt.xlabel("계약 유형")
plt.ylabel("고용 유형")
plt.show()

'''
정규직(무기계약) 비율이 가장 높은 고용 형태는 직접고용 > 특수고용 > 간접고용 순서
간접고용(하청, 용역 등)은 대부분이 계약직(기간제) 근로자이며, 정규직 비율이 가장 낮음
특수고용(프리랜서 등)은 무기계약 비율이 높지만, 고용 안정성이 실제로 높다고 단정하기 어려움

정규직(무기계약) 근로자는 직접고용에서 가장 많으므로, 직접고용이 상대적으로 안정적인 고용 형태
간접고용은 대부분이 기간제(계약직)이므로, 고용 안정성이 가장 낮음
특수고용의 무기계약 비율이 높지만, 법적 보호가 부족
'''

'''
하위 목표 5. 경제활동 참여 상태(h14_eco4_1)와 의료 이용 횟수(h14_med3, h14_med4)의 관계"

경제활동 상태(취업자 vs. 실업자 vs. 비경제활동인구)별로 의료기관 방문 횟수 차이가 있을까?
경제활동을 하지 않는 사람(비경제활동인구)이 의료기관을 더 자주 방문할까?

고용 형태(상용직, 임시직, 일용직, 자영업자 등)에 따라 의료기관 방문 횟수가 다른가?
안정적인 직업(상용직 vs. 고용주)과 불안정한 직업(임시직, 일용직, 실업자) 간 의료 이용 패턴이 다른가?


주된 경제활동 참여상태: 1. 상용직 임금근로자 / 2. 임시직 임금근로자 /
                    3. 일용직 임금근로자 / 
                    4. 자활근로, 공공근로, 노인일자 / 5. 고용주 /
                    6. 자영업자 / 7. 무급가족종사자
                    8. 실업자(지난 4주간 적극적으로 구직활동을 함)
                    9. 비경제 활동인구

1년간 의료기관 이용 외래진료횟수: 횟수
1년간 의료기관 이용 입원횟수: 횟수
'''

# 변수 검토 및 전처리
se_ntnh = wf[['status_eco', 'num_treat', 'num_hospital']].copy()
se_ntnh.isna().sum()

se_ntnh = se_ntnh.dropna()
se_ntnh.shape

se_ntnh['status_eco'].value_counts()

se_ntnh['status_group'] = np.select(
    [
        se_ntnh['status_eco'].isin([1, 5, 6]),
        se_ntnh['status_eco'].isin([2, 3, 4]),
        se_ntnh['status_eco'].isin([7, 8, 9]),
    ],
    [
        '안정경제활동',  # 상용직 + 자영업자 + 고용주
        '불안정경제활동',  # 임시직 + 일용직 + 공공근로
        '비경제활동',  # 무급가족종사자 + 실업자 + 비경제활동인구
    ],
    default='기타'
)

se_ntnh['num_hospital'] = np.where(se_ntnh['num_hospital'] == 0, '비입원',
                                  '입원')
se_ntnh['num_hospital'].value_counts()

se_ntnh['num_hospital'] = np.where(se_ntnh['num_hospital'] == '비입원', 0, 1)
se_ntnh['num_hospital'] = se_ntnh['num_hospital'].astype(int)

se_ntnh = se_ntnh[se_ntnh['num_treat'] <= 25]
se_ntnh.shape

# 색상 매핑
color_mapping = {'안정경제활동': 'cornflowerblue', '불안정경제활동': 'lightcoral', '비경제활동': 'gray'}

# Boxplot (외래진료 횟수)
plt.figure(figsize=(8, 5))
sns.boxplot(data=se_ntnh, x='status_group', y='num_treat', palette=color_mapping)
plt.title("경제활동 상태별 외래진료 횟수 분포")
plt.xlabel("경제활동 상태")
plt.ylabel("외래진료 횟수")
plt.xticks(rotation=0)
plt.show()

from scipy.stats import ttest_ind

# 안정경제활동 vs. 비경제활동 (외래진료 횟수 비교)
group1 = se_ntnh[se_ntnh['status_group'] == '안정경제활동']['num_treat']
group2 = se_ntnh[se_ntnh['status_group'] == '비경제활동']['num_treat']

t_stat, p_value = ttest_ind(group1, group2, equal_var=False)  # 등분산 가정하지 않음
print(f"안정경제활동 vs. 비경제활동 외래진료 횟수 T-test: p-value = {p_value}")

group1 = se_ntnh[se_ntnh['status_group'] == '안정경제활동']['num_treat']
group2 = se_ntnh[se_ntnh['status_group'] == '불안정경제활동']['num_treat']

t_stat, p_value = ttest_ind(group1, group2, equal_var=False)
print(f"안정경제활동 vs. 불안정경제활동 외래진료 횟수 T-test: p-value = {p_value}")

# 크로스탭 생성 (입원 여부 비율 계산)
cross_tab_hospital = pd.crosstab(se_ntnh['status_group'], se_ntnh['num_hospital'], normalize='index')

# 누적 막대 그래프
cross_tab_hospital.plot(kind='bar', stacked=True, figsize=(8, 5), color=['lightgray', 'lightcoral'])
plt.title("경제활동 상태별 입원 여부 비율")
plt.xlabel("경제활동 상태")
plt.ylabel("비율")
plt.legend(title="입원 여부", labels=["비입원", "입원"])
plt.xticks(rotation=0)
plt.show()

from scipy.stats import pearsonr

corr_coef, p_value = pearsonr(se_ntnh['num_treat'], se_ntnh['num_hospital'])
print(f"외래진료 횟수와 입원 여부 간 상관 계수: {corr_coef:.3f}, p-value = {p_value}")

plt.figure(figsize=(8, 5))
sns.boxplot(data=se_ntnh, x='num_hospital', y='num_treat', palette=['lightgray', 'lightcoral'])
plt.title("입원 여부에 따른 외래진료 횟수 분포")
plt.xlabel("입원 여부 (0=비입원, 1=입원)")
plt.ylabel("외래진료 횟수")
plt.xticks(rotation=0)
plt.show()

group1 = se_ntnh[se_ntnh['num_hospital'] == 0]['num_treat']  # 비입원 그룹
group2 = se_ntnh[se_ntnh['num_hospital'] == 1]['num_treat']  # 입원 그룹

t_stat, p_value = ttest_ind(group1, group2, equal_var=False)
print(f"비입원 vs. 입원 외래진료 횟수 T-test: p-value = {p_value}")

se_ntnh['num_hospital'] = np.where(se_ntnh['num_hospital'] == 0, '비입원',
                                  '입원')

plt.figure(figsize=(10, 6))
sns.boxplot(data=se_ntnh, x='status_group', y='num_treat', hue='num_hospital',
            palette={'비입원': 'lightgray', '입원': 'lightcoral'})

plt.title("경제활동 상태별 외래진료 횟수 분포")
plt.xlabel("경제활동 상태")
plt.ylabel("외래진료 횟수")
plt.legend(title="입원 여부")
plt.xticks(rotation=0)
plt.show()

'''
비경제활동 상태일수록 의료 이용(외래진료 및 입원)이 더 많음

안정경제활동 < 불안정경제활동 < 비경제활동 순으로 의료기관 방문 횟수가 증가
경제적 안정성이 높은 직업군이 의료기관을 덜 방문
입원 가능성과 외래진료 횟수는 약한 상관관계

외래진료가 많다고 반드시 입원이 증가하는 것은 아님
하지만 외래진료를 많이 받는 그룹이 입원 가능성도 조금 더 높음
불안정한 경제활동 집단은 안정적인 직업군보다 의료기관 방문 횟수가 많음

일용직, 임시직, 공공근로 등 불안정한 직업군이 의료 이용을 더 자주 함
고용 불안정, 건강보험 혜택 차이, 근로환경 등의 영향일 가능성
'''

