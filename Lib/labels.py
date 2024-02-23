
import os

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
#---------------------------------------------------------------------------------------------------------

# global labels dictionary
global_labels = {'neutral': 1, 'calm': 2, 'happy': 3, 'sad': 4, 'angry': 5, 'fearful': 6, 'disgust': 7,
                 'surprised': 8}

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



# Now, different functions specifically for each filename format in different datasets:

# TESS labels: ['angry' 'disgust' 'fear' 'happy' 'neutral' 'ps' 'sad']
def TESS():

    dataset_path = "Data\\TESS"                     # keeps the main path of the dataset
    dataset_folders = os.listdir(dataset_path)      # lists all the folders inside the dataset

    # all the information regarding the audio files in TESS will be kept in and returned as TESS_dictionary
    # it will contain:  1. audio's path
    #                   2. audio's dataset label
    #                   3. audio's global label
    TESS_dictionary = {'audio path': [], 'dataset label': [], 'label': []}

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

    return TESS_dictionary


# CREMA labels: ['ANG' 'DIS' 'FEA' 'HAP' 'NEU' 'SAD']
def CREMA():
    
    dataset_path = "Data\\CREMA"                     # keeps the main path of the dataset
    audio_files = os.listdir(dataset_path)           # lists all the folders inside the dataset

    # all the information regarding the audio files in TESS will be kept in and returned as CREMA_dictionary
    # it will contain:  1. audio's path
    #                   2. audio's dataset label
    #                   3. audio's global label
    CREMA_dictionary = {'audio path': [], 'dataset label': [], 'label': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for audio in audio_files:
        audio_path = os.path.join(dataset_path, audio)
        audio_label = audio.split("_")[2]
        audio_label_global = assign_global_labels('CREMA', audio_label)

        CREMA_dictionary['audio path'].append(audio_path)
        CREMA_dictionary['dataset label'].append(audio_label)
        CREMA_dictionary['label'].append(audio_label_global)
        

    return CREMA_dictionary


# SAVEE labels: ['a' 'd' 'f' 'h' 'n' 'sa' 'su']
def SAVEE():
    
    dataset_path = "Data\\SAVEE"                     # keeps the main path of the dataset
    audio_files = os.listdir(dataset_path)           # lists all the folders inside the dataset

    # all the information regarding the audio files in TESS will be kept in and returned as SAVEE_dictionary
    # it will contain:  1. audio's path
    #                   2. audio's dataset label
    #                   3. audio's global label
    SAVEE_dictionary = {'audio path': [], 'dataset label': [], 'label': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for audio in audio_files:
        audio_path = os.path.join(dataset_path, audio)
        audio_label = audio.split("_")[1][:-6]
        audio_label_global = assign_global_labels('SAVEE', audio_label)

        SAVEE_dictionary['audio path'].append(audio_path)
        SAVEE_dictionary['dataset label'].append(audio_label)
        SAVEE_dictionary['label'].append(audio_label_global)

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

    # all the information regarding the audio files in TESS will be kept in and returned as RAVDESS_dictionary
    # it will contain:  1. audio's path
    #                   2. audio's dataset label
    #                   3. audio's global label
    RAVDESS_dictionary = {'audio path': [], 'dataset label': [], 'label': []}

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

    return RAVDESS_dictionary
