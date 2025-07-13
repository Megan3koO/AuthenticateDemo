const express = require('express');
const router = express.Router();
const {authenticateToken, authorizeRoles} = require('../controllers/auth');

router.get('/api/admin', authenticateToken, authorizeRoles('admin'), (req, res) => {
  res.status(200).json({'message': 'Hello, Admin!'});
});

router.get('/api', (req, res) => {
    res.status(200).json({'message': 'Hello, World!'});
});

module.exports = router;