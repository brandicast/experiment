var MongoClient = require("mongodb").MongoClient;

MongoClient.connect("mongodb://localhost:27017", function (err, db) {
    if (err) throw err;
    var dbo = db.db('mongodbtest');
    dbo.createCollection('line_user', function (err, res) {
        dbo.collection('line_user').insertOne({
            line_id: 1234,
            gateway: [{
                gw_id: 5678,
                mute: false,
                last_update: 0
            }]
        });
        dbo.collection('line_user').insertOne({
            line_id: 2234,
            gateway: [{
                gw_id: 5678,
                mute: false,
                last_update: 0
            }]
        });

        dbo.collection('line_user').countDocuments(function (err, count) {
            if (err) throw err;
            console.log("Total Rows:" + count);
            db.close();
        })

    })

})