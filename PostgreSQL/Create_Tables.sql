/*
Header Comment
Project: [Garrett's Tracking System] [https://github.com/GreenBeanio/Garrett-s-Tracking-System]
Copyright: Copyright (c) [2024]-[2024] [Garrett's Tracking System] Contributors
Version: [0.1]
Status: [Development]
License: [MIT]
Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
Project Description: [This project is used to track a variety of purposes.]
File Description: [An sql script for creating the tables]
*/

/* Table of Accounts */
CREATE TABLE accounts (
	/* Columns */
	id bigint GENERATED ALWAYS AS IDENTITY,
	username varchar(64) constraint ac_nn_user not null,
	password char(256) constraint ac_nn_pass not null,
	salt varchar(20) constraint ac_nn_salt not null,
	recovery jsonb,
	email varchar(320), /* Max length of emails */
	creation timestamptz constraint ac_nn_timec not null,
	last_session timestamptz constraint acc_nn_timels not null,
	total_sessions int constraint dl_nn_ts not null,
	/* Constraints */
	constraint ac_pk primary key (id),
	constraint ac_u_user unique(username),
    constraint ac_salt_min check (length(salt) >= 5)
);

/* Table of Sessions */
CREATE TABLE sessions (
	/* Columns */
	id int GENERATED ALWAYS AS IDENTITY,
    session_id char(256) constraint s_nn_si not null, /* The length of the session id */
	user_id bigint constraint s_f_uid References accounts(id),
	creation timestamptz constraint s_nn_timec not null,
	expiration timestamptz constraint s_nn_timee not null,
	/* Constraints */
	constraint s_pk primary key (id),
	constraint s_u_key unique(session_id)
);

/*
Footer Comment
History of Contributions:
[2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
*/