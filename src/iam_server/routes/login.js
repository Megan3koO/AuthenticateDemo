const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt'); // Assuming bcrypt is used for password hashing

/*
const mongoose = require('mongoose');
const UserSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  role: { type: String, required: true, unique: true }});
const User = mongoose.model('user', UserSchema);
*/
const User = require('../models/user'); // Assuming User model is defined in models/user.js
const JWT_SECRET = require('../models/secrets').JWT_KEY; // Store in env in real apps
const BCRYPT_SECRET = require('../models/secrets').BCRYPT_KEY;

router.get('/login', async (req, res) => {
    const user = await User.findOne({ username: req.headers.username });
    if (!user) {
        return res.status(404).send('User not found');
    }
    
    if (!req.headers.password) {
        return res.status(400).send('Password is required');
    }

    //Should use bcrypt or similar for password hashing in real apps
    hashedPassword = bcrypt.hashSync(req.headers.password, BCRYPT_SECRET);
    /*
    bcrypt.compare(hashedPassword, user.password, (err, result) => {
        if (err) {
            console.error('Error comparing passwords:', err);
            return res.status(500).send('Internal server error');
        }
        if (!result) {
            return res.status(401).send('Wrong password');
        }
    });
    */
    const password = user.password;
    if (!(password === hashedPassword)) {
        return res.status(401).send('Wrong password');
    }

    const token = jwt.sign({ id: user.username, role: user.role }, JWT_SECRET, { expiresIn: '1h' });
    return res.status(200).json({ token });
});

module.exports = router;