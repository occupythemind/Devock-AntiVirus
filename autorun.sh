#! bash
. env/bin/activate
python Web/manage.py runserver > /dev/null 2>&1 &
mitmdump -s main.py
#sudo freshclam
#sudo systemctl restart clamav-daemon