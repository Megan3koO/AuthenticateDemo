const express = require('express');
const router = express.Router();
const {authenticateToken, authorizeRoles} = require('../controllers/auth');

const Request = require('../models/request');
const User = require('../models/user');

router.get('/admin/api', authenticateToken, authorizeRoles('admin'), (req, res) => {
  res.status(200).json({'message': 'Hello, Admin!'});
});

router.post('/admin/approve-request', authenticateToken, authorizeRoles('admin'), async (req, res) => {

    const request_id = req.body['_id'];
    const approverData = await User.findOne({username : req.body['approver']});
    const userData = await User.findOne({username : req.body['sender']});

    if (userData === undefined || approverData === undefined)
    {
      return res.status(404).send("User not found");
    }

    newData = req.body;
    
    if (req.body['reason'] === 'request-access')
    {
      if (approverData['role'] !== 'admin') //[TODO] should depend on weight. Leave it for now
      {
        newData['status'] = 'rejected';
        await Request.findOneAndUpdate({ _id : request_id}, newData, {upsert: true});
        return res.status(401).send("Fobidden! Unable to approve");
      }

      const body = req.body['requestBody'];
      if (req.body['role'] === body['request_role'])
      {
        newData['status'] = 'approved';
        await Request.findOneAndUpdate({ _id : request_id}, newData, {upsert: true});
        return res.status(201).json({'message': 'Role assigned already'});
      }


      newData['status'] = 'approved';
      newUserData = userData;
      newUserData['role'] = body['request_role'];

      await User.findOneAndUpdate({username : req.body['sender']}, userData, {upsert: true});
      await Request.findOneAndUpdate({_id : request_id}, newData, {upsert: true});
    }
    return res.status(201).json({'message': 'Request approved'});
});

module.exports = router;