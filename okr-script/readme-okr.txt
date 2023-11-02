1. ganti url dan token di 1_okr-get-user-team-obj.py dan run "python 1_okr-get-user-team-obj.py"

2. run "python 2_filter-okr-list.py" untuk fix csv format

3. cek di csv dan instance jika diperlukan lakukan import objective cycle / teams / user dulu dengan:
	run "python 4_(opt)-okr-post-obj-cycle.py"
	run "python 5_(opt)-okr-post-teams.py"
	run "python 6_(opt)-okr-post-user.py"
*Note: ganti url dan token juga pada setiap (opt) file

4. ganti url dan token di 3_okr-post.py dan run "python 3_okr-post.py"