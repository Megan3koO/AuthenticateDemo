const jwt = require('jsonwebtoken');

const JWT_SECRET = require('../models/secrets').JWT_KEY; // Store in env in real apps

function authenticateUser(req, res, next) {
  // should be used to authenticate password and username
};

// Middleware to verify token
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader?.split(' ')[1];

  if (!token) return res.status(401).send("Missing token!");
  jwt.verify(token, JWT_SECRET, (err, id) => {
    if (err)
    {
      //console.error('Token verification failed:', err.message);
      return res.status(403).send("Invalid token!");
    }
    
    /*
    if (!id || !id.id || !id.role) {
      console.error('Invalid token payload:', id);
      return res.sendStatus(403);
    }
    if (!req.username) {
      console.error('Username not found in request:', req);
      return res.sendStatus(403);
    }

    if (req.username && req.username !== id.id) {
      console.error('Username mismatch:', req.username, id.id);
      return res.sendStatus(403);
    }
    */
    req.role = id.role;
    next();
  });
}

// Middleware to check roles
function authorizeRoles(...allowedRoles) {
  //console.log('Allowed roles:', allowedRoles);
  return (req, res, next) => {
    if (!allowedRoles.includes(req.role)) {
      return res.status(403).send('Forbidden: insufficient rights');//json({ message: 'Forbidden: insufficient rights' });
    }
    next();
  };
}

module.exports = { authenticateToken, authorizeRoles };
