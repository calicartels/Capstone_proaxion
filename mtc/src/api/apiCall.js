const express = require('express');
const axios = require('axios');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
const port = 8080;

// Middleware to parse JSON bodies
app.use(express.json());

// Middleware to handle CORS
app.use(cors());

// Endpoint to handle chatbot messages using Python script
app.post('/api/chatbot', async (req, res) => {
  const { message } = req.body;

  exec(`python c:\\Users\\jared\\Desktop\\Home\\Class\\549\\Capstone_proaxion\\mtc\\src\\api\\python_api.py "${message}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return res.status(500).json({ error: error.message });
    }
    if (stderr) {
      console.error(`Python script stderr: ${stderr}`);
      return res.status(500).json({ error: stderr });
    }
    console.log(`Python script stdout: ${stdout}`);
    res.json({ reply: stdout.trim() });
  });
});

// Catch-all route for handling 404 errors
app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

app.listen(port, () => {
  console.log(`API server listening on http://localhost:${port}`);
});