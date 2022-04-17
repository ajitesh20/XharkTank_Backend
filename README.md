# Xhark Tank Backend

## Introduction

This is the backend of the Xhark Tank application. Made as a project for Crio Launch 2022.

## Technologies Used

- [Node.js](https://nodejs.org/)
- [Express.js](https://expressjs.com/)
- [MongoDB](https://www.mongodb.com/)
- [Mongoose](https://mongoosejs.com/)

## Contents

It consists of 5 api endpoints:

### [POST] /pitches

Endpoint to post a pitch to the backend
Returns id of the pitch

### [POST] /pitches/<pitch_id>/makeOffer

Endpoint to make a counter offer for a pitch to the backend
Returns id of the offer

### [GET] /pitches

Endpoint to fetch the all the pitches in the reverse chronological order from the backend
Returns all the pitches from the database along with their offers

### [GET] /pitches/<pitch_id>

Endpoint to specify a particular id to fetch a single Pitch
Returns the pitch with the specified id

### [ALL] \*

Endpoint to return 404 error if the endpoint is not found

## Install & Run

### Preffered versions

npm : 7.6.1 or higher

Node.js : 14.16.1 or higher

MongoDB : 4.2.0 or higher

To install, run the following command:
_npm install_

To start the server, run the following command:
_npm start_

deployment:

Pitch idea:
https://rebrand.ly/xharktank-pitches-https/?author=ajiteshsaxena20&url=https://xharktank-ajitesh.herokuapp.com/

Invest in a pitch:
https://rebrand.ly/xharktank-invest-https/?author=ajiteshsaxena20&url=https://xharktank-ajitesh.herokuapp.com/

---
