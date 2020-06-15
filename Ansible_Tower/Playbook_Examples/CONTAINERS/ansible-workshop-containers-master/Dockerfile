FROM registry.access.redhat.com/rhscl/python-27-rhel7:latest

COPY app/ /tmp/src/

USER 0

RUN chown -R 1001:0 /tmp/src

USER 1001

RUN /usr/libexec/s2i/assemble

EXPOSE 5000

CMD ["/usr/libexec/s2i/run"] 