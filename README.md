# Todo

* [X]  company

  * [X]  query enabled for searching & sorting
* [X]  user

  * [X]  jwt authentication enabled
* [X]  watchlist

  * [X]  many to many relation
  * [X]  adding company
  * [X]  removing company
* [X]  swagger ( /swagger-ui )
* [X]  celery
* [X]  metrics ( /metrics )

  * [X]  using prometheus client for django
  * [ ]  promethues for kubernetes not created (for pulling metrics from clients)
* [X]  django health checks
* [X]  docker

  * [X]  docker file
  * [X]  docker compose
  * [X]  docker swarm
* [X]  kubernetes

  * [X]  depl for trade app
    * [X]  postgres (stateful)
    * [X]  redis
  * [X]  fluentbit for collecting logs (daemon)
    * [X]  collect logs from pods , containers , application
* [X]  django logging with struct logger for enabling better debugging and  enables fluentbit to collect logs from application
* [X]  CI pipeline (CD pipeline requires real production) | branch rules enabled

  * [X]  (skipped) | some errors faced
    * [ ]  docker push
    * [ ]  docker testing
    * [ ]  docker vulnerability test
  * [X]  job
    * [X]  build
    * [X]  test
    * [X]  code coverage
      * [X]  reports are uploaded & saved successfully
