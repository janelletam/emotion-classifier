import os
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pickle

#---------------------------------------------------------------------------------------------------------
# List of the Global Labels for each emotion:
#   0 = neutral
#   1 = calm
#   2 = happy
#   3 = sad
#   4 = angry
#   5 = fearful
#   6 = disgust
#   7 = surprised
#
# All of the labels for each dataset:
#   TESS labels: ['angry' 'disgust' 'fear' 'happy' 'neutral' 'ps' 'sad']
#   CREMA labels: ['ANG' 'DIS' 'FEA' 'HAP' 'NEU' 'SAD']
#   SAVEE labels: ['a' 'd' 'f' 'h' 'n' 'sa' 'su']
#   RAVDESS labels: ['01' '02' '03' '04' '05' '06' '07' '08']
#   EMOdb labels (German): ['W' 'L' 'E' 'A' 'F' 'T' 'N']
#
# All of the emotions appeared which appeared in the datasets:
#   Angry       TESS, CREMA, SAVEE, RAVDESS
#   Disgust     TESS, CREMA, SAVEE, RAVDESS
#   Fear        TESS, CREMA, SAVEE, RAVDESS, EMOdb
#   Happy       TESS, CREMA, SAVEE, RAVDESS, EMOdb
#   Neutral     TESS, CREMA, SAVEE, RAVDESS, EMOdb
#   Sad         TESS, CREMA, SAVEE, RAVDESS, EMOdb
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
global_labels = {'neutral': 0, 'happy': 1, 'sad': 2, 'angry': 3, 'fearful': 4, 'disgust': 5,
                 'surprised': 6}

# global target sampling rate
target_sampling_rate = 24000

# specific label dictionaries for each dataset
TESS_labels = {
    'angry': 'angry',
    'disgust': 'disgust',
    'fear': 'fearful',
    'happy': 'happy',
    'neutral': 'neutral',
    'ps': 'surprised',
    'sad': 'sad'
}

CREMA_labels = {
    'ANG': 'angry',
    'DIS': 'disgust',
    'FEA': 'fearful',
    'HAP': 'happy',
    'NEU': 'neutral',
    'SAD': 'sad'
}

SAVEE_labels = {
    'a': 'angry',
    'd': 'disgust',
    'f': 'fearful',
    'h': 'happy',
    'n': 'neutral',
    'sa': 'sad',
    'su': 'surprised'
}

RAVDESS_labels = {
    '01': 'neutral',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

EMOdb_labels = {
    'A': 'fearful',
    'F': 'happy',
    'T': 'sad',
    'N': 'neutral'
}

# function to covert each dataset's local labeling to the global labels
def assign_global_labels(dataset, audio_label):

    global global_labels
    global TESS_labels
    global CREMA_labels
    global SAVEE_labels
    global EMOdb_labels

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

    # RAVDESS labels: ['01' '03' '04' '05' '06' '07' '08']
    elif dataset == 'RAVDESS':
        emotion = RAVDESS_labels[audio_label]
        converted_label = global_labels[emotion]

    # EMOdb labels: ['A' 'F' 'T' 'N']
    elif dataset == 'EMOdb':
        emotion = EMOdb_labels[audio_label]
        converted_label = global_labels[emotion]

    return converted_label

# convert global labels to their respective comprehensible word form label
def convert_label(label):
    global global_labels
    return (list(global_labels.keys())[list(global_labels.values()).index(label)])

# The following are some functions to resize, normalize, and process audio files from each dataset
# into new files and creates a new directory of processed data

# function to normalize and resamples every file into a specific sample rate (sr)
def resample_data(file_path, target_sr):
    audio, sr = librosa.load(file_path)
    audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
    audio_normalized = (audio_resampled - np.mean(audio_resampled)) / np.std(audio_resampled)
    return audio_normalized

def normalize_data(audio_file):
    audio_normalized = (audio_file - np.mean(audio_file)) / np.std(audio_file)
    return audio_normalized

# function to remove silence from audio
def remove_silence(input_path, output_path, min_silence_length_ms=300, silence_threshold=-50):
    audio = AudioSegment.from_file(input_path)
    chunks = split_on_silence(audio, min_silence_len = min_silence_length_ms, silence_thresh=silence_threshold)
    output = AudioSegment.empty()

    for chunk in chunks:    # reassemble non-silent segments
        output += chunk

    output.export(output_path, format="wav")
    return output 

# function to repeat audio file until it has length of at least min_target_length
def repeat_audio(audio, sr=24000, min_target_length=4):
    length_s = len(audio)/float(sr)

    if length_s < min_target_length:
        n = np.ceil(min_target_length*sr/len(audio))
        audio = np.tile(audio,int(n))
    
    return audio

def remove_silence_dataset(dataset, dataset_dictionary):
    # Prevents re-generating silence-cropped audio
    if (os.path.isdir(f"Data\\no_silence\\{dataset}")):
        print('Dataset has already had silence cut from audio. Skipping... ')

        with open(f'Data/no_silence/{dataset}_paths', 'rb') as f:
            data = pickle.load(f)
            f.close()
        dataset_dictionary['no silence path'] = data
        return 
    
    print('No silence-cropped data found. Generating audio without silence...')
    os.makedirs(f"Data\\no_silence\\{dataset}", exist_ok=True)
        
    dataset_dictionary['no silence path'] = []
    
    if dataset == "RAVDESS":     # in practicality, we will only be removing audio from RAVDESS 
        sil_thresh = -65
    elif dataset == "SAVEE":
        sil_thresh = -45
    else:
        sil_thresh = -50

    for index, audio_path in enumerate(dataset_dictionary['audio path']):
        # Generate audio without silent segments
        silence_modified_path = f"Data\\no_silence\\{dataset}\\{dataset}_sil_{str(index).zfill(6)}_emotion_{dataset_dictionary['label'][index]}.wav"
        remove_silence(audio_path, silence_modified_path, silence_threshold=sil_thresh)

        dataset_dictionary['no silence path'].append(silence_modified_path)
        
    print('Dataset successfully cropped without silence segments.')

    # Save dataset dictionary's resampled paths
    data_filename = f'Data/no_silence/{dataset}_paths'
    with open(data_filename, 'wb') as f:
        pickle.dump(dataset_dictionary['no silence path'], f)
    f.close()

    return 


def preprocess_dataset(dataset, dataset_dictionary):
    # Prevents re-running if the data has already been processed
    if (os.path.isdir(f"Data\\resampled_no_silence_no_looping\\{dataset}")):
        print('Dataset has already been normalized and resampled. Skipping...')
        return
    
    print('No processed data found. Processing the dataset...')
    os.makedirs(f"Data\\resampled_no_silence_no_looping\\{dataset}", exist_ok=True)
        
    for index, audio_path in enumerate(dataset_dictionary['no silence path']):
        # Resampling and normalizing
        audio_modified = resample_data(audio_path, target_sampling_rate)
        audio_modified = normalize_data(audio_modified)
        
        # Skipping audio looping
        # if len(audio_modified) != 0:
        #    audio_modified = repeat_audio(audio_modified, sr=target_sampling_rate, min_target_length=5)

        # Save audio output as wav file
        resampled_path = f"Data\\resampled_no_silence_no_looping\\{dataset}\\{dataset}_resampled_{str(index).zfill(6)}_emotion_{dataset_dictionary['label'][index]}.wav"
        sf.write(resampled_path, audio_modified, target_sampling_rate)
        librosa.get_samplerate(resampled_path)
    print('Dataset normalized and resampled successfully.')
    return


# function to add modified audio file's path to dataset dictionaries
def add_modified_path(dataset, dataset_dictionary):
    for index, audio_path in enumerate(dataset_dictionary['audio path']):
        path_name = f"Data\\resampled_no_silence_no_looping\\{dataset}\\{dataset}_resampled_{str(index).zfill(6)}_emotion_{dataset_dictionary['label'][index]}.wav"
        dataset_dictionary['resampled audio path'].append(path_name)
    return (dataset_dictionary)

# function to combine multiple dataset dictionaries into one
def merge_dataset_dictionaries(*dataset_dictionaries):
    merged_dictionary = {'path': [], 'label': []}  # will return a dictionary with only file paths and their labels
    for dataset_dictionary in dataset_dictionaries:
        merged_dictionary['path'] += dataset_dictionary['resampled audio path']
        merged_dictionary['label'] += dataset_dictionary['label']
    return merged_dictionary


# Now, different functions specifically for each filename format in different datasets:

# TESS labels: ['angry' 'disgust' 'fear' 'happy' 'neutral' 'ps' 'sad']
def TESS():

    dataset_path = "Data\\TESS"                     # keeps the main path of the dataset
    dataset_folders = os.listdir(dataset_path)      # lists all the folders inside the dataset

    TESS_dictionary = {'audio path': [], 'dataset label': [], 'label': [], 'resampled audio path': [], 'no silence path': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for file in dataset_folders:
        if file == "TESS Toronto emotional speech set data":
            continue

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
    print("Skipping generation of audio files without silence.")
    TESS_dictionary['no silence path'] = TESS_dictionary['audio path']
    preprocess_dataset('TESS', TESS_dictionary)
    TESS_dictionary = add_modified_path('TESS', TESS_dictionary)
    
    return TESS_dictionary


# CREMA labels: ['ANG' 'DIS' 'FEA' 'HAP' 'NEU' 'SAD']
def CREMA():
    
    dataset_path = "Data\\CREMA"                     # keeps the main path of the dataset
    audio_files = os.listdir(dataset_path)           # lists all the folders inside the dataset

    CREMA_dictionary = {'audio path': [], 'dataset label': [], 'label': [], 'resampled audio path': [], 'no silence path': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for audio in audio_files:
        audio_path = os.path.join(dataset_path, audio)
        audio_label = audio.split("_")[2]
        audio_label_global = assign_global_labels('CREMA', audio_label)

        CREMA_dictionary['audio path'].append(audio_path)
        CREMA_dictionary['dataset label'].append(audio_label)
        CREMA_dictionary['label'].append(audio_label_global)

    # preprocess all the audio files and keep the new paths
    print("Skipping generation of audio files without silence.")
    CREMA_dictionary['no silence path'] = CREMA_dictionary['audio path']
    preprocess_dataset('CREMA', CREMA_dictionary)
    CREMA_dictionary = add_modified_path('CREMA', CREMA_dictionary)

    return CREMA_dictionary


# SAVEE labels: ['a' 'd' 'f' 'h' 'n' 'sa' 'su']
def SAVEE():
    
    dataset_path = "Data\\SAVEE"                     # keeps the main path of the dataset
    audio_files = os.listdir(dataset_path)           # lists all the folders inside the dataset

    SAVEE_dictionary = {'audio path': [], 'dataset label': [], 'label': [], 'resampled audio path': [], 'no silence path': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for audio in audio_files:
        audio_path = os.path.join(dataset_path, audio)
        audio_label = audio.split("_")[1][:-6]
        audio_label_global = assign_global_labels('SAVEE', audio_label)

        SAVEE_dictionary['audio path'].append(audio_path)
        SAVEE_dictionary['dataset label'].append(audio_label)
        SAVEE_dictionary['label'].append(audio_label_global)

    # preprocess all the audio files and keep the new paths
    print("Skipping generation of audio files without silence.")
    SAVEE_dictionary['no silence path'] = SAVEE_dictionary['audio path']
    preprocess_dataset('SAVEE', SAVEE_dictionary)
    SAVEE_dictionary = add_modified_path('SAVEE', SAVEE_dictionary)
    
    return SAVEE_dictionary


# RAVDESS labels:
#
#   01 = neutral
#   02 = calm (skipping)
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

    RAVDESS_dictionary = {'audio path': [], 'dataset label': [], 'label': [], 'resampled audio path': [], 'no silence path': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for file in dataset_folders:
        if file == "audio_speech_actors_01-24":
            continue

        file_path = os.path.join(dataset_path, file)
        audio_files = os.listdir(file_path)
        
        for audio in audio_files:
            audio_path = os.path.join(file_path, audio)
            audio_label = (audio.split("-"))[2]

            # Skip calm
            if audio_label == '02':
                continue
            audio_label_global = assign_global_labels('RAVDESS', audio_label)

            RAVDESS_dictionary['audio path'].append(audio_path)
            RAVDESS_dictionary['dataset label'].append(audio_label)
            RAVDESS_dictionary['label'].append(audio_label_global)

    # preprocess all the audio files and keep the new paths
    remove_silence_dataset('RAVDESS', RAVDESS_dictionary)
    preprocess_dataset('RAVDESS', RAVDESS_dictionary)
    RAVDESS_dictionary = add_modified_path('RAVDESS', RAVDESS_dictionary)

    return RAVDESS_dictionary

# EMOdb labels:
#
#       A = anxiety/fear
#       F = happiness
#       T = sadness
#       N = neutral
#       NOTE: We only care about anxiety (fear), happiness, sadness, and neutral
#       since we want to augment our dataset
#
def EMOdb():
    dataset_path = "Data\\EMOdb"                  # keeps the main path of the dataset
    audio_files = os.listdir(dataset_path)      # lists all the folders inside the dataset

    EMOdb_dictionary = {'audio path': [], 'dataset label': [], 'label': [], 'resampled audio path': [], 'no silence path': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for audio in audio_files:
        audio_path = os.path.join(dataset_path, audio)
        audio_label = audio[5]
        if audio_label in ['A', 'F', 'T', 'N']:
            audio_label_global = assign_global_labels('EMOdb', audio_label)

            EMOdb_dictionary['audio path'].append(audio_path)
            EMOdb_dictionary['dataset label'].append(audio_label)
            EMOdb_dictionary['label'].append(audio_label_global)

    # preprocess all the audio files and keep the new paths
    print("Skipping generation of audio files without silence.")
    EMOdb_dictionary['no silence path'] = EMOdb_dictionary['audio path']
    preprocess_dataset('EMOdb', EMOdb_dictionary)
    EMOdb_dictionary = add_modified_path('EMOdb', EMOdb_dictionary)

    return EMOdb_dictionary

# In case one wants to just use the resampled data, we ignore all the original datasets and use all the
# resampled data

def load_resampled():
    
    global global_labels
    
    dataset_path = 'Data\\resampled_no_silence_no_looping'      # separate directory for resampled data that have no silent portions
    available_datasets = os.listdir(dataset_path)
    
    CREMA_dictionary = {'resampled audio path': [], 'label': []}
    RAVDESS_dictionary = {'resampled audio path': [], 'label': []}
    SAVEE_dictionary = {'resampled audio path': [], 'label': []}
    TESS_dictionary = {'resampled audio path': [], 'label': []}
    EMOdb_dictionary = {'resampled audio path': [], 'label': []}
    
    for dataset in available_datasets:

        file_path = os.path.join(dataset_path, dataset)
        audio_files = os.listdir(file_path)
        
        audio_files.sort()
        
        if dataset == 'CREMA': print('-----------CREMA:',len(audio_files))
        
        dataset_dictionary = locals()[dataset+'_dictionary']
        
        for audio in audio_files:
            
            audio_path = os.path.join(file_path, audio)
            audio_label = int((audio.split("_"))[-1][:-4])   # takes only the last section (x.wav) and removes the '.wav'
            
            dataset_dictionary['resampled audio path'].append(audio_path)
            dataset_dictionary['label'].append(audio_label)
    
    return CREMA_dictionary, RAVDESS_dictionary, SAVEE_dictionary, TESS_dictionary, EMOdb_dictionary