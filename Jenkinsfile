pipeline{
    agent any
    stages{
        stage("Run Tests") {
            steps {
                echo "destroy first..."
                sh 'printenv'
                sh 'pwd'
                sh 'echo DATABASE_USER=$DATABASE_USER >> docker/.env'
                sh 'DATABASE_PASSWORD=$DATABASE_PASSWORD >> docker/.env'
                sh 'DATABASE_NAME=$DATABASE_NAME >> docker/.env'
                sh 'DATABASE_HOST=$DATABASE_HOST >> docker/.env'
                sh 'DATABASE_PORT=$DATABASE_PORT >> docker/.env'
                sh 'SECRET_KEY=$SECRET_KEY >> docker/.env'
                sh 'EMAIL_HOST=$EMAIL_HOST >> docker/.env'
                sh 'EMAIL_PORT=$EMAIL_PORT >> docker/.env'
                sh 'EMAIL_HOST_USER=$EMAIL_HOST_USER >> docker/.env'
                sh 'EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD >> docker/.env'
                sh 'make down'
                echo "Starting..."
                sh 'make start'
                // sh 'make run-app-jenkins'
                sh 'make jenkins-tests'
            }
        }

        // stage("Run test") {
        //     steps {
        //         sh 'printenv'
        //         echo "Run tests"
        //         sh 'make jenkins-tests'
        //     }
        // }

        stage("Destroy environment") {
            steps {
                echo "Runnung docker-compose down"
                sh 'make down'
            }
        }
    }
}