import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import BertTokenizer, BertForSequenceClassification
from tqdm import tqdm

# 1. CSV 불러오기 및 분할
df = pd.read_csv("labeled_kakao_chat.csv")
label_map = {"Anger": 0, "Fear": 1, "Happy": 2, "Tender": 3, "Sad": 4}
df["label"] = df["emotion"].map(label_map)

from sklearn.model_selection import train_test_split

train_df, val_df = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=42)

# 2. 토크나이저 및 데이터셋 구성
tokenizer = BertTokenizer.from_pretrained("monologg/kobert", trust_remote_code=True, max_length=64)

class EmotionDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_len=32):
        self.data = dataframe
        self.tokenizer = tokenizer
        self.max_len = max_len
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        inputs = self.tokenizer(
            row["text"],
            max_length=self.max_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        return {
            "input_ids": inputs["input_ids"].squeeze(0),
            "attention_mask": inputs["attention_mask"].squeeze(0),
            "labels": torch.tensor(row["label"], dtype=torch.long)
        }
        
train_dataset = EmotionDataset(train_df, tokenizer)
val_dataset = EmotionDataset(val_df, tokenizer)

train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=1, shuffle=True)

# 3. 모델 로드
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained("rkdaldus/ko-sent5-classification", num_labels=5)
model.to(device)

# 4. 옵티마이저
optimizer = AdamW(model.parameters(), lr=2e-5)

# 5. 훈련 루프
def train_one_epoch():
    model.train()
    total_loss = 0
    for batch in tqdm(train_loader):
        batch = {k: v.to(device) for k, v in batch.items()}
        
        outputs = model(**batch)
        loss = outputs.loss
        total_loss += loss.item()
        
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    return total_loss / len(train_loader)

def evaluate():
    model.eval()
    total = 0
    correct = 0
    with torch.no_grad():
        for batch in val_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            preds = torch.argmax(outputs.logits, dim=1)
            correct += (preds == batch["labels"]).sum().item()
            total += batch["labels"].size(0)
        return correct / total

# 6. 에폭 루프
for epoch in range(3):
    print(f"Epoch {epoch+1}")
    train_loss = train_one_epoch()
    acc = evaluate()
    print(f"Train loss: {train_loss: .4f} | Val accuracy: {acc:.4f}")

# 7. 저장
model.save_pretrained("kobert-sent5-finetuned-yeonji")
tokenizer.save_pretrained("kobert-sent5-finetuned-yeonji")