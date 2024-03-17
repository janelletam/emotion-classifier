import os
import librosa
import numpy as np
import soundfile as sf

#---------------------------------------------------------------------------------------------------------
# List of the Global Labels for each emotion:
#   1 = neutral
#   2 = calm
#   3 = happy
#   4 = sad
#   5 = angry
#   6 = fearful
#   7 = disgust
#   8 = surprised
#
# All of the labels for each dataset:
#   TESS labels: ['angry' 'disgust' 'fear' 'happy' 'neutral' 'ps' 'sad']
#   CREMA labels: ['ANG' 'DIS' 'FEA' 'HAP' 'NEU' 'SAD']
#   SAVEE labels: ['a' 'd' 'f' 'h' 'n' 'sa' 'su']
#   RAVDESS labels: ['01' '02' '03' '04' '05' '06' '07' '08']
#
# All of the emotions appeared which appeared in the datasets:
#   Angry       TESS, CREMA, SAVEE, RAVDESS
#   Disgust     TESS, CREMA, SAVEE, RAVDESS
#   Fear        TESS, CREMA, SAVEE, RAVDESS
#   Happy       TESS, CREMA, SAVEE, RAVDESS
#   Neutral     TESS, CREMA, SAVEE, RAVDESS
#   Sad         TESS, CREMA, SAVEE, RAVDESS
#   Surprised   TESS, SAVEE, RAVDESS
#   Calm        RAVDESS
#
# All the information regarding the audio files in each dataset will be kept in a dictionary as followed:
# Each dictionary will contain:     1. audio's path
#                                   2. audio's dataset label
#                                   3. audio's global label
#                                   4. modified audio's path
#---------------------------------------------------------------------------------------------------------

# global labels dictionary
global_labels = {'neutral': 1, 'calm': 2, 'happy': 3, 'sad': 4, 'angry': 5, 'fearful': 6, 'disgust': 7,
                 'surprised': 8}

# global target sampling rate
target_sampling_rate = 24000

# specific label dictionaries for each dataset
TESS_labels = {'angry': 'angry', 'disgust': 'disgust', 'fear': 'fearful', 'happy': 'happy',
               'neutral': 'neutral', 'ps': 'surprised', 'sad': 'sad'}

CREMA_labels = {'ANG': 'angry', 'DIS': 'disgust', 'FEA': 'fearful', 'HAP': 'happy', 'NEU': 'neutral',
                'SAD': 'sad'}

SAVEE_labels = {'a': 'angry', 'd': 'disgust', 'f': 'fearful', 'h': 'happy', 'n': 'neutral', 'sa': 'sad',
                'su': 'surprised'}


# function to covert each dataset's local labeling to the global labels
def assign_global_labels(dataset, audio_label):

    global global_labels
    global TESS_labels
    global CREMA_labels
    global SAVEE_labels

    converted_label = 0

    # TESS labels: ['angry' 'disgust' 'fear' 'happy' 'neutral' 'ps' 'sad']
    if dataset == 'TESS':
        emotion = TESS_labels[audio_label]
        converted_label = global_labels[emotion]

    # CREMA labels: ['ANG' 'DIS' 'FEA' 'HAP' 'NEU' 'SAD']
    elif dataset == 'CREMA':
        emotion = CREMA_labels[audio_label]
        converted_label = global_labels[emotion]

    # SAVEE labels: ['a' 'd' 'f' 'h' 'n' 'sa' 'su']
    elif dataset == 'SAVEE':
        emotion = SAVEE_labels[audio_label]
        converted_label = global_labels[emotion]

    # RAVDESS labels: ['01' '02' '03' '04' '05' '06' '07' '08']
    elif dataset == 'RAVDESS': converted_label = int(audio_label)


    return converted_label

# The following are some functions to resize, normalize, and process audio files from each dataset
# into new files and creates a new directory of processed data

# function to normalize and resamples every file into a specific sample rate (sr)
def resample_and_normalize_data(file_path, target_sr):
    audio, sr = librosa.load(file_path)
    audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
    audio_normalized = (audio_resampled - np.mean(audio_resampled)) / np.std(audio_resampled)
    return audio_normalized

def preprocess_dataset(dataset, dataset_dictionary):
    # prevents re-running if the data has already been processed
    if (os.path.isdir("Data\\resampled\\{dataset}")): return
    
    for index, audio_path in enumerate(dataset_dictionary['audio path']):
        audio_resampled = resample_and_normalize_data(audio_path, target_sampling_rate)

        # Making directory to store audio files
        os.makedirs(f"Data\\resampled\\{dataset}", exist_ok=True)
        path_name = f"Data\\resampled\\{dataset}\\{dataset}_resampled_{index}_emotion_{dataset_dictionary['label'][index]}.wav"

        # Save audio output as wav file
        sf.write(path_name, audio_resampled, target_sampling_rate)
        librosa.get_samplerate(path_name)

# function to add modified audio file's path to dataset dictionaries
def add_modified_path(dataset, dataset_dictionary):
    for index, audio_path in enumerate(dataset_dictionary['audio path']):
        path_name = f"Data\\resampled\\{dataset}\\{dataset}_resampled_{index}_emotion_{dataset_dictionary['label'][index]}.wav"
        dataset_dictionary['audio resampled path'].append(path_name)
    return (dataset_dictionary)


# Now, different functions specifically for each filename format in different datasets:

# TESS labels: ['angry' 'disgust' 'fear' 'happy' 'neutral' 'ps' 'sad']
def TESS():

    dataset_path = "Data\\TESS"                     # keeps the main path of the dataset
    dataset_folders = os.listdir(dataset_path)      # lists all the folders inside the dataset

    TESS_dictionary = {'audio path': [], 'dataset label': [], 'label': [], 'audio resampled path': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for file in dataset_folders:
        file_path = os.path.join(dataset_path, file)
        audio_files = os.listdir(file_path)
        
        for audio in audio_files:
            audio_path = os.path.join(file_path, audio)
            audio_label = audio.split("_")[2][:-4]
            audio_label_global = assign_global_labels('TESS', audio_label)

            TESS_dictionary['audio path'].append(audio_path)
            TESS_dictionary['dataset label'].append(audio_label)
            TESS_dictionary['label'].append(audio_label_global)

    # preprocess all the audio files and keep the new paths
    preprocess_dataset('TESS', TESS_dictionary)
    TESS_dictionary = add_modified_path('TESS', TESS_dictionary)
    
    return TESS_dictionary


# CREMA labels: ['ANG' 'DIS' 'FEA' 'HAP' 'NEU' 'SAD']
def CREMA():
    
    dataset_path = "Data\\CREMA"                     # keeps the main path of the dataset
    audio_files = os.listdir(dataset_path)           # lists all the folders inside the dataset

    CREMA_dictionary = {'audio path': [], 'dataset label': [], 'label': [], 'audio resampled path': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for audio in audio_files:
        audio_path = os.path.join(dataset_path, audio)
        audio_label = audio.split("_")[2]
        audio_label_global = assign_global_labels('CREMA', audio_label)

        CREMA_dictionary['audio path'].append(audio_path)
        CREMA_dictionary['dataset label'].append(audio_label)
        CREMA_dictionary['label'].append(audio_label_global)

    # preprocess all the audio files and keep the new paths
    preprocess_dataset('CREMA', CREMA_dictionary)
    CREMA_dictionary = add_modified_path('CREMA', CREMA_dictionary)
        
    return CREMA_dictionary


# SAVEE labels: ['a' 'd' 'f' 'h' 'n' 'sa' 'su']
def SAVEE():
    
    dataset_path = "Data\\SAVEE"                     # keeps the main path of the dataset
    audio_files = os.listdir(dataset_path)           # lists all the folders inside the dataset

    SAVEE_dictionary = {'audio path': [], 'dataset label': [], 'label': [], 'audio resampled path': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for audio in audio_files:
        audio_path = os.path.join(dataset_path, audio)
        audio_label = audio.split("_")[1][:-6]
        audio_label_global = assign_global_labels('SAVEE', audio_label)

        SAVEE_dictionary['audio path'].append(audio_path)
        SAVEE_dictionary['dataset label'].append(audio_label)
        SAVEE_dictionary['label'].append(audio_label_global)

    # preprocess all the audio files and keep the new paths
    preprocess_dataset('SAVEE', SAVEE_dictionary)
    SAVEE_dictionary = add_modified_path('SAVEE', SAVEE_dictionary)
    
    return SAVEE_dictionary


# RAVDESS labels:
#
#   01 = neutral
#   02 = calm
#   03 = happy
#   04 = sad
#   05 = angry
#   06 = fearful
#   07 = disgust
#   08 = surprised
#
# RAVDESS labels: ['01' '02' '03' '04' '05' '06' '07' '08']
def RAVDESS():

    dataset_path = "Data\\RAVDESS"                  # keeps the main path of the dataset
    dataset_folders = os.listdir(dataset_path)      # lists all the folders inside the dataset

    RAVDESS_dictionary = {'audio path': [], 'dataset label': [], 'label': [], 'audio resampled path': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for file in dataset_folders:
        file_path = os.path.join(dataset_path, file)
        audio_files = os.listdir(file_path)
        
        for audio in audio_files:
            audio_path = os.path.join(file_path, audio)
            audio_label = (audio.split("-"))[2]
            audio_label_global = assign_global_labels('RAVDESS', audio_label)

            RAVDESS_dictionary['audio path'].append(audio_path)
            RAVDESS_dictionary['dataset label'].append(audio_label)
            RAVDESS_dictionary['label'].append(audio_label_global)

    # preprocess all the audio files and keep the new paths
    preprocess_dataset('RAVDESS', RAVDESS_dictionary)
    RAVDESS_dictionary = add_modified_path('RAVDESS', RAVDESS_dictionary)

    return RAVDESS_dictionary