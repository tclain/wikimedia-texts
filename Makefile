all : elastic serve

elastic:
	export JAVA_HOME=$(/usr/libexec/java_home -v 1.7)
	/opt/elasticsearch/bin/elasticsearch -d
stop-elastic:
	ps aux | grep elastic |grep -v grep| awk '{print $2}' | xargs kill	
serve :
	@echo "Serving App"
	@echo "Starting crawling and indexing"
	@echo "Starting web"	
	cd web && python index.py
