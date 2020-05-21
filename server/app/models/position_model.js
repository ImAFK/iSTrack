const mongoose = require('mongoose');
Schema = mongoose.Schema;

let PositionSchema = new Schema({

  name: {
    type: String,
    required: true
  },
  complete_address:{
    type: String,
    required: true
  }
});

const Position = mongoose.model('Position', PositionSchema);
module.exports = Position;