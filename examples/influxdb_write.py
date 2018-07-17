from influxdb import InfluxDBClient

#client = InfluxDBClient(host, port, user, password, dbname)
client = InfluxDBClient("localhost", 8086)

client.create_database("plant_monitor")
client.switch_database("plant_monitor")

#client.create_retention_policy('awesome_policy', '3d', 3, default=True)
#client.switch_user(dbuser, dbuser_password)

measurement = {"moisture": 34, "timestamp": "2018-07-17 06:53:06.894367", "temperature": 25.9, "conductivity": 189, "device": "C4:7C:8D:65:BD:76", "light": 1460}
json_body =\
    [
        {
            "measurement": "plant_monitor",
             "fields": measurement
        }
    ]

client.write_points(json_body)
