/* --------------------------- */
/* Temp Date */
/* --------------------------- */

Insert Into GTS_Accounts 
	(user_uuid, username, password, salt, creation, last_session, total_sessions)
	Values
	(gen_random_uuid(), 'SuperTom', '24496183853626216512831333924456',
	'93792120806686679433866248008591', now(), now(), 1);

Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'yum'),
	(1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'yum');

Insert Into DL_Log
	(user_id, activity_1, activity_2, activity_3, activity_4, activity_5, time_start, time_end)
	Values
	(1, '1-0-0-0-0-0-0-0-0-0', '1-0-0-0-0-0-0-0-0-0', '1-0-0-0-0-0-0-0-0-0', '1-0-0-0-0-0-0-0-0-0',
		'1-0-0-0-0-0-0-0-0-0', date_trunc('minute', now()), date_trunc('minute', now() + interval '30 minutes')),
	(1, '2-0-0-0-0-0-0-0-0-0', '1-0-0-0-0-0-0-0-0-0', '1-0-0-0-0-0-0-0-0-0', '1-0-0-0-0-0-0-0-0-0',
		'1-0-0-0-0-0-0-0-0-0', date_trunc('minute', now() + interval '30 minutes'), 
	date_trunc('minute', now() + interval '1 hour'));

/*------*/
Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'yum');
Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 'yum');
Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'yum');
Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'yum');
Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 5, 2, 1, 0, 0, 0, 0, 0, 0, 0, 'yum');
Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 5, 2, 2, 0, 0, 0, 0, 0, 0, 0, 'yum');
Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 5, 2, 3, 0, 0, 0, 0, 0, 0, 0, 'yum');
Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 5, 2, 4, 0, 0, 0, 0, 0, 0, 0, 'yum');
Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 'yum');
Insert Into DL_Activities
	(user_id, first_num, second_num, third_num, fourth_num, fifth_num, sixth_num,
	seventh_num, eighth_num, ninth_num, tenth_num, label)
	Values
	(1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'yum');
