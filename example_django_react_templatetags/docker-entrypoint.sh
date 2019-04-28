#!/bin/bash
# $0 is a script name, $1, $2, $3 etc are passed arguments
# $1 is our command
# Credits: https://rock-it.pl/how-to-write-excellent-dockerfiles/
CMD=$1

setup_django () {
    echo Running migrations
    python manage.py migrate --noinput

    echo Collecting static-files
    python manage.py collectstatic --noinput

}

case "$CMD" in
    "runserver" )
        setup_django

        echo Starting using manage.py runserver
        exec python manage.py runserver 0.0.0.0:8000
        ;;
    * )
        # Run custom command. Thanks to this line we can still use
        # "docker run our_container /bin/bash" and it will work
        exec $CMD ${@:2}
        ;;
esac
