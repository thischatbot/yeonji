from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI()

Emotion = Literal['기쁨', '슬픔', '분노', '불안', '놀람', '평온']

# 요청 본문 모델
class EmotionRequest(BaseModel):
    user_input: str = Field(..., example="오늘 너무 힘들었어")
    detected_emotion: Emotion = Field(..., example="슬픔")
    confidence: float = Field(..., ge=0.0, le=1.0, example=0.92)

# 응답 모델
class EmotionResponse(BaseModel):
    message: str
    emotion: Emotion
    confidence: float

@app.post("/analyze", response_model=EmotionResponse)
async def analyze_emotion(data: EmotionRequest):
    if data.confidence < 0.5:
        raise HTTPException(status_code=400, detail="Confidence too low")
    
    response_message = f"당신이 느끼는 '{data.detected_emotion}' 감정에 공감해요."
    return EmotionResponse(
        message=response_message,
        emotion=data.detected_emotion,
        confidence=data.confidence
    )