Clone the repository.

Edit config.yaml providing your callsign, password, and a list of stations to monitor.

And then
```
pip install aprslib
pip install pyyaml
pip install flask-restful
sudo apt-get install python-twisted
```
Now edit stationservice.service:
1.  WorkingDirectory should be where you cloned the repository.
1.  Environment should be where your site packages are, and the current working directory.
```
sudo cp stationservice.service /etc/systemd/user/stationservice.service
sudo systemctl daemon-reload
```

Start the service with `sudo systemctl start stationservice.service`.
Stop the service with `sudo systemctl stop stationservice.service`.
