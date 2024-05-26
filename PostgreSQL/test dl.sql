/* ---------------------------*/

/* Function to get the current User Entry */
CREATE or Replace FUNCTION DL_Act_User_Entry()
RETURNS trigger
as $$
declare
	new_entry int; /* Variable to store the count */
begin 
	/* Get the largest amount of entires the user made */
	select max(user_entry)
	into new_entry
	from TG_TABLE_NAME
	where user_id = new."user_id";
	/* Set the new entry value for the user */
	if new_entry IS NUll THEN
		new_entry = 1;
	ELSE
		new_entry = test + 1;
	end if;
	/* raise notice 'count : %', new_entry; */
	new."user_entry" = new_entry; /* Set the entry amount in the new row */
	return new; /* Return the new row */
end;
$$ language plpgsql;

/* Trigger for user entries on DL activites */
CREATE or Replace TRIGGER tempt
	BEFORE INSERT on DL_Activities
	FOR EACH ROW
	EXECUTE FUNCTION DL_Act_User_Entry();
