const jwt = require('jsonwebtoken');

const SECRET = "123456"; // Store in env in real apps

// Middleware to verify token
function authenticateToken(req, res, next) {
  //console.log(req.headers)
  const authHeader = req.headers['authorization'];
  const token = authHeader?.split(' ')[1];

  if (!token) return res.sendStatus(401);
  jwt.verify(token, SECRET, (err, id) => {
    if (err)
    {
      console.error('Token verification failed:', err.message);
      return res.sendStatus(403);
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
      return res.status(403).json({ message: 'Forbidden: insufficient rights' });
    }
    next();
  };
}

module.exports = { authenticateToken, authorizeRoles };
