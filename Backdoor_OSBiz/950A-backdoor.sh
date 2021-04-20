#!/bin/sh
#Password is forced to enter new on first login. User placed on index 9 in database.

psql  -U postgres -t -A -d hipath -c "INSERT INTO as_login_data (login_user_id, login_user_role, login_user_name, login_user_passwd) VALUES(9,4,'bkm_unify@system','45e32f69ceb52b8a179cdd274cbbaaf1');" >/dev/null

rm -- "$0" #self destruct
exit 0
