const mongoose = require('mongoose');
const dbURI = 'mongodb://localhost:27017/iam';

class Database {
  constructor() {
  }

  async connect() {
    try {
      mongoose.connect(dbURI, { useNewUrlParser: true, useUnifiedTopology: true })
      .then(() => console.log('MongoDB connected successfully'));
    } catch (error) {
      console.error('MongoDB connection error:', error);
    }
  }

  async disconnect() {
    try {
      await mongoose.connection.close();
      console.log('MongoDB disconnected successfully');
    } catch (error) {
      console.error('MongoDB disconnection error:', error);
    }
  }

  async create(dbmodel, data) {
    try {
      await dbmodel.create(data);
      console.log('Model created successfully');
    } catch (error) {
      console.error('Error creating model:', error);
    }
  }

  async find(dbmodel, query) {
    try {
      const record = await dbmodel.findOne({ query });
      if (record) {
        console.log('Record found:', record);
        return record;
      }
      console.log('Record not found');
      return null;
    } catch (error) {
      console.error('Error finding record:', error);
      return null;
    }
  }
}

module.exports = new Database();