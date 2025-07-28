from dataclasses import dataclass
from typing import Literal, Optional
from pydantic import BaseModel, Field, ValidationError

# --- 1. 감정 유형 정의: Literal을 활용한 명확한 타입 지정 ---
# 'Emotion' 타입은 사전에 정의된 특정 문자열 값('기쁨', '슬픔' 등)만 가질 수 있도록 제한합니다.
# 이는 감정 분류 결과가 예상치 못한 값으로 들어오는 것을 방지하여 데이터의 일관성을 유지합니다.
Emotion = Literal['기쁨', '슬픔', '분노', '불안', '놀람', '평온']

# --- 2. dataclass로 대화 데이터 정의: 간결하고 읽기 쉬운 데이터 구조 ---
# @dataclass 데코레이터를 사용하여 'DialogueLog' 클래스를  데이터 저장용으로 만듭니다.
# 이는 데이터를 묶어두는 간단한 컨테이너 역할을 하며, 별도의 __init__ 메서드 없이도 객체 생성이 용이합니다.
@dataclass
class DialogueLog:
    user_input: str # 사용자의 원본 발화 내용을 문자열로 저장
    detected_emotion: Emotion # 감정 분석 모델이 감지한 감정 (위에서 정의한 Emotion 타입)
    confidence: float # 감정 분석 결과에 대한 모델의 확신도 (0.0 ~ 1.0 사이의 실수)

# --- 3. pydantic으로 유효성 검증 클래스 정의: 강력한 데이터 검증과 변환 ---
# 'BaseModel'을 상속받아 'EmotionResult' 클래스를 정의합니다.
# pydantic을 데이터가 이 모델의 스키마를 따르는지 자동으로 검증해줍니다.
class EmotionResult(BaseModel):
    user_input : str
    detected_emotion: Emotion # Emotion 타입을 사용하여 유효한 감정만 받도록 합니다.
    # 'confidence' 필드는 기본값 없이 필수이며(ellipsis, ...) 0.0 이상 1.0 이하의 값을 가져야 합니다.
    # 'Field' 함수는 이렇게 세밀한 유효성 검증 규칙을 정의할 때 사용됩니다.
    confidence: float = Field(..., ge=0.0, le=1.0) # ge= greater than or equal, le = less than or equal

# --- 4. 예시 데이터 생성 및 유효성 검증 실행 ---
print("--- 유효한 데이터 예시 ---")
try:
    # 모든 조건에 부합하는 유효한 EmotionResult 객체 생성
    valid_result = EmotionResult(
        user_input="오늘 너무 힘들었어",
        detected_emotion="슬픔",
        confidence=0.92
    )
    # .dict() 메서드를 사용하여 객체를 딕셔너리 형태로 변환 (직렬화)
    print("유효한 감정 분석 결과:", valid_result.dict())
except ValidationError as e:
    # 유효성 검증 실패 시 발생하는 ValidationError를 잡아서 JSON 형태로 출력
    print("유효성 검증 오류 (유효한 데이터):", e.json())

print("\n--- 유효하지 않은 데이터 예시 (confidence 범위 초과) ---")
try:
    # confidence 값이 1.5로 1.0을 초과하여 유효성 검증 실패 예정
    invalid_confidence_result = EmotionResult(
        user_input="기분이 정말 좋지 않아",
        detected_emotion="분노",
        confidence=1.5
    )
    print("유효하지 않은 감정 분석 결과:", invalid_confidence_result.dict())
except ValidationError as e:
    print("유효성 검증 오류 (confidence 범위 초과):", e.json())

print("\n--- 유효하지 않은 데이터 예시 (정의되지 않은 감정) ---")
try:
    # detected_emotion이 Emotion 타입에 정의되지 않은 '행복'이므로 유효성 검증 실패 예정
    invalid_emotion_result = EmotionResult(
        user_input="완전 행복해!",
        detected_emotion="행복", # Emotion Literal에 없는 값
        confidence=0.99
    )
    print("유효하지 않은 감정 분석 결과:", invalid_emotion_result.dict())
except ValidationError as e:
    print("유효성 검증 오류 (정의되지 않은 감정):", e.json())