Commands to run the server and clients.

## Part1:

    Backend:
        Catalog:
            python3 app.py
        Order:
            CATALOG_HOST=127.0.0.1 python3 app.py
    
    Frontend:
        CATALOG_HOST=127.0.0.1 ORDER_HOST=127.0.0.1 python3 app.py 

    Client:
        python3 client.py
            Options:
                --probability (optional, default is 0.5)
                    probability
            Example: 
                python3 client.py --probability=0.9
            
## Part2:

    Building images (before building images please cd to the root folder of this repo)
        Catalog:
            docker build -t catalog -f Dockerfile.catalog .
        Order:
            docker build -t order -f Dockerfile.order .
        Frontend:
            docker build -t frontend -f Dockerfile.frontend .
        
        Alternatively, we can build the docker images using the build.sh script in the root folder
            bash build.sh
        
    Running the service using docker
        we have included a bash script to run the docker images without having to provide the ips of containers manually. The script automatically does that. On running the script, it will build the images and spawns the each service one by one by passing environment variables if any required.

        command to run:
            bash build_and_run.sh
    
    Deploying Our Application:
        docker-compose up -d
    
    To shutdown our application:
        docker-compose down