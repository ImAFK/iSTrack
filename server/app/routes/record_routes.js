var Record = require("../models/record_model");
var Position = require("../models/position_model");

const express = require('express');
router = express.Router();
xss = require('xss');
lib = require('../config/library');

router.get('/test', function (req, res) {
  res.send("Record Routes Working");
});

// Create a new Record
router.post("/create", function (req, res) {

  var errors = [];
  id_number = xss(req.body.id_number);
  location = xss(req.body.location);
  first_name = xss(req.body.first_name);
  last_name = xss(req.body.last_name);
  body_temperature = xss(req.body.body_temperature);

  userInfos = [id_number, location, first_name, last_name, body_temperature];
  console.log(userInfos);

  userInfos.forEach(data => {
    if (lib.checkIfContainsHTML(data)) {
      console.log("Attempt of XSS Injection by IP " + req.connection.remoteAddress);
      errors.push("HTML Tags inside data");
    }
  });
  userInfos.length = 0;

  if (!id_number) {
    res.status(400).send({ message: "id_number cannot be empty." })
    return
  }
  const record = new Record({
    id_number: id_number,
    location : location.name,
    first_name: first_name,
    last_name: last_name,
    body_temperature: body_temperature,
    date : new Date()
  });
  
  record
    .save(record)
    .then(data => {
      res.send(data)
    })
    .catch(err => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while creating the Record."
      })
    })
});

// Get All the Records
router.get("/read-all/", function (req, res) {
  const id_number = req.query.id_number
  var condition = id_number ? { id_number: { $regex: new RegExp(id_number), $options: "i" } } : {}

  Record.find(condition)
    .then(data => {
      res.send(data)
    })
    .catch(err => {
      message:
      err.message || "Some error occurred while retrieving Records."
    })
});

// Find a single Record with an id
router.get('/read-one/', function(req, res) {
  
  Record.findOne({id_number: req.body.id_number}, function(err, record) {
    if(err) throw err;
    if(!record)
        res.status(500).send("No existing record with the given id");
    else
        res.status(201).send(record);
  }); 

});

module.exports = router;