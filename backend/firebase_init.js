const admin = require('firebase-admin');
const serviceAccount = require('../supotify-57704-firebase-adminsdk-4iqts-882ee8420d.json'); 

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

module.exports = admin;
