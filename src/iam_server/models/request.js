const mongoose = require('mongoose');

const RequestSchema = new mongoose.Schema({
  sender: { type: String, required: true},
  approver: { type: String, required: true},
  role: { type: String, required: true, enum: ['user', 'admin', 'editor']},
  reason: { type: String, required: true, enum: ['request-access', 'request-resource']},
  status: { type: String, required: true, enum: ['pending', 'approved', 'rejected']},
  requestBody: {type: Object, required: true} //should be handle by api
}, {collection: 'requests'});

module.exports = mongoose.model('Request', RequestSchema);