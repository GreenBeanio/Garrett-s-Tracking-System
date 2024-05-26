/* ---------------------------*/

/* Creating the main database */
CREATE database GTS;

/* Creating an admin account for the database */
Create user gts_admin with Password 'qF=9;{k%=Dyk=CL87B0iXW:bN[:dS{Qk'; /* Obviously change the password */
Grant All On Schema public to gts_admin;

/* ---------------------------*/

/* Table of Accounts */
CREATE TABLE GTS_Accounts (
	/* Columns */
	id bigint GENERATED ALWAYS AS IDENTITY,
	user_uuid uuid constraint ac_nn_uuid not null,
	username varchar(64) constraint ac_nn_user not null,
	password char(32) constraint ac_nn_pass not null,
	salt char(32) constraint ac_nn_salt not null,
	recovery jsonb,
	email varchar(320), /* Max length of emails */
	creation timestamptz constraint ac_nn_timec not null,
	last_session timestamptz constraint acc_nn_timels not null,
	total_sessions int constraint dl_nn_ts not null,
	/* Constraints */
	constraint ac_pk primary key (id),
	constraint ac_u_uuid unique(user_uuid),
	constraint ac_u_user unique(username),
	constraint ac_u_pass unique(password)
);

/* Table of Sessions */
CREATE TABLE GTS_Sessions (
	/* Columns */
	id int GENERATED ALWAYS AS IDENTITY,
	key uuid constraint s_nn_key not null,
	user_id bigint constraint s_f_uid References GTS_Accounts(id),
	creation timestamptz constraint s_nn_timec not null,
	expiration timestamptz constraint s_nn_timee not null,
	/* Constraints */
	constraint s_pk primary key (id),
	constraint s_u_key unique(key)
);

/* Create Accounts and Sessions user */
Create User u_accounts with Password 'V=_?#Ko(Z0X4#n2F';  /* Obviously change the password */
Grant ALL on GTS_Accounts to u_accounts;
Grant ALL on GTS_Sessions to u_accounts;

/* ---------------------------*/

/* Table for the Activities */
CREATE TABLE DL_Activities (
	/* Columns */
	id bigint GENERATED ALWAYS AS IDENTITY,
	user_entry int constraint act_nn_ue not null,
	user_id bigint constraint act_f_uid References GTS_Accounts(id),
	reference varchar(59) GENERATED ALWAYS AS (
	first_num || '-' || 
	second_num || '-' || 
	third_num || '-' || 
	fourth_num || '-' || 
	fifth_num || '-' || 
	sixth_num || '-' || 
	seventh_num || '-' || 
	eighth_num || '-' ||
	ninth_num || '-' ||
	tenth_num || '-') STORED, /* 5 digits per every category + the five - 
	this is kind of stupid because I can't use concat. 
	I might just do this back end and send it to sql */
	first_num smallint constraint dl_first_num not null,
	first_text text,
	second_num smallint constraint dl_second_num not null,
	second_text text,
	third_num smallint constraint dl_third_num not null,
	third_text text,
	fourth_num smallint constraint dl_fourth_num not null,
	fourth_text text,
	fifth_num smallint constraint dl_fifth_num not null,
	fifth_text text,
	sixth_num smallint constraint dl_sixth_num not null,
	sixth_text text,
	seventh_num smallint constraint dl_seventh_num not null,
	seventh_text text,
	eighth_num smallint constraint dl_eighth_num not null,
	eighth_text text,
	ninth_num smallint constraint dl_ninth_num not null,
	ninth_text text,
	tenth_num smallint constraint dl_tenth_num not null,
	tenth_text text,
	label text constraint dl_label not null,
	comment text,
	/* Constraints */
	constraint dl_act_pk primary key (id),
	constraint dl_act_user_entry unique(user_id, user_entry),
	constraint dl_reference unique(user_id, reference)
	/* I might change these to deafuly 0 instead of null, but hmmm not sure */
);

/* Table for the Daily Log */
CREATE TABLE DL_Log (
	/* Columns */
	id bigint GENERATED ALWAYS AS IDENTITY,
	user_entry int constraint dl_nn_ue not null,
	user_id bigint constraint dl_f_uid References GTS_Accounts(id),
	/* Have to specify these seperate for composite foreign key later */
	activity_1 varchar(59) constraint dl_nn_act1 not null, 
	activity_2 varchar(59) constraint dl_nn_act2 not null,
	activity_3 varchar(59) constraint dl_nn_act3 not null,
	activity_4 varchar(59) constraint dl_nn_act4 not null,
	activity_5 varchar(59) constraint dl_nn_act5 not null,
	/* Don't think I need to specify not null, but it wont hurt */
	time_start timestamptz constraint dl_nn_time_s not null,
	time_end timestamptz constraint dl_nn_time_e not null,
	duration interval GENERATED ALWAYS AS (time_end - time_start) STORED, /* Will need to make sure this works with python */
	source text,
	/* Constraints */
	constraint dl_l_pk primary key (id),
	constraint dl_l_user_entry unique(user_id, user_entry),
	/* Have to do this buffoonery because reference is a composite unique not true unique */
	constraint dl_act1 foreign key (user_id, activity_1) References DL_Activities(user_id, reference),
	constraint dl_act2 foreign key (user_id, activity_2) References DL_Activities(user_id, reference),
	constraint dl_act3 foreign key (user_id, activity_3) References DL_Activities(user_id, reference),
	constraint dl_act4 foreign key (user_id, activity_4) References DL_Activities(user_id, reference),
	constraint dl_act5 foreign key (user_id, activity_5) References DL_Activities(user_id, reference)
);

/* Create Daily Log User */
Create User u_daily with Password 'zQ2&q}.85{mpaYRm';  /* Obviously change the password */
Grant ALL on DL_Activities to u_daily;
Grant ALL on DL_Log to u_daily;