import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import numpy as np
from tqdm import tqdm 
import os
import gc

# Optional: Set seeds for reproducibility
def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    
set_seed()

# Check available GPU
if torch.cuda.is_available():
    print(f"GPU available: {torch.cuda.get_device_name(0)}")
    print(f"Memory allocated: {torch.cuda.memory_allocated(0)/1e9:.2f} GB")

# Define our dataset class (same as before)
class YouTubeTitleDataset(Dataset):
    def __init__(self, titles, labels, tokenizer, max_length=128):
        self.titles = titles
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.titles)
    
    def __getitem__(self, idx):
        title = str(self.titles[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer.encode_plus(
            title,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# Load the dataset and take a small subset
df = pd.read_csv('youtube_titles_dataset.csv')

# Split the data
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['title'].values, 
    df['is_informative'].values, 
    test_size=0.2, 
    random_state=42
)

# Initialize tokenizer and model
tokenizer = BertTokenizer.from_pretrained('prajjwal1/bert-tiny')
model = BertForSequenceClassification.from_pretrained(
    'prajjwal1/bert-tiny',
    num_labels=2
)

# Create datasets
train_dataset = YouTubeTitleDataset(train_texts, train_labels, tokenizer)
val_dataset = YouTubeTitleDataset(val_texts, val_labels, tokenizer)

# Create dataloaders
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8)

# Training setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")
model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

# Enhanced training loop with validation and progress bar
def train_model(model, train_loader, val_loader, epochs=100):
    best_accuracy = 0
    
    for epoch in range(epochs):
        # Training phase
        model.train()
        train_loss = 0
        correct = 0
        total = 0
        
        # Add progress bar
        progress_bar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{epochs}')
        
        for batch in progress_bar:
            optimizer.zero_grad()
            
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            predictions = torch.argmax(outputs.logits, dim=1)
            correct += (predictions == labels).sum().item()
            total += labels.size(0)
            
            # Update progress bar
            progress_bar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'accuracy': f'{correct/total:.4f}'
            })
        
        # Calculate training metrics
        avg_train_loss = train_loss / len(train_loader)
        train_accuracy = correct / total
        
        # Add early stopping check
        if train_accuracy > best_accuracy:
            best_accuracy = train_accuracy
            # Save best model
            torch.save(model.state_dict(), 'best_model.pt')
            
        # Add GPU memory management
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        print(f"Epoch {epoch+1}")
        print(f"Training Loss: {avg_train_loss:.4f}")
        print(f"Training Accuracy: {train_accuracy:.4f}")
        print("-" * 30)

# Function to predict on new titles
def predict_title(title, model, tokenizer):
    model.eval()
    encoding = tokenizer.encode_plus(
        title,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )
    
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        prediction = torch.argmax(outputs.logits, dim=1)
    
    return "Informative" if prediction.item() == 1 else "Entertainment"

# Train the model
train_model(model, train_loader, val_loader)

# Test some examples from our dataset
test_titles = df['title'].values[:5]  # Test first 5 titles
for title in test_titles:
    result = predict_title(title, model, tokenizer)
    print(f"Title: '{title}'")
    print(f"Prediction: {result}")
    print("-" * 50)
    
# Make all model parameters contiguous before saving
for param in model.parameters():
    param.data = param.data.contiguous()

# Now save the model and tokenizer
model_save_path = 'extension_model'
tokenizer.save_pretrained(model_save_path)
model.save_pretrained(model_save_path)