/* Temp data */
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