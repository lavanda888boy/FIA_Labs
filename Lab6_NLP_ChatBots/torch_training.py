import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
from sklearn.model_selection import train_test_split


INPUT_DIM = 700
OUTPUT_DIM = 700
HIDDEN_DIM = 256
EMBED_DIM = 64
NUM_LAYERS = 1
LEARNING_RATE = 0.001
EPOCHS = 180
BATCH_SIZE = 32
MAX_LEN = 20


class Tokenizer:
    def __init__(self):
        self.word2idx = {"<PAD>": 0, "<SOS>": 1, "<EOS>": 2, "<UNK>": 3}
        self.idx2word = {0: "<PAD>", 1: "<SOS>", 2: "<EOS>", 3: "<UNK>"}

    def fit(self, sentences):
        unique_words = set()
        for sentence in sentences:
            unique_words.update(sentence.split())

        for word in unique_words:
            idx = len(self.word2idx)
            self.word2idx[word] = idx
            self.idx2word[idx] = word

    def encode(self, sentence):
        return [self.word2idx.get(word, self.word2idx["<UNK>"]) for word in sentence.split()]

    def decode(self, indices):
        return " ".join([self.idx2word[idx] for idx in indices if idx not in [0, 1, 2]])


class ChatDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        question = self.data.iloc[idx]["Question"]
        answer = self.data.iloc[idx]["Answer"]

        src = torch.tensor([1] + self.tokenizer.encode(question) + [2])
        trg = torch.tensor([1] + self.tokenizer.encode(answer) + [2])

        return src, trg


class Encoder(nn.Module):

    def __init__(self, input_dim, embed_dim, hidden_dim, num_layers):
        super(Encoder, self).__init__()
        self.embedding = nn.Embedding(input_dim, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim,
                            num_layers, batch_first=True)

    def forward(self, x):
        embedded = self.embedding(x)
        _, (hidden, cell) = self.lstm(embedded)
        return hidden, cell


class Decoder(nn.Module):

    def __init__(self, output_dim, embed_dim, hidden_dim, num_layers):
        super(Decoder, self).__init__()
        self.embedding = nn.Embedding(output_dim, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim,
                            num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, hidden, cell):
        x = x.unsqueeze(1)
        embedded = self.embedding(x)
        output, (hidden, cell) = self.lstm(embedded, (hidden, cell))
        prediction = self.fc(output.squeeze(1))
        return prediction, hidden, cell


class Seq2Seq(nn.Module):

    def __init__(self, encoder, decoder, device):
        super(Seq2Seq, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.device = device

    def forward(self, src, trg, teacher_forcing_ratio=0.5):
        batch_size = trg.shape[0]
        trg_len = trg.shape[1]
        trg_vocab_size = self.decoder.fc.out_features
        outputs = torch.zeros(batch_size, trg_len,
                              trg_vocab_size).to(self.device)

        hidden, cell = self.encoder(src)
        input = trg[:, 0]

        for t in range(1, trg_len):
            output, hidden, cell = self.decoder(input, hidden, cell)
            outputs[:, t] = output
            teacher_force = torch.rand(1).item() < teacher_forcing_ratio
            input = trg[:, t] if teacher_force else output.argmax(1)

        return outputs


device = torch.device("cpu")

data = pd.read_csv("dataset.csv")
train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

tokenizer = Tokenizer()
tokenizer.fit(data["Question"].tolist() + data["Answer"].tolist())

train_dataset = ChatDataset(train_data, tokenizer)
val_dataset = ChatDataset(val_data, tokenizer)


def prepare_batch(batch):
    src_batch, trg_batch = zip(*batch)

    src_batch = pad_sequence(src_batch, batch_first=True, padding_value=0)
    trg_batch = pad_sequence(trg_batch, batch_first=True, padding_value=0)

    return src_batch, trg_batch


train_loader = DataLoader(
    train_dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=prepare_batch)
val_loader = DataLoader(
    val_dataset, batch_size=BATCH_SIZE, collate_fn=prepare_batch)

encoder = Encoder(INPUT_DIM, EMBED_DIM, HIDDEN_DIM, NUM_LAYERS).to(device)
decoder = Decoder(OUTPUT_DIM, EMBED_DIM, HIDDEN_DIM, NUM_LAYERS).to(device)
model = Seq2Seq(encoder, decoder, device).to(device)

criterion = nn.CrossEntropyLoss(ignore_index=0)
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)


def train_model(model, train_loader, val_loader, criterion, optimizer):
    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0

        for src, trg in train_loader:
            src, trg = src.to(device), trg.to(device)

            optimizer.zero_grad()
            output = model(src, trg)
            output = output[:, 1:].reshape(-1, OUTPUT_DIM)

            trg = trg[:, 1:].reshape(-1)
            loss = criterion(output, trg)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        model.eval()
        val_loss = 0

        with torch.no_grad():
            for src, trg in val_loader:
                src, trg = src.to(device), trg.to(device)

                output = model(src, trg)
                output = output[:, 1:].reshape(-1, OUTPUT_DIM)
                trg = trg[:, 1:].reshape(-1)

                val_loss += criterion(output, trg).item()

        print(f"Epoch {epoch+1}/{EPOCHS}, Train Loss: {train_loss /
              len(train_loader):.4f}, Val Loss: {val_loss/len(val_loader):.4f}")


if __name__ == "__main__":
    train_model(model, train_loader, val_loader, criterion, optimizer)
    torch.save(model.state_dict(), './models/moldova_seq2seq_torch.pth')
    torch.save(tokenizer, './models/moldova_tokenizer.pth')
