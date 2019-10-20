## Code description
1. simulate_streaming_logs.py converts logs in the steam_source to real-time logs which can be used to test dynamic session generation code in the java workspace. 
2. Steaming log monitor file: incubator-sdap-mudrod\core\src\main\java\org\apache\sdap\mudrod\weblog\streaming\LogMonitor.java
3. In the stream source file, we can only provide sample logs since logs contains senstive information, e.g. user email. In the sample log, IP filed in HTTP and FTP and email in FTP are manually changed to avoid disclosure of user information.

