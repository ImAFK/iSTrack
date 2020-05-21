const mongoose = require('mongoose');
  Schema = mongoose.Schema;
  Position = require('../models/position_model').schema

let RecordSchema = new Schema({

  //Student card id or ROC id in future scaling
  id_number: {
    type: String,
    required: true
  },
  // This is the device id
  location:{ 
    type: String,
    required: false
  },
  first_name: {
    type: String,
    required: true
  },
  last_name: {
    type: String,
    required: true
  },
  body_temperature: {
    type: Number,
    required: true
  },
  date: Date
  // inside outside params
});

const Record = mongoose.model('Record', RecordSchema);
module.exports = Record;