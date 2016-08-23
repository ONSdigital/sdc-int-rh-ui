Respondent Home Ruby Web Application
====================================

This Ruby [Sinatra](http://www.sinatrarb.com/) application is the user interface for the Respondent Home product. It allows users to validate their Internet Access Code (IAC) and forwards
them to the [ONS eQ Survey Runner](https://github.com/ONSdigital/eq-survey-runner) upon successful validation.

Prerequisites
-------------

The application's `config.yml` configuration file references the Java web services using `collect-server` and `eq-server` names that need to be present in your hosts file. Install the RubyGems the application depends on by running `bundle install`.

Running
-------

To run this project in development using its [Rackup](http://rack.github.io/) file use:

  `bundle exec rackup config.ru` (the `config.ru` may be omitted as Rack looks for this file by default)

and access using [http://localhost:9292](http://localhost:9292)

Running Using the Mock Backend
------------------------------

This project includes a Sinatra application that provide a mock version of the Internet Access Code web service. To run it, edit your hosts file so that `collect-server` uses 127.0.0.1. Then run:

  `./run.sh` from within the `mock` directory. This is a shell script that starts the mock web service in the background. Use Ctrl + C to terminate it. The output from the background process is written to `mock/nohup.out`. This file can be deleted if not required.

Start the user interface normally as described above. Use `hhrc zv2b` as a test IAC that is no longer valid because the questionnaire has already been submitted. Use `lx6k 5z6m` as a valid test IAC.