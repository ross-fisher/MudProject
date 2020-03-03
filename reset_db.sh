heroku restart && heroku pg:reset DATABASE_URL --confirm binary-assassins && heroku run rake db:migrate && heroku run rake db:seed
