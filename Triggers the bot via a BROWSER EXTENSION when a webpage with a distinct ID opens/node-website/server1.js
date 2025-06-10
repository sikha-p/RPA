const express = require('express');
const app = express();
const port = 3000;

app.use(express.static('public'));

app.get('/apex/EMDR', (req, res) => {
  const emdrId = req.query.id;

  if (!emdrId) {
    res.status(400).send("Missing EMDR ID");
    return;
  }

  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>EMDR?id=${emdrId}</title>
    </head>
    <body>
      <h1>EMDR Page: ${emdrId}</h1>
      <p>This is a test page for EMDR ID ${emdrId}.</p>
      <button onclick="editEMDR()">Simulate Edit</button>

      <script>
        function editEMDR() {
          window.postMessage({ type: "emdr_edited" }, "*");
        }
      </script>
    </body>
    </html>
  `);
});

app.listen(port, () => {
  console.log("EMDR test site running at http://localhost:/3000");
});
