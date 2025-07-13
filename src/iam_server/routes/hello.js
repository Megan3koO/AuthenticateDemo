const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.send('Hello, World!');
});

router.post('/', (req, res) => {
  res.send('Hello, World! POST request received!');
});

router.put('/', (req, res) => {
  res.send('Hello, World! PUT request received!');
});

router.delete('/', (req, res) => {      
  res.send('Hello, World! DELETE request received!');
});

module.exports = router;