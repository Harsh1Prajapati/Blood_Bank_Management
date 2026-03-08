pipeline {
    // Ye batata hai ki pipeline kisi bhi available agent par chal sakti hai
    agent any

    stages {
        stage('Prepare Workspace') {
            steps {
                // Proper Jenkins way to change directory
                dir('C:\\Deployment\\BloodBank') {
                    bat 'echo Flask > requirements.txt'
                    echo 'Requirements file generated successfully.'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('C:\\Deployment\\BloodBank') {
                    bat 'docker build -t bloodbank-app .'
                    echo 'Docker Image built successfully.'
                }
            }
        }
        
        stage('Deploy to Container') {
            steps {
                dir('C:\\Deployment\\BloodBank') {
                    // Purana container hatao taaki port 5000 free ho jaye (error ignore karega agar nahi hai)
                    catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                        bat 'docker rm -f bloodbank-container'
                    }
                    
                    // Naya container run karo
                    bat 'docker run -d --name bloodbank-container -p 5000:5000 bloodbank-app'
                    echo 'Blood Bank Project is LIVE on Port 5000!'
                }
            }
        }
    }
}
