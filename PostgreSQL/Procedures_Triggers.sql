/* --------------------------- */
/* Function & Trigger for finding the User Entry */
/* --------------------------- */

/* Function to get the current User Entry (for multiple tables) */
CREATE or Replace FUNCTION DL_User_Entry()
RETURNS trigger
as $$
declare
	new_entry int; /* Variable to store the count */
begin 
	EXECUTE format('select max(user_entry)
	from %I
	where user_id = $1."user_id";', TG_TABLE_NAME) INTO new_entry Using new; 
	/* $1 is the identifier for the USING new. %I is the passed SQL table name. */
	
	/*
	/* Get the largest amount of entires the user made */
	select max(user_entry)
	into new_entry
	from DL_Activities
	where user_id = new."user_id";
	*/

	/* Set the new entry value for the user */
	if new_entry IS NUll THEN
		new_entry = 1;
	ELSE
		new_entry = new_entry + 1;
	end if;
	/* raise notice 'count : %', new_entry; */
	raise notice 'count : %', TG_TABLE_NAME;
	new."user_entry" = new_entry; /* Set the entry amount in the new row */
	return new; /* Return the new row */
end;
$$ language plpgsql;

/* Trigger for user entries on DL activites */
CREATE or Replace TRIGGER Trig_DL_Act_User_Entry
	BEFORE INSERT on DL_Activities
	FOR EACH ROW
	EXECUTE FUNCTION DL_User_Entry();

/* Trigger for user entries on DL activites */
CREATE or Replace TRIGGER Trig_DL_Log_User_Entry
	BEFORE INSERT on DL_Log
	FOR EACH ROW
	EXECUTE FUNCTION DL_User_Entry();

/* --------------------------- */
/* Function & Trigger for ensuring parent activities exist */
/* --------------------------- */
/* I think this may be served better on the backend instead of a
stored procedure and trigger. That way I can automatically insert
needed parents. I'm sure I could do that here, but it'd probably
be easier to implement in python. */

/* Function to check activities for parenthood */
CREATE or Replace FUNCTION DL_Act_Parenthood()
RETURNS trigger
as $$
declare
	int_index int = 0; /* Stores the for loop index */
	last_ind int; /* Stores the previous array value */
	current_ind int; /* Stores the current array value */
	insert_array int[]; /* Stores activity identifiers */
begin 
	/* Insert the new values into an array */
	insert_array = Array[new.first_num, new.second_num, new.third_num,
	new.fourth_num, new.fifth_num, new.sixth_num, new.seventh_num,
	new.eighth_num, new.ninth_num, new.tenth_num];

	/* First checking that there is no 0 prior to anything else */
	FOREACH current_ind in ARRAY insert_array LOOP
		int_index = int_index + 1;
		if int_index = 1 then
			last_ind = current_ind;
		else
			/* If the last number was 0 and the next number wasn't */
			if last_ind = 0 AND current_ind != 0 THEN
				RAISE EXCEPTION 'Daily Log Activity Error: Category (>0) added after empty (0)';
			end if;
			last_ind = current_ind;
		end if;
	END LOOP;

	/* Possibly add the feature to create children if they don't exist and it's a valid number */

	return new; /* Don't forget to return silly */
end;
$$ language plpgsql;

/* Trigger for user entries on DL activites */
CREATE or Replace TRIGGER Trig_DL_Act_Parenthood
	BEFORE INSERT on DL_Activities
	FOR EACH ROW
	EXECUTE FUNCTION DL_Act_Parenthood();

/* --------------------------- */
/* Function & Trigger to Round Times */
/* --------------------------- */

/* Function to Round Times [TO THE MINUTE] (for multiple tables) */
/* This is one that should probably be handled by the front end or back end.
This shouldn't hurt though. I'm also setting it to round to the minute, because
that's what I've been using before this software was created. I might change it
to seconds in the future, but probably not now */
CREATE or Replace FUNCTION DL_Round_Time()
RETURNS trigger
as $$
declare
	s_time timestamptz;
	e_time timestamptz;
begin
	new."time_start" = date_trunc('minute', new."time_start");
	new."time_end" = date_trunc('minute', new."time_end");
	return new;
end;
$$ language plpgsql;

/* Trigger for user entries on DL activites */
CREATE or Replace TRIGGER Trig_DL_Log_Round_Time
	BEFORE INSERT on DL_Log
	FOR EACH ROW
	EXECUTE FUNCTION DL_Round_Time();
