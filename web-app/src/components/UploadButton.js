import React, { useState } from "react";
import axios from "axios";
import {
  Button,
  LinearProgress,
  CircularProgress,
  Box,
  Typography,
  Container,
  Divider,
  styled,
} from "@mui/material";
import { CloudUploadRounded } from "@mui/icons-material";

const HiddenInput = styled("input")({
  display: "none",
});

function UploadButton() {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [predictionResult, setPredictionResult] = useState({
    prediction: null,
    predictionAccuracy: null,
    confidence: [],
    emotions: [],
  });

  const [prediction, setPrediction] = useState("");

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    axios
      .post("http://localhost:5000/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(percentCompleted);
        },
      })
      .then((response) => {
        setPrediction(response.data.prediction); // Store the prediction
        setLoading(false);
        setPredictionResult({
          prediction: response.data.prediction,
          predictionAccuracy: response.data.predictionAccuracy,
          confidence: response.data.confidence,
          emotions: response.data.emotions,
        });
        console.log(response);
      })
      .catch((error) => {
        setLoading(false);
        console.error(error);
      });
  };

  return (
    <div className="UploadButton">
      <Container sx={{ marginY: 2.5 }}>
        <HiddenInput
          accept="audio/*"
          className="UploadButton"
          id="contained-button-file"
          type="file"
          onChange={handleFileUpload}
        />
        <label htmlFor="contained-button-file">
          <Button variant="contained" color="primary" component="span">
            <Box display="flex" alignItems="center">
              <CloudUploadRounded />
              <Box ml={1} mr={1}>
                Upload Audio File
              </Box>
            </Box>
          </Button>
        </label>
        <LinearProgress
          sx={{ mt: 3 }}
          variant="determinate"
          value={uploadProgress}
        />
        {loading && <CircularProgress sx={{ mt: 2 }} />}{" "}
        {/* Show loading animation */}
        {predictionResult.prediction !== null && (
          <>
            <Divider sx={{ my: 2 }} />
            <Typography variant="h6">
              Predicted Emotion:{" "}
              {predictionResult.emotions[predictionResult.prediction]}
            </Typography>
            <Typography sx={{ mt: 2 }} variant="subtitle1">
              Accuracy: {Math.round(predictionResult.predictionAccuracy * 100)}%
            </Typography>
            <Typography variant="subtitle2">Confidence Levels:</Typography>
            {predictionResult.emotions.map((emotion, index) => (
              <Box key={emotion} mb={1}>
                <Typography variant="body2">{emotion}</Typography>
                <LinearProgress
                  variant="determinate"
                  value={predictionResult.confidence[index] * 100}
                />
              </Box>
            ))}
          </>
        )}
      </Container>
    </div>
  );
}

export default UploadButton;
