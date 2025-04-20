from transformers import  BertForSequenceClassification, get_linear_schedule_with_warmup , BertTokenizer 
from torch.optim import AdamW
import torch

model_path = r"F:\Projects\Updated_Real_Time_News\Saperate\f_model\classification_bert_8_classes_initial_ep_equ_data.pth"
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

checkpoint = torch.load(model_path, map_location=torch.device('cpu'))

model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=8)
model.load_state_dict(checkpoint['model_state_dict'])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device) 

def classify_review(title , description, model, tokenizer, device, max_length=128):
    model.eval()

    title = "[CLS] " + title + " [SEP]"
    description = "[CLS] " + description + " [SEP]"

    combined_text = title 

    encoded_inputs = tokenizer(combined_text, add_special_tokens=True, max_length=max_length, truncation=True, padding='max_length', return_tensors="pt")

    input_ids = encoded_inputs["input_ids"].to(device)
    attention_mask = encoded_inputs["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits

    predicted_label = torch.argmax(logits, dim=-1).item()

    classes = [
        "BUSINESS", "WORLD", "SPORTS", "SCI/TECH", "POLITICS", 
        "ENTERTAINMENT", "ARTS & CULTURE" , "GENERAL"
    ]

    return classes[predicted_label]

# test_inputs = [
#     {
#         "title": "Tech Giant Merges With Startup",
#         "description": "In a surprising move, a leading tech company announced a merger with an innovative software startup.",
#         "expected_class": "BUSINESS"
#     },
#     {
#         "title": "Global Leaders Gather for Climate Summit",
#         "description": "Delegates from dozens of countries convened in Paris to discuss strategies for tackling climate change.",
#         "expected_class": "WORLD"
#     },
#     {
#         "title": "Local Team Clinches Championship",
#         "description": "In a thrilling finale, the city's basketball team secured the championship with a last-second shot.",
#         "expected_class": "SPORTS"
#     },
#     {
#         "title": "New AI Algorithm Shatters Performance Records",
#         "description": "Researchers have developed a breakthrough AI algorithm that significantly outperforms current benchmarks.",
#         "expected_class": "SCI/TECH"
#     },
#     {
#         "title": "Government Announces Sweeping Policy Reforms",
#         "description": "A series of new policies have been introduced aimed at overhauling the healthcare and education sectors.",
#         "expected_class": "POLITICS"
#     },
#     {
#         "title": "Blockbuster Movie Breaks Box Office Records",
#         "description": "The latest summer blockbuster has smashed box office records, drawing massive audiences to theaters.",
#         "expected_class": "ENTERTAINMENT"
#     },
#     {
#         "title": "Renowned Painter's Exhibition Opens to Rave Reviews",
#         "description": "A celebrated painter's exhibition is drawing art lovers from around the world with its blend of classic and modern styles.",
#         "expected_class": "ARTS & CULTURE"
#     },
#     {
#         "title": "Community Fair Brings Neighbors Together",
#         "description": "A local fair provided a platform for community members to gather, celebrate, and enjoy various cultural festivities.",
#         "expected_class": "GENERAL"
#     },
# ]

# for idx, sample in enumerate(test_inputs):
#         title = sample["title"]
#         description = sample["description"]
#         expected = sample["expected_class"]

#         predicted_class = classify_review(title, description, model, tokenizer, device)
        
#         print(f"Test Sample {idx+1}:")
#         print("  Title            :", title)
#         print("  Description      :", description)
#         print("  Expected Class   :", expected)
#         print("  Predicted Class  :", predicted_class)
#         print("-" * 60)