// Fonts
import * as React from 'react';

// MUI components
import { Container, Typography, Box } from "@mui/material";

const Title = () => {
  return (
    <div className="Title">
        <Container>
            <Typography variant="h4" component="h2">
                <Box component="span" fontWeight='fontWeightMedium'>
                    Emotion Classifier Model
                </Box>
            </Typography>
        </Container>   
    </div>
  );
}

export default Title;