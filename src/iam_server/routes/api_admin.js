const express = require('express');
const router = express.Router();
const {authenticateToken, authorizeRoles} = require('../controllers/auth');

router.get('/admin/api', authenticateToken, authorizeRoles('admin'), (req, res) => {
  res.status(200).json({'message': 'Hello, Admin!'});
});

router.post('/admin/approve-request', authenticateToken, authorizeRoles('admin'), (req, res) => {
    res.status(200).json({'message': 'Hello, Admin'});
});

module.exports = router;