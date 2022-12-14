import os
import math

DATA_DIR = "./data"
MODEL_DIR = "./models"

DATA_OPTION = "mfcc"

JSON_PATH = os.path.join(DATA_DIR, DATA_OPTION + ".json")

NUM_GENRES = 10

SAMPLE_RATE = 22050
DURATION = 25
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION
HOP_LENGTH = 512
N_FFT = 2048

NUM_SEGMENTS = 10
NUM_SAMPLES_PER_SEGMENT = int(SAMPLES_PER_TRACK / NUM_SEGMENTS)
EXPECTED_SEGMENT_LENGTH = math.ceil(NUM_SAMPLES_PER_SEGMENT / HOP_LENGTH)

N_MFCC = 13

N_MELS = 128
