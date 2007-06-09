Summary:	PHP-based Wiki webapplication
Summary(pl.UTF-8):	Oparta na PHP aplikacja WWW Wiki
Name:		phpwiki
Version:	1.3.12p2
Release:	0.5
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/phpwiki/%{name}-%{version}.tar.gz
# Source0-md5:	e405f9a86f3e341e971250d540971410
Patch0:		%{name}-pear.patch
Patch1:		%{name}-webapps.patch
URL:		http://phpwiki.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php(pcre)
Requires:	php-pear-Cache
Requires:	php-pear-DB
Requires:	php-pear-DB_Pager
Requires:	php-pear-File_Passwd
Requires:	php-pear-PEAR-core
Requires:	webapps
Requires:	webserver(php) >= 4.0.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
PhpWiki is a WikiWikiWeb clone in PHP. A WikiWikiWeb is a site where
anyone can edit the pages through an HTML form. Multiple storage
backends, dynamic hyperlinking, themeable, scriptable by plugins, full
authentication, ACLs.

%description -l pl.UTF-8
PhpWiki to klon WikiWikiWeb napisany w PHP. WikiWikiWeb to serwis, w
którym ktokolwiek może zmieniać strony poprzez formularz HTML.
Dostępne jest wiele backendów do przechowywania danych, dynamiczne
odnośniki, motywy, oskryptowanie poprzez wtyczki, pełne
uwierzytelnienie, listy kontroli dostępu (ACL).

%prep
%setup -q
mv config/config{-dist,}.ini
mv config/phpwiki.spec .
mv config/make-dbhelper.pl .
rm -rf lib/pear
%patch0 -p1
%patch1 -p1

cat > apache.conf <<EOF
Alias /%{_webapp} %{_appdir}
<Directory /%{_appdir}>
	Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},/var/lib/%{name}}

cp -a *.php *.ico *.wsdl wiki $RPM_BUILD_ROOT%{_appdir}
cp -a lib locale pgsrc themes uploads $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc doc/* schemas INSTALL README TODO UPGRADING
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.ini
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/two-level-tlds
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/whitelist
%{_appdir}
%dir %attr(770,root,http) /var/lib/%{name}
