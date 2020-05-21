const dbConfig = require("../config/db_config.js")
      mongoose = require("mongoose")
mongoose.Promise = global.Promise

const db = {}
db.mongoose = mongoose
db.url = dbConfig.url
db.person = require("./record_model.js")(mongoose)

module.exports = db