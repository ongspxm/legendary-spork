/* dbase.js */
const sqlite = require("sqlite3");

function getDB(){
    return (new sqlite.Database(process.env.DATABASE));
}

function procData(data){ 
    var keys = [];
    var vals = [];
    var rand = [];

    for (key in data) {
        keys.push(key); vals.push(data[key]);
        rand.push("?");
    }

    return {
        keys: keys,
        vals: vals,
        str: rand
    };
}

module.exports = {
    // callback(sqlite_obj)
    insert: function (table, data) {
        return new Promise((res, err) => { 
            var obj = procData(data);

            var sql = "INSERT INTO " + table + "("+
                obj.keys.join(",") + ") VALUES ("+
                obj.str.join(",") + ")";
           
            var db = getDB();
            db.run(sql, obj.vals, () => res());
            db.close(); 
        });
    },
    
    // fields = [field1, field2]
    // where = "u_id=?"; params = [u_id]
    // callback(rows) 
    select: function (table, where, params, fields) {
        return new Promise((res, err) => {
            var vals = "*";
            if (fields) {
                vals = fields.join(",");
            }

            var sql = "SELECT "+vals+" FROM "+table+" WHERE "+where;

            var db = getDB();
            db.all(sql, params, function(db_err, rows){
                if(db_err){
                    console.log("err: dbase.select - "+db_err);
                    return err();
                }
                res(rows);
            }); 
            db.close();

        });
    },
    
    // callback(sqlite_obj)
    update: function (table, data, where, params) {
        return new Promise((res, err) => {
            var obj = procData(data);
            keys = obj.keys.map(function(key){ return key+" = ?"; } ).join(",");

            var sql = "UPDATE "+table+" SET "+keys+" WHERE "+where;

            var db = getDB();
            db.run(sql, obj.vals.concat(params), () => res());
            db.close();
        });
    },

    // callback(sqlite_obj)
    delete: function (table, where, params) {
        return new Promise((res, err) => {
            var sql = "DELETE FROM "+table+" WHERE "+where;

            var db = getDB();
            db.run(sql, params, () => res());
            db.close();
        });
    },

    setup: function(schema){
        return new Promise((res, err) => {
            var db = getDB(); 
            db.exec(schema, ()=>res());
            db.close();
        });
    }
};
