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
    numAvailable integer,
);

create table if not exists admins(
    auth0 text;
);

create table if not exists images(
    imgur text unique,
    r_id text,
    dhash text
);
