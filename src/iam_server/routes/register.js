const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt'); // Assuming bcrypt is used for password hashing

const User = require('../models/user'); // Assuming User model is defined in models/user.js
const JWT_SECRET = require('../models/secrets').JWT_KEY; // Store in env in real apps
const BCRYPT_SECRET = require('../models/secrets').BCRYPT_KEY;

router.post('/register', async (req, res) => {
    const user = await User.findOne({ username: req.body.username });
    if (user) {
        return res.status(401).send('User already exists!');
    }
    
    if (!req.body.password) {
        return res.status(401).send('Password is required');
    }

    //Should use bcrypt or similar for password hashing in real apps
    hashedPassword = bcrypt.hashSync(req.body.password, BCRYPT_SECRET);
    console.log('Hashed password:', hashedPassword);

    const userData = {
        "username" : req.body.username,
        "password" : hashedPassword,
        "role" : "user"
    };

    try
    {
        await User.create(userData);
    }
    catch (error)
    {   
        console.log(error);
        return res.status(500).send("Unexpected error when creating user");
    }
    
    return res.status(201).send({"message" : 'Created'}); //Leave it for now
});

module.exports = router;