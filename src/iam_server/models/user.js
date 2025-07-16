const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  password: { type: String, required: false },
  role: { type: String, required: true, unique: false, enum: ['user', 'admin', 'editor'], default: 'user' }}, {collection: 'users'});

module.exports = mongoose.model('User', UserSchema);