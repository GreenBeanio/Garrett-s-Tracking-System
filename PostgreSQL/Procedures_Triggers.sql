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
	/* raise notice 'count : %', TG_TABLE_NAME; */
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
	parent_count int; /* Stores the parent rows */
	largest_number_right int; /* Stores the largest index is correct */
	largest_index int = 0; /* stores the largest index in use */
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
			largest_index = 1; /* Putting this here incase it's all 0s */
		else
			/* If the last number was 0 and the next number wasn't */
			if last_ind = 0 AND current_ind != 0 THEN
				RAISE EXCEPTION 'Daily Log Activity Error: Category (>0) added after empty (0)';
			end if;
			last_ind = current_ind;
		end if;
		/* Get the largest index */
		if current_ind != 0 Then
			largest_index = int_index;
		end if;
	END LOOP;

	/* Possibly add the feature to create children if they don't exist and it's a valid number 
	select count(user_entry)
	into parent_count
	from DL_Activities
	where user_id = new."user_id" AND
		first_num = new."first_num"; */

	/* Check the previous number in the largest category */
	/* actually maybe I should start bottom up not top down */
	/* no I should start from the top down because recrsion should "cascade" down */

	raise notice 'largest : %', largest_index;

	/* Don't check if it's the primary category */
	if largest_index != 1 THEN
		/* Check if the largest number should be smaller */
		select count(user_entry) /* Doesn't matter what column just need to check existence */
		into largest_number_right
		from DL_Activities
		where (user_id = new."user_id") AND (first_num = new."first_num") AND /* these are always needed */
			(Case
				When largest_index = 2 THEN second_num = new."second_num" - 1
				When largest_index > 2 THEN second_num = new."second_num" ELSE
				second_num = 0 END
			) AND
			(Case
				When largest_index = 3 THEN third_num = new."third_num" - 1
				When largest_index > 3 THEN third_num = new."third_num" ELSE
				third_num = 0 END
			) AND
			(Case
				When largest_index = 4 THEN fourth_num = new."fourth_num" - 1
				When largest_index > 4 THEN fourth_num = new."fourth_num" ELSE
				fourth_num = 0 END
			) AND
			(Case
				When largest_index = 5 THEN fifth_num = new."fifth_num" - 1
				When largest_index > 5 THEN fifth_num = new."fifth_num" ELSE
				fifth_num = 0 END
			) AND
			(Case
				When largest_index = 6 THEN sixth_num = new."sixth_num" - 1
				When largest_index > 6 THEN sixth_num = new."sixth_num" ELSE
				sixth_num = 0 END
			) AND
			(Case
				When largest_index = 7 THEN seventh_num = new."seventh_num" - 1
				When largest_index > 7 THEN seventh_num = new."seventh_num" ELSE
				seventh_num = 0 END
			) AND
			(Case
				When largest_index = 8 THEN eighth_num = new."eighth_num" - 1
				When largest_index > 8 THEN eighth_num = new."eighth_num" ELSE
				eighth_num = 0 END
			) AND
			(Case
				When largest_index = 9 THEN ninth_num = new."ninth_num" - 1
				when largest_index > 9 THEN ninth_num = new."ninth_num" ELSE
				ninth_num = 0 END
			) AND
			(Case
				When largest_index = 10 THEN tenth_num = new."tenth_num" - 1 ELSE
				tenth_num = 0 END
			);
		raise notice 'largest number : %', largest_number_right;
		/* If the "older sibling" doesn't exist throw error */
		if largest_number_right = 0 THEN /* IS NUll THEN */
			/* throwing an error now, in the future I suppose I could instead get the max value from the
			siblings and then add 1 to it, but I think I'd rather give the user the ability to verify that first */
			RAISE EXCEPTION 'Daily Log Activity Error: Largest activity index has no older sibling (prior child in parent)';
		end if;
	end if;

	/* Don't check if there isn't a parent */
	/* Huh, just realized this kind of doesn't matter because the prior check also prevents not having a parent 
	I might need to put this one on top of the other check */
	if largest_index != 1 THEN
		/* Checking if the parent exists */
		select count(user_entry) /* Doesn't matter what column just need to check existence */
		into parent_count
		from DL_Activities
		where (user_id = new."user_id") AND
			(Case
				When largest_index >= 2 THEN first_num = new."first_num" END /* Nothing else to check it wouldn't run */
			) AND
			(Case
				When largest_index >= 3 THEN second_num = new."second_num" ELSE
				second_num = 0 END
			) AND
			(Case
				When largest_index >= 4 THEN third_num = new."third_num" ELSE
				third_num = 0 END
			) AND
			(Case
				When largest_index >= 5 THEN fourth_num = new."fourth_num" ELSE
				fourth_num = 0 END
			) AND
			(Case
				When largest_index >= 6 THEN fifth_num = new."fifth_num" ELSE
				fifth_num = 0 END
			) AND
			(Case
				When largest_index >= 7 THEN sixth_num = new."sixth_num" ELSE
				sixth_num = 0 END
			) AND
			(Case
				When largest_index >= 8 THEN seventh_num = new."seventh_num" ELSE
				seventh_num = 0 END
			) AND
			(Case
				When largest_index >= 9 THEN eighth_num = new."eighth_num" ELSE
				eighth_num = 0 END
			) AND
			(Case
				When largest_index = 10 THEN ninth_num = new."ninth_num" ELSE
				ninth_num = 0 END
			) AND (tenth_num = 0); /* The tenth should always be 0 for this test since it has no children categories */
		raise notice 'parent : %', parent_count;
		/* If the "parent" doesn't exist throw an error */
		if parent_count = 0 THEN
			/* I would like to auto populate parents if they're missing. It should only take one insert in the
			trigger because of recursion */
			RAISE EXCEPTION 'Daily Log Activity Error: No parent for the entry';
		end if;
	end if;
	/*--------*/
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
