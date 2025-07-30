import pandas as pd
from sklearn.utils import resample

# 1. CSV 파일 불러오기
df = pd.read_csv("labeled_kakao_chat.csv")

# 2. 감정 라벨 분포 확인
print("💡라벨 분포 (원본)")
print(df["emotion"].value_counts())

# 3. 가장 적은 클래스 수를 기준으로 맞춤
min_count = df["emotion"].value_counts().min()

# 4. 클래스별 under-sampling
balanced_df = pd.concat([
    resample(df[df["emotion"] == label],
             replace=False,
             n_samples=min_count,
             random_state=42)
             for label in df["emotion"].unique()
             ], ignore_index=True)

# 5. 결과 확인
print("\n✅ 라벨 분포 (균형 조정 후)")
print(balanced_df["emotion"].value_counts())

# 6. 저장
balanced_df.to_csv("balanced_kakao_chat.csv", index=False)
print("\n📁 저장 완료: balanced_kakao_chat.csv")