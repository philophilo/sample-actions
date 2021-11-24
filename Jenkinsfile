pipeline{
    agent any
    stages{
        stage("Setup docker") {
            steps {
                echo "Starting..."
                sh 'make start'
            }
        }

        stage("Run test") {
            steps {
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