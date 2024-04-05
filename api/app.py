from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
from pydub.silence import split_on_silence
import librosa
import soundfile as sf
import numpy as np
from io import BytesIO
import torch
import torch.optim as optim
from model import CNNModel

app = Flask(__name__)
CORS(app)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Set up model
model_path = 'api\ModelWeights\trained_model.pth' # to edit
model = CNNModel(num_classes=8).to(device)
model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))

@app.route('/predict', methods=['POST'])
def predict():
    audio_file = request.files['audio']

    # Process the audio_file (convert to wav, remove silence, resample, normalize)
    mfccs = convert_to_mfcc(audio_file)

    # Prediction
    model.eval()
    with torch.no_grad():
        my_input = mfccs.unsqueeze(1)
        my_input = my_input.to(device)
        outputs = model(my_input)
        pred_accuracy, predicted = torch.max(outputs, 1)

    return jsonify({'prediction': predicted.item(), 
                    'prediction accuracy':  round(pred_accuracy.item(), 2), 
                    'confidence': outputs.softmax(dim=1).squeeze().tolist(), 
                    'emotions': ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']})

# function to remove silence from audio
def remove_silence(input_path, output_path, min_silence_length_ms=300, silence_threshold=-50):
    audio = AudioSegment.from_file(input_path)
    chunks = split_on_silence(audio, min_silence_len = min_silence_length_ms, silence_thresh=silence_threshold)
    output = AudioSegment.empty()

    for chunk in chunks:    # reassemble non-silent segments
        output += chunk

    output.export(output_path, format="wav")
    return output 


# REMOVE THIS MAYBE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# function to repeat audio file until it has length of at least min_target_length
def repeat_audio(audio, sr=24000, min_target_length=4):
    length_s = len(audio)/float(sr)

    if length_s < min_target_length:
        n = np.ceil(min_target_length*sr/len(audio))
        audio = np.tile(audio,int(n))
    
    return audio
  
        
# function to normalize and resamples every file into a specific sample rate (sr)
def resample_data(file_path, target_sr):
    audio, sr = librosa.load(file_path)
    audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
    audio_normalized = (audio_resampled - np.mean(audio_resampled)) / np.std(audio_resampled)
    return audio_normalized


def normalize_data(audio_file):
    audio_normalized = (audio_file - np.mean(audio_file)) / np.std(audio_file)
    return audio_normalized
 

def pad_audio(audio, sr, desired_length_in_sec):
    # audio is the raw audio signal as numpy array from librosa
    desired_length = int(sr * desired_length_in_sec)

    # Truncate if too long
    if len(audio) > desired_length:
        audio = audio[:desired_length]
        # TODO: Check for silent parts before cropping the audio file

    # Else, pad with 0s
    else:
        padding = int(desired_length - len(audio))
        audio = np.pad(audio, (0, padding), 'constant')
    return audio


# extract MFCCs from the audio files
def extract_mfccs(file_path=None, audio=None, n_mfcc=13):
    
    # Checks if the input has been a file path or a file
    if (file_path!=None): audio, sr = librosa.load(file_path, sr=None)
    else: sr = 24000
        
    audio = pad_audio(audio, sr, 4.0)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    delta_mfcc  = librosa.feature.delta(mfcc)
    delta2_mfcc = librosa.feature.delta(mfcc, order=2)

    # Stacking mfcc and deltas together
    combined_matrix = np.vstack([mfcc, delta_mfcc, delta2_mfcc])

    # Normalize mfccs
    combined_matrix = (combined_matrix - np.mean(combined_matrix, axis=0)) / np.std(combined_matrix, axis=0)

    # We transpose so that the ROWS correspond to the frames of the audio, while COLUMNS represent features
    transposed_matrix = np.transpose(combined_matrix, [1, 0])
    return transposed_matrix


def convert_to_mfcc(audio_file):
    target_sampling_rate = 24000

    audio_data = BytesIO(audio_file.read())
    audio_segment = AudioSegment.from_file_using_temporary_files(audio_data)

    # Export AudioSegment to WAV format
    with NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
        wav_filename = temp_wav_file.name
        audio_segment.export(wav_filename, format="wav") 

    no_silence_path = f'{wav_filename}_no_sil'
    no_silence_audio = remove_silence(wav_filename, no_silence_path, min_silence_length_ms=300, silence_threshold=-50)
    resampled_audio = resample_data(no_silence_path, target_sr=target_sampling_rate)
    normalized_audio = normalize_data(resampled_audio)
    
    mfccs = extract_mfccs(audio=normalized_audio)

    # Delete the temporary WAV file
    os.remove(wav_filename)
    os.remove(no_silence_path)

    return mfccs


if __name__ == '__main__':
    app.run(debug=True)