import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

IMAGE_LABELS = 'labels.csv'

data = pd.read_csv('labels.csv')
data['Label'] = data['Label'].astype(str)

train_data, temp_data = train_test_split(
    data, test_size=0.35, random_state=42, shuffle=True)
validation_data, test_data = train_test_split(
    temp_data, test_size=15/35, random_state=42, shuffle=True)

train_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255).flow_from_dataframe(
        dataframe=train_data,
        directory='./images',
        x_col="ImageName",
        y_col="Label",
        target_size=(128, 128),
        class_mode="binary",
        batch_size=32,
        shuffle=True,
        width_shift_range=0.3,
        height_shift_range=0.3,
        zoom_range=0.3,
)

validation_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255).flow_from_dataframe(
        dataframe=validation_data,
        directory='./images',
        x_col="ImageName",
        y_col="Label",
        target_size=(128, 128),
        class_mode="binary",
        batch_size=32,
        shuffle=True,
        width_shift_range=0.3,
        height_shift_range=0.3,
        zoom_range=0.3,
)

test_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255).flow_from_dataframe(
        dataframe=test_data,
        directory='./images',
        x_col="ImageName",
        y_col="Label",
        target_size=(128, 128),
        class_mode="binary",
        batch_size=32,
        shuffle=True
)

model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(128, 128, 3)),
    tf.keras.layers.Conv2D(32, (5, 5), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(48, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (2, 2), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu',
                          kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

history = model.fit(
    train_data_generator,
    validation_data=validation_data_generator,
    epochs=50,
    callbacks=[early_stopping],
)

print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
