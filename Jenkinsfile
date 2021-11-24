pipeline{
    agent any
    stages{
        stage("Run tests") {
            steps {
                echo "Starting...1"
                sh 'make start'
                echo "Run tests"
                sh 'make jenkins-tests'
            }
        }
    }
}