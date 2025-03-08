pipeline {
    agent none
    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
    }
    stages {
        stage('test') {
            // when { branch 'master'; beforeAgent true }
            agent {
                docker {
                    
                    image "$env.POETRY_I3_RUNNER_IMAGE" // py3.11 and py3.12
                    args '--entrypoint=\'\' -u root:root -v /home/tenant/data/spacy/models:/home/tenant/data/spacy/models'
                    reuseNode true
                    label 'postgresql' // runner with 8GB RAM
                    // label 'trigger' // runner with 8GB RAM
                }
            }
            steps {
                sh '''
                echo START;
                date;

                which python3.11;
                                
                poetry env use /usr/bin/python3.11
                poetry remove es_core_news_lg en_core_web_trf de_core_news_lg
                poetry add /home/tenant/data/spacy/models/en_core_web_trf-3.5.0.tar.gz /home/tenant/data/spacy/models/de_core_news_lg-3.5.0.tar.gz /home/tenant/data/spacy/models/es_core_news_lg-3.5.0.tar.gz
                poetry install
                poetry run pytest --full-trace -vvv

                poetry env list --full-path;
               
                date;
                echo END;
                '''
            }
        }
    }
}
