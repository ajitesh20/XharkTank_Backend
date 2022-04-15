const express = require('express');
const mongoose = require('mongoose');
const PORT = process.env.PORT || 8081;

// saving the pitch collection to a variable
let pitch = require('./pitchCollection');

// creating a new express app
const app = express();
app.use(express.json());

// connecting to the database
mongoose.connect('mongodb://localhost/xharktank');
let db = mongoose.connection;

// checking if the connection is successful
db.once('open', () => {
    console.log('Connected to Db');
});
db.on('error', (err) => {
    console.log(err)
});

// function to change _id key to id
function renameIdKey(obj) {
    let temp = {};
    temp.id = obj._id;
    temp.entrepreneur = obj.entrepreneur;
    temp.pitchTitle = obj.pitchTitle;
    temp.pitchIdea = obj.pitchIdea;
    temp.askAmount = obj.askAmount;
    temp.equity = obj.equity;
    temp.offers = [];
    obj.offers.forEach(offer => {
        temp.offers.push({
            id: offer._id,
            investor: offer.investor,
            amount: offer.amount,
            equity: offer.equity,
            comment: offer.comment
        });
    });
    return temp;
}

app.get('/', (req, res) => {
    res.send('Hello World');
});

// Endpoint to post a pitch to the backend
app.post('/pitches', (req, res) => {
    req.body.offers = [];
    if (req.body.equity > 100 || req.body.equity < 0 || req.body.askAmount < 0 || req.body.entrepreneur == "" || req.body.pitchTitle == "" || req.body.pitchIdea == "") {
        res.status(400).send("Invalid Request Body");
    }
    else {
        let newPitch = new pitch(req.body);
        newPitch.save((err, data) => {  // saving the pitch to the collection after checks
            if (err) {
                res.status(400).send("Invalid Request Body");
            } else {
                res.status(201).send({ "id": data._id });
            }
        });
    }
});

// Endpoint to make a counter offer for a pitch to the backend
app.post('/pitches/:id/makeOffer', (req, res) => {
    if (req.body.equity > 100 || req.body.equity < 0 || req.body.investor == "" || req.body.amount < 0 || req.body.comment == "") {
        res.status(400).send("Invalid Request Body");
    }
    pitch.findById(req.params.id, (err, data) => {  // finding pitch by id
        if (err || data == null) {
            res.status(404).send("Pitch not found");
        }
        else {
            data.offers.push(req.body); // saving offers to the pitch
            data.save((err, out) => {
                if (err) {
                    res.status(400).send("Invalid Request Body");
                } else {
                    res.status(201).send({ "id": out.offers[out.offers.length - 1]._id });
                }
            });
        }
    });
});

// Endpoint to fetch the all the pitches in the reverse chronological order
app.get('/pitches', (req, res) => {
    pitch.find({}, null, { sort: { pitched_at: -1 } }, (err, data) => {  // finding all pitches in reverse chronological order
        if (err) {
            res.status(500).send("Internal Server Error");
        } else {
            let allData = [];
            data.forEach(ele => {
                allData.push(ele);     // storing all the pitches in an array
            });
            let updatedJsonData = [];
            allData.forEach(ele => {
                let temp = renameIdKey(ele); // renaming the _id key to id
                updatedJsonData.push(temp);
            });
            res.status(200).send(updatedJsonData);
        }
    });
});

// Endpoint to specify a particular id to fetch a single Pitch
app.get('/pitches/:id', (req, res) => {
    pitch.findById(req.params.id, (err, data) => {
        if (err || data == null) {
            res.status(404).send("Pitch Not Found");
        }
        else {
            let temp = renameIdKey(data);     // renaming the _id key to id
            res.status(200).send(temp);       // sending the pitch with the specified id
        }
    });
});

// status 404 in all other cases
app.all('*', (req, res) => {
    res.status(404).send("Not Found");
});

// listening to the port

app.listen(PORT, () => {
    console.log('Server is running on port', PORT);
});