const https = require('https');
const express = require('express');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process')
const app = express();
app.use(express.json());
app.use(express.static("express"));

// Define a POST API endpoint
app.post('/api/webhook', (req, res) => {
    console.log('API called');
    const payload = req.body;
     //console.log(payload );
     //console.log(payload );
     const headCommitAdded = payload.head_commit.added;
     const headCommitModified = payload.head_commit.modified;
     console.log(headCommitAdded  );
     console.log(headCommitModified );
     final = headCommitAdded.concat(headCommitModified);
     console.log(final)
    // Full path to the batch file
const batFilePath = 'C:\\Users\\Administrator\\Documents\\node-website\\runExportImport.bat';

const fileListString = JSON.stringify(final);
console.log("fileListString")
console.log(fileListString)
    const finalJoined = final.join(',');

// Construct the full command
const command = `"${batFilePath}" "${finalJoined}"`;
// Construct the command
     //const command = `C:\\Users\\Administrator\\Documents\\node-website\\runExportImport.bat `.final;
     console.log("command")
     console.log(command)

      exec(command, (error, stdout, stderr) => {
    if (error) {
        console.error(`Error: ${error}`);
        return;
    }

    if (stderr) {
        console.error(`stderr: ${stderr}`);
    }

    console.log(`stdout: ${stdout}`);
   });

    const commitId = payload?.head_commit?.id || 'No commit ID found';
    console.log('Commit ID:', commitId);

headCommitModified.forEach(filePath => {
  const directoryPath = path.dirname(filePath);
  console.log("Directory Path:", directoryPath);
});

    res.status(200).json({ message: 'Payload received successfully', commitId });
});

// Default route for the website
app.use('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/express/index.html'));
});

// Load SSL certificates
const sslOptions = {
    key: fs.readFileSync('\privatekey.pem'),
    cert: fs.readFileSync('\certificate.crt')
};

// Create the HTTPS server
const server = https.createServer(sslOptions, app);

// Listen on port 443
const port = 443;
server.listen(port, () => {
    console.log(`Server running on https://gsd.automationanywhere.net`);
});