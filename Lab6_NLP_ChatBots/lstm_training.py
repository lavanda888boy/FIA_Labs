import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

data = pd.read_csv('questions.csv')

questions = data["Question"].values
answers = data["Answer"].values

tokenizer = tf.keras.preprocessing.text.Tokenizer()

bos_token = "bos"
eos_token = "eos"
questions = [f"{bos_token} {q} {eos_token}" for q in questions]
answers = [f"{bos_token} {a} {eos_token}" for a in answers]

tokenizer.fit_on_texts(questions + answers)

questions_seq = tokenizer.texts_to_sequences(questions)
answers_seq = tokenizer.texts_to_sequences(answers)

question_lengths = [len(seq) for seq in questions_seq]
answer_lengths = [len(seq) for seq in answers_seq]

max_sentence_len = max(max(question_lengths), max(answer_lengths))

questions_padded = tf.keras.preprocessing.sequence.pad_sequences(
    questions_seq, maxlen=max_sentence_len, padding='post', truncating='post')
answers_padded = tf.keras.preprocessing.sequence.pad_sequences(
    answers_seq, maxlen=max_sentence_len, padding='post', truncating='post')

vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 256
latent_dim = 256

encoder_input = tf.keras.layers.Input(shape=(max_sentence_len,))
encoder_embedding = tf.keras.layers.Embedding(
    input_dim=vocab_size, output_dim=embedding_dim, embeddings_regularizer=tf.keras.regularizers.l2(0.01))(encoder_input)
encoder_lstm = tf.keras.layers.LSTM(latent_dim, dropout=0.3, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)
encoder_states = [state_h, state_c]

decoder_input = tf.keras.layers.Input(shape=(max_sentence_len,))
decoder_embedding = tf.keras.layers.Embedding(
    input_dim=vocab_size, output_dim=embedding_dim, embeddings_regularizer=tf.keras.regularizers.l2(0.01))(decoder_input)
decoder_lstm = tf.keras.layers.LSTM(
    latent_dim, dropout=0.3, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(
    decoder_embedding, initial_state=encoder_states)

output = tf.keras.layers.Dense(
    vocab_size, activation='softmax')(decoder_outputs)
model = tf.keras.models.Model([encoder_input, decoder_input], output)

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy', metrics=['accuracy'])

X_train, X_val, y_train, y_val = train_test_split(
    questions_padded, answers_padded, test_size=0.3, random_state=42)

history = model.fit(
    [X_train, y_train],
    y_train,
    batch_size=64,
    epochs=500,
    validation_data=([X_val, y_val], y_val),
    verbose=1
)

print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")

model.save('./models/moldova_seq2seq.keras')
