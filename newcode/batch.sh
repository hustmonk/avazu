keys="C1 banner_pos site_id site_domain site_category app_id app_domain app_category device_id device_ip device_model device_type device_conn_type C14 C15 C16 C17 C18 C19 C20 C21"
keys="C14 C15 C16 C17 C18 C19 C20 C21"
#keys="site_id site_domain site_category app_id app_domain app_category device_id device_ip device_model device_type device_conn_type C14 C15 C16 C17 C18 C19 C20 C21"
#keys="app_id site_id"
for key in $keys
do
    echo $key
    python train.py $key
done
