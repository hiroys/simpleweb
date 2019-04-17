FROM centos:latest
LABEL maintainer "HIROYUKI SEKIGUCHI <hiroys@peeyocho.jp>"

RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y httpd24u httpd24u-devel httpd24u-mod_ssl openssl-devel python36u python36u-pip python36u-devel git2u make gcc
RUN pip3.6 install --upgrade pip
RUN pip3.6 install flask
RUN pip3.6 install psycopg2-binary
RUN pip3.6 install mod_wsgi

ADD httpd_simpleweb.conf /etc/httpd/conf.d/
RUN ln -s /usr/lib64/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so /etc/httpd/modules/mod_wsgi.so
RUN echo "LoadModule wsgi_module modules/mod_wsgi.so" > /etc/httpd/conf.modules.d/10-wsgi.conf
RUN git clone https://github.com/hiroys/simpleweb.git
RUN chmod 755 /simpleweb/index.wsgi

EXPOSE 80
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
