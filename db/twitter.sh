curl "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary" \
-G \
--data-urlencode 'start_key=["melbourne",2021,1,1]' \
--data-urlencode 'end_key=["melbourne",2021,5,31]' \
--data-urlencode 'reduce=false' \
--data-urlencode 'include_docs=true' \
--user "readonly:ween7ighai9gahR6" \
-o ./twitter2021.json