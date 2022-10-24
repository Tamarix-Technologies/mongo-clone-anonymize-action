const mongoose = require('mongoose')

console.log(process.argv[2]);
try{
    mongoose.connect(process.argv[2]);
    console.log('Connected to DB')
    }catch(err){console.log(err)}


var simpleMasksPt1Stage = {
    // FULL FIELD OBFUSCATION USING AN MD5 HASH OF ITS VALUE (note, not 'cryptographically safe')
    'username': {'$function': {'lang': 'js', 'args': ['$_id'], 'body':                   
                            function(id) {
                                return hex_md5(id);
                            }
                        }},
};

var pipeline = [
    {'$set': simpleMasksPt1Stage}
];

replace_pipeline = [].concat(pipeline);  // COPY THE ORIGINAL PIPELINE
replace_pipeline.push(
    {'$merge': {'into': { 'db': 'appdb', 'coll': 'users'}, 'on': '_id',  'whenMatched': 'replace', 'whenNotMatched': 'fail'}}
);
db.payments.aggregate(replace_pipeline);
db.payments.find();