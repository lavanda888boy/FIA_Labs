import torch
from torch_training import MAX_LEN, INPUT_DIM, OUTPUT_DIM, EMBED_DIM, HIDDEN_DIM, NUM_LAYERS, Tokenizer, Encoder, Decoder, Seq2Seq
import telebot
import os
from dotenv import load_dotenv


device = torch.device("cpu")

tokenizer = torch.load('./models/moldova_tokenizer.pth', weights_only=False)

encoder = Encoder(INPUT_DIM, EMBED_DIM, HIDDEN_DIM, NUM_LAYERS).to(device)
decoder = Decoder(OUTPUT_DIM, EMBED_DIM, HIDDEN_DIM, NUM_LAYERS).to(device)
model = Seq2Seq(encoder, decoder, device).to(device)

model.load_state_dict(torch.load(
    './models/moldova_seq2seq_torch.pth', weights_only=True))


def prepare_answer(model, question, tokenizer):
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


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Welcome to this chatbot!\n\n"
        "You can ask any question about Moldova and in particular its capital - Chisinau!\n\n"
        "For example, you can ask:\n"
        "- What is the climate in Moldova?\n"
        "- Where can I watch movies in Chisinau?")


@bot.message_handler(func=lambda message: message.text is not None and len(message.text) > 5 and '/' not in message.text)
def send_answer(message):
    answer = prepare_answer(model, message.text, tokenizer)
    bot.reply_to(message, answer)


bot.infinity_polling()
