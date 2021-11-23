pipeline{
    agent any
    stages{
        stage("build image") {
            steps {
                echo "Starting...1"
                sh 'make start'
                echo "Run tests"
                sh 'make tests'
            }
        }
    }
}