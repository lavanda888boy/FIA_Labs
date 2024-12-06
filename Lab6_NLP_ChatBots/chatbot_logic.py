import torch
import pandas as pd
from sklearn.model_selection import train_test_split
from torch_training import MAX_LEN, INPUT_DIM, OUTPUT_DIM, EMBED_DIM, HIDDEN_DIM, NUM_LAYERS, Encoder, Decoder, Seq2Seq


device = torch.device("cpu")

data = pd.read_csv("dataset.csv")
train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

tokenizer = torch.load('./models/moldova_tokenizer.pth', weights_only=False)

encoder = Encoder(INPUT_DIM, EMBED_DIM, HIDDEN_DIM, NUM_LAYERS).to(device)
decoder = Decoder(OUTPUT_DIM, EMBED_DIM, HIDDEN_DIM, NUM_LAYERS).to(device)
model = Seq2Seq(encoder, decoder, device).to(device)

model.load_state_dict(torch.load(
    './models/moldova_seq2seq_torch.pth', weights_only=True))


def answer_the_question(model, question, tokenizer):
    model.eval()

    src = torch.tensor([1] + tokenizer.encode(question) +
                       [2]).unsqueeze(0).to(device)
    hidden, cell = model.encoder(src)
    input_token = torch.tensor([1]).to(device)

    result = []

    for _ in range(MAX_LEN):
        output, hidden, cell = model.decoder(input_token, hidden, cell)
        pred_token = output.argmax(1).item()

        if pred_token == 2:
            break

        result.append(pred_token)
        input_token = torch.tensor([pred_token]).to(device)

    return tokenizer.decode(result)


print(answer_the_question(model, "Which malls are in Chisinau?", tokenizer))
