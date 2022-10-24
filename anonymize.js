const mongoose = require('mongoose')

console.log(process.argv[2]);
try{
    mongoose.connect(process.argv[2]);
    console.log('Connected to DB')
    }catch(err){console.log(err)}

