import librosa
import numpy as np
import keras as keras

from config import (
    DURATION,
    NUM_SEGMENTS,
    NUM_SAMPLES_PER_SEGMENT,
    EXPECTED_SEGMENT_LENGTH,
    DATA_OPTION,
    N_MFCC,
    N_FFT,
    HOP_LENGTH,
    N_MELS,
    SAMPLE_RATE,
)

SAVED_MODEL = "D:/Projects/DPS Project/musicproject/model.h5"


def process_file(
    file_path,
    num_segments=NUM_SEGMENTS,
    num_samples_per_segment=NUM_SAMPLES_PER_SEGMENT,
    option=DATA_OPTION,
    n_mfcc=N_MFCC,
    n_fft=N_FFT,
    hop_length=HOP_LENGTH,
    n_mels=N_MELS,
    fmax=SAMPLE_RATE // 2,
    duration=DURATION,
):

    waveform, _ = librosa.load(file_path, duration=duration)

    feature_list = []

    for s in range(num_segments):
        start_sample = num_samples_per_segment * s
        end_sample = start_sample + num_samples_per_segment

        if option == "mfcc":
            mfcc = librosa.feature.mfcc(
                waveform[start_sample:end_sample],
                n_mfcc=n_mfcc,
                n_fft=n_fft,
                hop_length=hop_length,
            )

            feature_to_export = mfcc.T

        elif option == "melspectrogram":
            melspec = librosa.feature.melspectrogram(
                waveform[start_sample:end_sample],
                n_mels=n_mels,
                n_fft=n_fft,
                hop_length=hop_length,
                fmax=fmax,
            )
            feature_to_export = melspec.T

        else:
            raise ValueError("option needs to be either melspectrogram or mfcc.")

        if (len(feature_to_export) == EXPECTED_SEGMENT_LENGTH) and np.any(
            feature_to_export
        ):
            feature_list.append(feature_to_export.tolist())

    return feature_list


class _Genre_Recognition_Service:

    model = None
    _instance = None

    _mappings = [
        "pop",
        "metal",
        "disco",
        "blues",
        "reggae",
        "classical",
        "rock",
        "hiphop",
        "country",
        "jazz",
    ]

    def predict(self, file_path):

        mfcc = self.preprocess(file_path)
        mfcc = mfcc[..., np.newaxis]
        prediction_indices = np.argmax(self.model.predict(mfcc), axis=1)
        prediction_idx = int(np.bincount(prediction_indices).argmax())
        prediction = self._mappings[prediction_idx]

        return prediction

    def preprocess(self, file_path):
        mfcc = np.array(process_file(file_path))

        return mfcc


def Genre_Recognition_Service():

    if _Genre_Recognition_Service._instance is None:
        _Genre_Recognition_Service._instance = _Genre_Recognition_Service()
        _Genre_Recognition_Service.model = keras.models.load_model(SAVED_MODEL)

    return _Genre_Recognition_Service._instance


if __name__ == "__main__":

    grs = Genre_Recognition_Service()

    genre_1 = grs.predict("./data/jazz/jazz.00001.wav")
    genre_2 = grs.predict("./data/rock/rock.00001.wav")

    print(f"Predicted Genres: {genre_1}, {genre_2}")
