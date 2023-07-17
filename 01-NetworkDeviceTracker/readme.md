# Network Device Status Checker
Provided list of ip's the script will use threads to ping each ip and retrive it status
this health data will be stored into the output.csv files

Vitual Environment
```bash
python -m venv venv && pip install -r requirements.txt1
```

Script Usage
```bash
python main.py -i <input-file> -o <output-file>
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