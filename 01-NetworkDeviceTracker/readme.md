# Network Device Status Monitoring Tool
Provided list of ip's the script will use threads to ping each ip and retrive it status
this health data will be stored into the output.csv files

### Virtual Environment
```bash
python -m venv venv && pip install -r requirements.txt1
```

### Script Usage

Display Help
```bash 
python ping-monitor -h
 ```

Custom Input and Ouput file
(defaults:  -i device_data.json -o ouput.csv)
writes logs to output.csv for all the device in input.json
```bash 
python ping-monitor -i <input-file> -o <output-file>
 ```

List Device
```bash 
python ping-monitor list-devices
 ```

Add Device
```bash 
python ping-monitor add-device
 ```

Delete Device
```bash 
python ping-monitor delete-device <id:int>
 ```

Edit Device
```bash 
python ping-monitor edit-device <id:int>
 ```




Device Data _sample.json_
```json
[
	{
		"id": 1,
		"name": "Device 1",
		"ip":"192.168.0.1",
		
	}
]
```
Output Format
```markdown
device_id | device_name | timestamp           | status
1         | dummy 1     | 2023-07-11 11:42:34 | 1
2         | dummy 2     | 2023-07-11 11:42:34 | 0
```