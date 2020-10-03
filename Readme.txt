1. Create python3 virtualenv 
      python3 -m install envName
2. Activate venv 
      source envName/bin/activate
3. Install requirements
      Pip3 install -r reqt.txt
4. Start the application (by default it runs on localhost:5000)
      Python3 app.py
5. Hit APIs, where APIs are 
      i. Search Query -  curl -XGET "127.0.0.1:5000/search?query=ipl"  -v
      ii. Get Query -    curl -XGET "127.0.0.1:5000/get_videos?page_num=1&limit=10"
          NOTE : page_num is the page number for pagination and
                 limit is the number of results on a single page


           <Docker>
6. Create docker image
      docker build -t youtube-videos-docker .
7. Creates a container from a given image
      docker run -p 5000:5000 youtube-videos-docker:latest
8. To view the docker image
      docker images
9. To list the containers
      docker container ls
10. To enter inside the container
      docker exec -it <containerId> /bin/sh