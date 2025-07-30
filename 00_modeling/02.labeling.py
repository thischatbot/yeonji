import pandas as pd

# 감정 키워드 사전 정의
emotion_keywords = {
    "Anger": ["개쓰레기야", "그만해", "너무한 거 아니야?", "그만하자", "왜 그래", "이렇게까지"],
    "Fear": ["죽고싶어", "무너지는", "차단했어", "초라해", "이상해져", "불안해", "싫어", "고통스러워", "괴로워"],
    "Sad": ["무시당하니까", "힘들어", "너무하네", "제발", "피곤하다", "말이라도 해줘", "한마디만", "답장", "사랑받고"]
}

def label_emotion(text):
    for emotion, keywords in emotion_keywords.items():
        if any(word in text for word in keywords):
            return emotion
    return "Tender" #"기타"

# 데이터 로드
df = pd.read_csv("kakao_chat.csv")

# 보이스톡 관련 메시지 제거
df = df.drop(df[df["text"].str.contains("해요\\)")].index)
df = df.drop(df[df["text"].str.contains("응답없음\\)")].index)
df = df.drop(df[df["text"].str.contains("\\(보이스톡")].index)

# 유사 문장 확인
print(df["text"].duplicated().sum())

# 유사 문장 제거
df = df.drop_duplicates(subset=['text'], keep='first')

# 라벨링 적용
df["emotion"] = df["text"].apply(label_emotion)

# 확인
print(df["emotion"].value_counts())
df.to_csv("labeled_kakao_chat.csv", index=False)

