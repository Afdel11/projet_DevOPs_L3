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
        sh 'docker-compose build'
      }
    }

    stage("Déployer l’application localement à l’aide de docker-compose"){
      steps{
        sh 'docker-compose up -d'
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
