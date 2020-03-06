# curl -X POST -H o
# curl -X POST -H 'Authorization: Token 76769f4cd57a4dc88d0e78bcf8ee81e54f8785b4' -H "Content-Type: application/json" -d '{"direction":"e"}' localhost:8000/api/adv/move/

# curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser", "password1":"testpassword", "password2":"testpassword"}' localhost:8000/api/registration/

curl -X GET -H 'Authorization: Token a017a7007bf5ecdfb6210b28fd83607123627682' -H "Content-Type: application/json"  localhost:8000/api/adv/room
printf '\n\n'
curl -X POST -H 'Authorization: Token a017a7007bf5ecdfb6210b28fd83607123627682' -H "Content-Type: application/json" -d '{"direction":"n"}' localhost:8000/api/adv/move/
printf '\n\n'
curl -X POST -H 'Authorization: Token a017a7007bf5ecdfb6210b28fd83607123627682' -H "Content-Type: application/json" -d '{"message":"something"}' localhost:8000/api/adv/say
printf '\n\n'
# curl -X GET -H 'Authorization: Token a017a7007bf5ecdfb6210b28fd83607123627682' -H "Content-Type: application/json" localhost:8000/api/adv/inventory
# printf '\n'

curl -X GET -H 'Authorization: Token a017a7007bf5ecdfb6210b28fd83607123627682' -H "Content-Type: application/json"  https://binary-assassins.herokuapp.com/api/adv/room
printf '\n\n'
curl -X POST -H 'Authorization: Token a017a7007bf5ecdfb6210b28fd83607123627682' -H "Content-Type: application/json" -d '{"direction":"n"}' https://binary-assassins.herokuapp.com/api/adv/move/
printf '\n\n'
curl -X POST -H 'Authorization: Token a017a7007bf5ecdfb6210b28fd83607123627682' -H "Content-Type: application/json" -d '{"message":"something"}' https://binary-assassins.herokuapp.com/api/adv/say
printf '\n\n'
