%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: 	A cryptography library for Python.
Name: 		python-crypto
Version: 	1.9
Epoch:		0
Release: 	0.fdr.6.a6.2
License: 	Python License (CNRI Python License)
Group: 		Development/Libraries
URL: 		http://www.amk.ca/python/code/crypto.html
Source:		http://www.amk.ca/files/python/crypto/pycrypto-1.9a6.tar.gz
BuildRequires:	python >= 0:2.2
BuildRequires:	python-devel >= 0:2.2
BuildRequires:	gmp-devel >= 0:4.1
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot-%(%{__id_u} -n)
Requires:   python-abi = %(%{__python} -c "import sys ; print sys.version[:3]")

%description
Python-crypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, IDEA, RSA, ElGamal,
etc.).

# The pre section.
%prep
%setup -n pycrypto-1.9a6 -q 

# The build section.
%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

# The install section.
%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

find -name "*.py"|xargs %{__perl} -pi -e "s:/usr/local/bin/python:%{__python}:"

# The clean section.
%clean
rm -rf $RPM_BUILD_ROOT

# The files section.
%files 
%defattr(-,root,root,-)
%doc README TODO ACKS ChangeLog LICENSE Doc Demo
%{python_sitelib}/Crypto/*.py
%{python_sitelib}/Crypto/*.pyc
%ghost %{python_sitelib}/Crypto/*.pyo
%{python_sitearch}/Crypto/Cipher/*.so
%{python_sitelib}/Crypto/Cipher/*.py
%{python_sitelib}/Crypto/Cipher/*.pyc
%ghost %{python_sitelib}/Crypto/Cipher/*.pyo
%{python_sitearch}/Crypto/Hash/*.so
%{python_sitelib}/Crypto/Hash/*.py
%{python_sitelib}/Crypto/Hash/*.pyc
%ghost %{python_sitelib}/Crypto/Hash/*.pyo
%{python_sitelib}/Crypto/Protocol/*.py
%{python_sitelib}/Crypto/Protocol/*.pyc
%ghost %{python_sitelib}/Crypto/Protocol/*.pyo
%{python_sitearch}/Crypto/PublicKey/*.so
%{python_sitelib}/Crypto/PublicKey/*.py
%{python_sitelib}/Crypto/PublicKey/*.pyc
%ghost %{python_sitelib}/Crypto/PublicKey/*.pyo
%{python_sitelib}/Crypto/Util/*.py
%{python_sitelib}/Crypto/Util/*.pyc
%ghost %{python_sitelib}/Crypto/Util/*.pyo
%dir %{python_sitelib}/Crypto
%dir %{python_sitelib}/Crypto/Cipher/
%dir %{python_sitelib}/Crypto/Hash/
%dir %{python_sitelib}/Crypto/Protocol/
%dir %{python_sitelib}/Crypto/PublicKey/
%dir %{python_sitelib}/Crypto/Util/

%changelog
* Fri Aug 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.9-0.fdr.6.a6
- Don't use get_python_version(), it's available in Python >= 2.3 only.

* Thu Aug 12 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0.3.2-0.fdr.5.a6
- Own dir python_sitearch/Crypto/

* Wed Aug 11 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0.3.2-0.fdr.4.a6
- Match python spec template more

* Sat Jul 17 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0.3.2-0.fdr.4.a6
- Own _libdir/python/site-packages/Crypto/

* Wed Mar 24 2004 Panu Matilainen <pmatilai@welho.com> 0.3.2-0.fdr.2.a6
- generate .pyo files during install
- require exact version of python used to build the package
- include more docs + demos
- fix dependency on /usr/local/bin/python
- use fedora.us style buildroot
- buildrequires gmp-devel
- use description from README

* Sun Jan 11 2004 Ryan Boder <icanoop@bitwiser.org>  0.3.2-0.fdr.1.a6
- Initial build.

