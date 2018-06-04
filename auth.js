/* tests/auth.js */

const fs = require("fs");
const sqlite = require("sqlite3");
const assert = require("assert");

const auth = require("../auth.js");
const DB_TMP = ".data/tmp.db";
const DB_SCHEMA = "schema.sql";

function getDB(){
    return (new sqlite.Database(DB_TMP));
}

function getMsg(){
    return {
        chat: {
            id: 123456
        }
    };
}

describe("Auth", function(){
    beforeAll(function(){
        process.env.DATABASE = DB_TMP;
    });

    beforeEach(function(done){
        fs.readFile(DB_SCHEMA, function(err, data){
            var db = getDB(); 
            db.exec(data.toString(), function(){ done(); });
            db.close();
        });
    });

    afterEach(function(done){
        fs.unlink(DB_TMP, function(){ done(); });
    });

    describe("#funcAuth()", function(){
        it("everything fine", function(done){
            auth.funcAuth(getMsg().chat.id)
            .then(() => { 
                // check that request token written into database
                var db = getDB();
                db.all("SELECT * from twitter_reqTkns", function(err, rows){
                    assert.ok(rows.length==1);
                    done();
                }); 
                db.close();
            }); 
        });
    });

    describe("#funcAuth2()", function(){
        it("reqTkn not exist", function(done){
            auth.funcAuth2("fake_reqtkn", "fake_verifier")
            .catch(() => done());
        });

        it("reqTkn exist, verifier fake", function(done){
            auth.funcAuth(getMsg().chat.id)
            .then((url) => auth.funcAuth2(url.split("=")[1], "fake_verifier"))
            .catch(() => done());
        });
    });
});
