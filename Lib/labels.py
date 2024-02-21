
import os

#---------------------------------------------------------------------------------------------------------
# TODO: Global labels for emotions as numbers
# Note: currently the labels currently are only as kept as the generic filenames
#
# Note: RAVDESS already has a clear and straightforward labeling for the emotions. The labels are:
#   01 = neutral
#   02 = calm
#   03 = happy
#   04 = sad
#   05 = angry
#   06 = fearful
#   07 = disgust
#   08 = surprised
# Maybe these can be implemented in our global emotion labels...
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
#   Surprised   TESS, CREMA, RAVDESS
#   Calm        RAVDESS
#  
#---------------------------------------------------------------------------------------------------------


# TESS labels: ['angry' 'disgust' 'fear' 'happy' 'neutral' 'ps' 'sad']
def TESS():

    dataset_path = "Data\\TESS"                     # keeps the main path of the dataset
    dataset_folders = os.listdir(dataset_path)      # lists all the folders inside the dataset

    # all the information regarding the audio files in TESS will be kept in and returned as TESS_dictionary
    # it will contain:  1. audio's path
    #                   2. audio's filename
    #                   3. audio's label
    TESS_dictionary = {'audio path': [], 'audio name': [], 'label': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for file in dataset_folders:
        file_path = os.path.join(dataset_path, file)
        audio_files = os.listdir(file_path)
        
        for audio in audio_files:
            audio_path = os.path.join(file_path, audio)
            audio_name = audio[:-4]
            audio_label = audio.split("_")[2][:-4]
            TESS_dictionary['audio path'].append(audio_path)
            TESS_dictionary['audio name'].append(audio_name)
            TESS_dictionary['label'].append(audio_label)

    return TESS_dictionary


# CREMA labels: ['ANG' 'DIS' 'FEA' 'HAP' 'NEU' 'SAD']
def CREMA():
    
    dataset_path = "Data\\CREMA"                     # keeps the main path of the dataset
    audio_files = os.listdir(dataset_path)           # lists all the folders inside the dataset

    # all the information regarding the audio files in TESS will be kept in and returned as CREMA_dictionary
    # it will contain:  1. audio's path
    #                   2. audio's filename
    #                   3. audio's label
    CREMA_dictionary = {'audio path': [], 'audio name': [], 'label': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for audio in audio_files:
        audio_path = os.path.join(dataset_path, audio)
        audio_name = audio[:-4]
        audio_label = audio.split("_")[2]
        CREMA_dictionary['audio path'].append(audio_path)
        CREMA_dictionary['audio name'].append(audio_name)
        CREMA_dictionary['label'].append(audio_label)

    return CREMA_dictionary


# SAVEE labels: ['a' 'd' 'f' 'h' 'n' 'sa' 'su']
def SAVEE():
    
    dataset_path = "Data\\SAVEE"                     # keeps the main path of the dataset
    audio_files = os.listdir(dataset_path)           # lists all the folders inside the dataset

    # all the information regarding the audio files in TESS will be kept in and returned as SAVEE_dictionary
    # it will contain:  1. audio's path
    #                   2. audio's filename
    #                   3. audio's label
    SAVEE_dictionary = {'audio path': [], 'audio name': [], 'label': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for audio in audio_files:
        audio_path = os.path.join(dataset_path, audio)
        audio_name = audio[:-4]
        audio_label = audio.split("_")[1][:-6]
        SAVEE_dictionary['audio path'].append(audio_path)
        SAVEE_dictionary['audio name'].append(audio_name)
        SAVEE_dictionary['label'].append(audio_label)

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
    #                   2. audio's filename
    #                   3. audio's label
    RAVDESS_dictionary = {'audio path': [], 'audio name': [], 'label': []}

    # going through each file in the dataset and extract the information about all the audio files inside
    for file in dataset_folders:
        file_path = os.path.join(dataset_path, file)
        audio_files = os.listdir(file_path)
        
        for audio in audio_files:
            audio_path = os.path.join(file_path, audio)
            audio_name = audio[:-4]
            audio_label = (audio.split("-"))[2]
            RAVDESS_dictionary['audio path'].append(audio_path)
            RAVDESS_dictionary['audio name'].append(audio_name)
            RAVDESS_dictionary['label'].append(audio_label)

    return RAVDESS_dictionary
