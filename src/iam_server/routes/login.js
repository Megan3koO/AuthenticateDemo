const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');

/*
const mongoose = require('mongoose');
const UserSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  role: { type: String, required: true, unique: true }});
const User = mongoose.model('user', UserSchema);
*/
const User = require('../models/user'); // Assuming User model is defined in models/user.js
const SECRET = "123456"; // Store in env in real apps

router.get('/login', async (req, res) => {
    const user = await User.findOne({ username: req.query.username });
    if (!user) {
        return res.status(404).send('User not found');
    }
    
    if (!req.query.password) {
        return res.status(400).send('Password is required');
    }
    //Should use bcrypt or similar for password hashing in real apps
    const password = user.password;
    if (!(password === req.query.password)) {
        return res.status(401).send('Wrong password');
    }

    const token = jwt.sign({ id: user.username, role: user.role }, SECRET, { expiresIn: '1h' });
    res.status(200).json({ token });
});

module.exports = router;