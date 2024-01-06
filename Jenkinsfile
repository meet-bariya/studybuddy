pipeline{
    agent { label 'alabasta' }

    stages{
        stage('docker container setup'){
            steps{
                sh '''
                docker-compose down
                docker-compose up --build &
                '''
            }
        }
    }
}