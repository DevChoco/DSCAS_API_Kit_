from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
from PIL import Image
import torch
import io
import glob
import json
import os

from pipeline import pipeline, segmentation_filter, user_palette_classification_filter, retrieval_filter
from utils import segmentation_labels
from palette_classification import color_processing, palette

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 기본 설정
device = 'cuda' if torch.cuda.is_available() else 'cpu'
segmentation_model = 'cloud'

# 경로 설정
palettes_path = 'palette_classification/palettes/'
cloth_dataset_path = 'dresscode_test_dataset/'
palette_mappings_path = 'palette_classification/clothing_palette_mappings/'

# 팔레트 로딩 (서버 시작 시 1회만)
palette_filenames = glob.glob(palettes_path + '*.csv')
reference_palettes = [palette.PaletteRGB().load(p.replace('\\', '/'), header=True) for p in palette_filenames]

palette_mappings_dict = {}
for category in ['dresses', 'lower_body', 'upper_body']:
    with open(os.path.join(palette_mappings_path, category, f"{category}_palette_mappings.json")) as f:
        palette_mappings_dict[category] = json.load(f)


@app.post("/analyze")
async def analyze_color_and_recommend(
    image: UploadFile = File(...),
    query: Literal["upper_body", "lower_body", "dresses"] = Form(...)
):
    try:
        # 이미지 로딩
        image_bytes = await image.read()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # 파이프라인 구성
        pl = pipeline.Pipeline()
        pl.add_filter(segmentation_filter.SegmentationFilter(segmentation_model))
        pl.add_filter(user_palette_classification_filter.UserPaletteClassificationFilter(reference_palettes))

        # 1차 실행: segmentation + 퍼스널컬러 분류
        user_palette = pl.execute(img, device)

        # 옷 추천 필터 추가 후 재실행
        rf = retrieval_filter.RetrievalFilter(cloth_dataset_path, palette_mappings_dict)
        rf.set_query(query)
        pl.add_filter(rf)

        retrieved_paths = pl.execute(img, device)

        return JSONResponse(content={
            "personal_color": user_palette.description(),
            "recommendations": retrieved_paths
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
