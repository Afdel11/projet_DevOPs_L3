pipeline {
  agent any

  stages {
    stage("Cloner le code depuis le depot Github"){
      steps{
        checkout scm
      }
    }

    stage("Construire les conteneurs a l'aide de Docker"){
      steps{
        powershell 'docker-compose build'
      }
    }

    stage("Déployer l’application localement à l’aide de docker-compose"){
      steps{
        powershell 'docker-compose up -d'
      }
    } 
  }

  post{
    success{
      echo "Pipeline execute avec succes"
    }
    failure{
      echo "L'execution du pipeline a echoue"
    }
  }
}
