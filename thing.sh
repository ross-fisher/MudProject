# curl -X POST -H 'Authorization: Token 76769f4cd57a4dc88d0e78bcf8ee81e54f8785b4' -H "Content-Type: application/json" -d '{"direction":"e"}' localhost:8000/api/adv/move/
curl -X GET -H 'Authorization: Token 76769f4cd57a4dc88d0e78bcf8ee81e54f8785b4' -H "Content-Type: application/json"  localhost:8000/api/adv/room
printf '\n'
curl -X POST -H 'Authorization: Token 76769f4cd57a4dc88d0e78bcf8ee81e54f8785b4' -H "Content-Type: application/json" -d '{"direction":"e"}' localhost:8000/api/adv/move/
printf '\n'
curl -X POST -H 'Authorization: Token 76769f4cd57a4dc88d0e78bcf8ee81e54f8785b4' -H "Content-Type: application/json" -d '{"message":"something"}' localhost:8000/api/adv/say
printf '\n'
curl -X GET -H 'Authorization: Token 76769f4cd57a4dc88d0e78bcf8ee81e54f8785b4' -H "Content-Type: application/json" localhost:8000/api/adv/inventory
printf '\n'
