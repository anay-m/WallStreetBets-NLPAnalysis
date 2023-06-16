const express = require('express');
const sql = require('mysql');
const app = express();

app.get('/', (req,res) =>{
    res.send('This is the homepage');
});

const port = 8080; // or any other port number you prefer
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});