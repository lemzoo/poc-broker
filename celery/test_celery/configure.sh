# add user 'jimmy' with password 'jimmy123'
sudo rabbitmqctl add_user jimmy jimmy123
# add virtual host 'jimmy_vhost'
sudo rabbitmqctl add_vhost jimmy_vhost
# add user tag 'jimmy_tag' for user 'jimmy'
$sudo rabbitmqctl set_user_tags jimmy jimmy_tag
# set permission for user 'jimmy' on virtual host 'jimmy_vhost'
sudo rabbitmqctl set_permissions -p jimmy_vhost jimmy ".*" ".*" ".*"
