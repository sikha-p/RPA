const express = require('express');
const path = require('path');
const app = express();
const port = 5555;

// Sample list of EMDR IDs
const emdrIds = [
  { id: '11111111111', name: 'EMDR 1' },
  { id: '22222222222', name: 'EMDR 2' },
  { id: '33333333333', name: 'EMDR 3' }
];

// Serve static files (like CSS, JS, etc.)
app.use(express.static(path.join(__dirname, 'public')));

// Route for the main EMDR list page
app.get('/apex', (req, res) => {
  let emdrListHtml = '<h1>EMDR List</h1><ul>';
  emdrIds.forEach(emdr => {
    emdrListHtml += `<li><a href="/apex/EMDR?id=${emdr.id}">${emdr.name}</a> | <a href="/apex/EMDR?id=${emdr.id}&edit=true">Edit</a></li>`;
  });
  emdrListHtml += '</ul>';
  res.send(emdrListHtml);
});

// Route for the EMDR page
app.get('/apex/EMDR', (req, res) => {
  const { id, edit } = req.query;
  const emdr = emdrIds.find(e => e.id === id);

  if (!emdr) {
    return res.status(404).send('EMDR not found');
  }

  if (edit === 'true') {
    // Render the edit view
    res.send(`
      <h1>Edit EMDR: ${emdr.name}</h1>
      <form action="/apex" method="GET">
        <label for="name">EMDR Name:</label>
        <input type="text" id="name" name="name" value="${emdr.name}">
        <button type="submit">Save</button>
      </form>
      <br><a href="/apex/EMDR?id=${emdr.id}">Cancel</a>
    `);
  } else {
    // Render the regular EMDR page
    res.send(`
      <h1>EMDR: ${emdr.name}</h1>
      <p>ID: ${emdr.id}</p>
      <br><a href="/apex/EMDR?id=${emdr.id}&edit=true">Edit</a> | <a href="/apex">Back to List</a>
    `);
  }
});

// POST route to handle form submission when editing
app.post('/apex/EMDR', (req, res) => {
  const { id } = req.query;
  const { name } = req.body;

  // Find the EMDR and update its name
  const emdr = emdrIds.find(e => e.id === id);
  if (emdr) {
    emdr.name = name;
    res.redirect(`/apex/EMDR?id=${id}`);
  } else {
    res.status(404).send('EMDR not found');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
