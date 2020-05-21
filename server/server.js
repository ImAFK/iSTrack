const express = require('express');
bodyParser = require('body-parser');
path = require('path');
logger = require('morgan');
app = express();
mongoose = require('mongoose');

/* DB Entities */
const record = require('./app/routes/record_routes');

const env = require("./app/models")
const options = {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    user: 'admin',
    pass: 'password'
};
mongoose.connect(env.url, options);
mongoose.Promise = global.Promise;
let db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

/* Logger to keep track on the dev*/
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));


/* Routes */
app.use('/record', record);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log('Server running on port ' + PORT);
    console.log('Shortcut : http://localhost:' + PORT);
});