let mongoose = require('mongoose');

// defining a pitch schema for the database
// also helps in carrying out the checks for fields in request object
let pitchSchema = new mongoose.Schema({
    entrepreneur: {
        type: String,
        required: true
    },
    pitchTitle: {
        type: String,
        required: true
    },
    pitchIdea: {
        type: String,
        required: true
    },
    askAmount: {
        type: Number,
        required: true
    },
    equity: {
        type: Number,
        required: true
    },
    offers: [{                      // offers array holds all the offers made by the sharks
        investor: {
            type: String,
            required: true
        },
        amount: {
            type: Number,
            required: true
        },
        equity: {
            type: Number,
            required: true
        },
        comment: {
            type: String,
            required: true
        }
    }]
});

let pitch = mongoose.model('pitch', pitchSchema);

module.exports = pitch; // exporting the pitch model