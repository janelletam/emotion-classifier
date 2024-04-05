// Fonts
import * as React from "react";
import { ReactMediaRecorder } from "react-media-recorder";

// MUI components
import { Button, Container, Typography, Box } from "@mui/material";
import { KeyboardVoiceRounded, StopCircleRounded } from "@mui/icons-material";

const RecordBox = () => {
  return (
    <ReactMediaRecorder
      audio
      render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
        <div className="RecordBox">
          <Container sx={{ marginY: 2.5 }}>
            <Button
              variant="contained"
              color={"primary"}
              sx={{ width: "200px", height: "50px" }}
              onClick={startRecording}
            >
              <Box display="flex" alignItems="center">
                <Box ml={1} mr={1}>
                  {"Record"}
                </Box>
                <KeyboardVoiceRounded />
              </Box>
            </Button>
            <Button
              variant="contained"
              color={"secondary"}
              sx={{ width: "200px", height: "50px" }}
              onClick={stopRecording}
            >
              <Box display="flex" alignItems="center">
                <Box ml={1} mr={1}>
                  {"Stop"}
                </Box>
                <StopCircleRounded />
              </Box>
            </Button>
          </Container>
          {status === "stopped" && (
            <audio src={mediaBlobUrl} controls autoPlay loop />
          )}
        </div>
      )}
    />
  );
};
// function RecordBox() {
//   // Keep track to see if we're recording or not
//   const [isRecording, setIsRecording] = React.useState(false);

//   // Start recording function
//   const startRecording = () => {
//     let constraints = { audio: true };
//     audioContext = new window.AudioContext();

//     console.log("sample rate: " + audioContext.sampleRate);

//     navigator.mediaDevices
//       .getUserMedia(constraints)
//       .then(function (stream) {
//         console.log("Initializing recorder");
//         gumStream = stream;
//         let input = audioContext.createMediaStreamSource(stream);

//         recorder = new window.Recorder(input, {
//           numChannels: 1,
//         });

//         recorder.record();
//         console.log("Recorder started");
//         setIsRecording(true);
//       })
//       .catch(function (err) {
//         // If getUserMedia() fails, reset recording state
//         console.log(err);
//         setIsRecording(false);
//       });
//   };

//   // Stop recording function
//   const stopRecording = () => {
//     console.log("Stop recording clicked");
//     recorder.stop();
//     gumStream.getAudioTracks()[0].stop();
//     recorder.exportWAV(onStop);
//     setIsRecording(false);
//   };

//   const onStop = (blob) => {
//     console.log("Uploading...");

//     let data = new FormData();
//     data.append("wavfile", blob, "recording.wav");

//     const config = {
//       headers: { "content-type": "multipart/form-data" },
//     };

//     axios.post("http://localhost:3000/predict", data, config);
//   };

//   return (
//     <div className="RecordBox">
//       <Container sx={{ marginY: 2.5 }}>
//         <Button
//           variant="contained"
//           color={isRecording ? "secondary" : "primary"}
//           sx={{ width: "200px", height: "50px" }}
//           onClick={isRecording ? stopRecording : startRecording}
//         >
//           <Box display="flex" alignItems="center">
//             <Box ml={1} mr={1}>
//               {isRecording ? "Stop" : "Record"}
//             </Box>
//             <KeyboardVoiceRounded />
//           </Box>
//         </Button>
//       </Container>
//     </div>
//   );
// }

export default RecordBox;