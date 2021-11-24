pipeline{
    agent any
    stages{
        stage("Run Tests") {
            steps {
                echo "Starting..."
                sh 'make start'
                echo "Run tests"
                sh 'make jenkins-tests'
            }
        }

        stage("Destroy environment") {
            steps {
                echo "Stop containers"
                sh 'make down'
            }
        }
    }
}