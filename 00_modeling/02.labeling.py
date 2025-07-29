import pandas as pd

# 감정 키워드 사전 정의
emotion_keywords = {
    "Anger": ["개쓰레기", "너무하네", "여자 만나", "이렇게까지", "왜 그런말", "진짜 너무하네"],
    "Fear": ["불안", "제발", "버려", "무너지는", "혼자서", "답장", "싫어", "어?..."],
    "Sad": ["죽고싶어", "초라해", "이상해져", "사랑받고", "힘들어", "피곤하다"]
}

def label_emotion(text):
    for emotion, keywords in emotion_keywords.items():
        if any(word in text for word in keywords):
            return emotion
    return "Tender" #"기타"

# 데이터 로드
df = pd.read_csv("kakao_chat.csv")

# 라벨링 적용
df["emotion"] = df["text"].apply(label_emotion)

# 확인
print(df["emotion"].value_counts())
df.to_csv("labeled_kakao_chat.csv", index=False)