%define hornetquser hornetq
%define hornetqgroup hornetq

Name:		hornetq
Version:	2.3.0.Final
Release:	1%{?dist}
Summary:	HornetQ is an open source project to build a multi-protocol, embeddable, very high performance, clustered, asynchronous messaging system.
Packager:	Ernest Beinrohr <Ernest.Beinrohr@axonpro.sk>

Group:		Java
License:	Apache
URL:		http://www.hornetqsoft.org/
Source0:	http://dist.codehaus.org/hornetq/distributions/%{name}-%{version}-bin.tar.gz
Source1:	hornetq-init-script
Source2:	hornetq-sysconfig
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	java
Requires:	java

%description
What is HornetQ?
    HornetQ is an open source project to build a multi-protocol, embeddable, very high performance, clustered, asynchronous messaging system.
    For answers to more questions about what HornetQ is and what it isn't please visit the FAQs wiki page.
Why use HornetQ? Here are just a few of the reasons:
    100% open source software. HornetQ is licenced using the Apache Software License v2.0 to minimise barriers to adoption.
    HornetQ is designed with usability in mind.
    Written in Java. Runs on any platform with a Java 6+ runtime, that's everything from Windows desktops to IBM mainframes.
    Amazing performance. Our class beating high performance journal provides persistent messaging performance at rates normally seen for non persistent messaging, our non persistent messaging performance rocks the boat too.
    Full feature set. All the features you'd expect in any serious messaging system, and others you won't find anywhere else.
    Elegant, clean-cut design with minimal third party dependencies. Run HornetQ stand-alone, run it in integrated in your favourite JEE application server, or run it embedded inside your own product. It's up to you.
    Seamless high availability. We provide a HA solution with automatic client failover so you can guarantee zero message loss or duplication in event of server failure.
    Hugely flexible clustering. Create clusters of servers that know how to load balance messages. Link geographically distributed clusters over unreliable connections to form a global network. Configure routing of messages in a highly flexible way.

%prep
rm -rf %{buildroot}
%setup -q 

%build

%pre
getent group %{hornetqgroup} >/dev/null || groupadd -r %{hornetqgroup}
getent passwd %{hornetquser} >/dev/null || \
useradd -r -g %{hornetqgroup} -d %{_javadir}/%{name} -s /bin/bash \
    -c "HornetQ user" %{hornetquser} || :

%post
chkconfig --add %{name}
chkconfig %{name} on

%preun
service %{name} stop
chkconfig %{name} off
chkconfig --del %{name}

%install
install -m 755 -d %{buildroot}/usr/share/doc/%{name}-%{version}
cp -a examples/ %{buildroot}/usr/share/doc/%{name}-%{version}/examples/
cp -a docs/  %{buildroot}/usr/share/doc/%{name}-%{version}/
cp -a licenses/  %{buildroot}/usr/share/doc/%{name}-%{version}/licenses/
install -m 755 -d %{buildroot}/%{_javadir}/%{name}/
cp -a schema lib/ bin/ %{buildroot}/%{_javadir}/%{name}/
install -m 755 -d %{buildroot}/var/lib/%{name}
install -m 755 -d %{buildroot}/%{_initddir}
install -m 755 -d %{buildroot}/etc/sysconfig/
install -m 755 -d %{buildroot}/var/log/%{name}/
install -m 755 -d %{buildroot}/var/run/%{name}/
install -m 755 %{SOURCE1} %{buildroot}/%{_initddir}/%{name}
cp %{SOURCE2} %{buildroot}/etc/sysconfig/%{name}

cp -a config %{buildroot}/etc/%{name}/

ln -s /var/lib/%{name} %{buildroot}%{_javadir}/%{name}/data
ln -s /etc/%{name} %{buildroot}%{_javadir}/%{name}/config
ln -s /var/log/%{name}/     %{buildroot}%{_javadir}/%{name}/logs
ln -s /var/log/%{name}/     %{buildroot}%{_javadir}/%{name}/bin/logs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc /usr/share/doc/%{name}-%{version}
%{_javadir}/%{name}/
%attr(775, %{hornetquser}, %{hornetqgroup}) /var/lib/%{name}
%{_initddir}/%{name}
%config /etc/sysconfig/%{name}
%config /etc/%{name}
%attr(775, %{hornetquser}, %{hornetqgroup}) /var/log/%{name}/
%attr(775, %{hornetquser}, %{hornetqgroup}) /var/run/%{name}/

%changelog
* Thu Sep 11 2013 Ernest Beinrohr <Ernest@Beinrohr.sk> - 2.3.0-1
- Initial RPM release


