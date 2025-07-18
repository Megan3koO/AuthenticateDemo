const express = require('express');
const router = express.Router();
const {authenticateToken, authorizeRoles} = require('../controllers/auth');

const JWT_SECRET = require('../models/secrets').JWT_KEY
const jwt = require('jsonwebtoken')
const Request = require('../models/request')

router.get('/api', (req, res) => {
    res.status(200).json({'message': 'Hello, World!'});
});

router.post('/api/request-access', async (req, res) => {
  const token = req.body['token']
  const approver = req.body['approver']
  const requesting_role = req.body['request_role']

  const decoded = jwt.decode(token, JWT_SECRET);
  const username = decoded['id'];
  const role = decoded['role'];

  const requestData = {
    "sender" : username,
    "approver" : approver,
    "role" : role,
    "reason" : "request-access",
    "status" : "pending",
    "requestBody" : {
      "reason" : "request-access",
      "request_role" : requesting_role
    }
  };

  try{
    result = Request.create(requestData);
  }
  catch (error)
  {   
      console.log(error);
      return res.status(500).send("Unexpected error when creating user");
  }
  
  //need to avoid spamming here
  res.status(201).json({'message' : 'Request sent!'});
});


router.get('/api/pending-request', async (req, res) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader?.split(' ')[1];

  const decoded = jwt.decode(token, JWT_SECRET);

  const username = decoded['id'];
  requests = undefined
  try
  {
    requests = await Request.find({approver : username, status: "pending"});
  }
  catch (error)
  {
    console.log('Error: ', error);
    return res.status(403).send('Error getting requests');
  }
  return res.status(200).json({'message': requests});
});

module.exports = router;