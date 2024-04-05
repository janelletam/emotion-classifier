import * as React from 'react';
import logo from './logo.svg';
import './App.css';

// MUI components
import RecordBox from './components/RecordBox';
import Title from './components/Title';
import { Container } from "@mui/material"

function App() {
  return (
    <div className="App">
      <Container sx={{marginY:10}}>
        <Title/>
        <RecordBox/>
      </Container>
    </div>
  );
}

export default App;