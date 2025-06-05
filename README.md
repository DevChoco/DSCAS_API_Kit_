# DSCAS_API_Kit
> deep-seasonal-color-analysis-system_API_Kit
> : 퍼스널 컬러 기반 옷 추천 AI 모델 - API Ver

Created by modifying [DSCAS](https://github.com/mrcmich/deep-seasonal-color-analysis-system).

-----
## 수정파일 정보
- `ds_cas_api.py` -> API 서버 코드
- `요청.py` -> API 클라이언트 Test 코드
- `pipeline_demo.ipynb` -> 수정된 leffa실행 테스트 코드
- `utils.py, retrieval_filter.py, dataset.py` -> 신체 카테고리를 설정해도 다른 카테고리의 옷이 출력되는 문제 수정 88(적절한 폴더에 수동저장 할 것!)88
- `dresscode_test_dataset` -> 옷 이미지 **(palette_classification 다시 실행해야함)**
-----
### API 실행 
`conda activate dscas` 접속 후
```
uvicorn ds_cas_api1:app --reload

or

uvicorn ds_cas_api1:app --reload
```
------
# 설치

## 설치전 작업
1. 우분투 아나콘다 설치 - 파이썬 3.10 - [아나콘다 설치 참고](https://github.com/kimsehyun-34/Data_Preprocessing/blob/main/README.md)
2. 우분투 아나콘다 주피터 노트북 설치

## 설치
1. clone DSCAS (우분투 아나콘다 콘솔)
```
git clone https://github.com/mrcmich/deep-seasonal-color-analysis-system.git
```
```
클론된 저장소로 이동
```
2. 추가 코드 clone
```
git clone https://github.com/DevChoco/DSCAS_API_Kit.git
```
3. 라이브러리 설치
```
pip install -r requirements.txt
```
