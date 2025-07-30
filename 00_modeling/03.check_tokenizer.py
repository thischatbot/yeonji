from transformers import AutoTokenizer

tokenizer1 = AutoTokenizer.from_pretrained("monologg/kobert")
tokenizer2 = AutoTokenizer.from_pretrained("monologg/distilkobert")

sentence = "왜 안 읽어?"

print(tokenizer1.tokenize(sentence))
print(tokenizer2.tokenize(sentence))
