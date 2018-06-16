create table if not exists users(
    email text unique,
    tstamp integer,
    name text,
    code text
);

create table if not exists login(
    email text,
    tstamp text
);

create table if not exists rooms(
    _id integer primary key,
    u_email text,
    name text,
    weekRange integer,
    numAvailable integer
);

create table if not exists admins(
    email text unique
);

create table if not exists images(
    imgur text unique,
    link text,
    r_id integer,
    dhash text
);

create table if not exists vals(
    key text unique,
    val text
);

insert or replace into vals(key, val) values("email_verification", "
code: %s

use this code within the hour, if not the code will expire and you will have
to request a new one.

do not give this code to anyone else, we will never ask for it. if you didn't
request this, it is safe to ignore this email.

also, one time use only, if you key in a wrong code, please generate a new
one.

---");

insert or ignore into users(email) values("ongspxm@gmail.com");
insert or ignore into admins(email) values("ongspxm@gmail.com");
