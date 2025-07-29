import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import torch

# 1. CSV 불러오기 및 분할
df = pd.read_csv("labeled_kakao_chat.csv")
label_map = {"Anger": 0, "Fear": 1, "Happy": 2, "Tender": 3, "Sad": 4}
df["label"] = df["emotion"].map(label_map)

train_df, val_df = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=42)
train_dataset = Dataset.from_pandas(train_df[["text", "label"]])
val_dataset = Dataset.from_pandas(val_df[["text", "label"]])

# 2. 토크나이저
tokenizer = AutoTokenizer.from_pretrained("monologg/kobert", trust_remote_code=True)

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)

train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
val_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# 3. 모델 로드
model = AutoModelForSequenceClassification.from_pretrained("rkdaldus/ko-sent5-classification", num_labels=5)

# 4. 트레이너
training_args = TrainingArguments(
    output_dir="./results",
    logging_dir="./logs",
    learning_rate=2e-5,
    eval_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=5,
    no_cuda=True,  # CPU 강제
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# 5. 훈련
trainer.train()

# 6. 저장
trainer.save_model("kobert-sent5-finetuned-yeonji")