FROM ontotext/graphdb:10.8.1
COPY /rdf /root/graphdb-import
# Copy all .ttl files into the same dir
RUN mkdir /root/graphdb-import/all
RUN find /root/graphdb-import/ -type f -print0 | xargs -0 cp -t /root/graphdb-import/all

# Copy template
COPY /database/template.ttl /root/template.ttl
# Create config
RUN mkdir /opt/graphdb/home/conf/
RUN echo graphdb.home.data = /opt/graphdb/home/data > /opt/graphdb/home/conf/graphdb.properties
# Load data into DB with loadrdf
RUN GDB_JAVA_OPTS='-Dgraphdb.home=/opt/graphdb/home' importrdf load -c /root/template.ttl -m parallel /root/graphdb-import/all/*.ttl
