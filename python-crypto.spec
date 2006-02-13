%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	Cryptography library for Python
Name:		python-crypto
Version:	2.0.1
Release:	2%{?dist}
License:	Python License (CNRI Python License)
Group:		Development/Libraries
URL:		http://www.amk.ca/python/code/crypto.html
Source:		http://www.amk.ca/files/python/crypto/pycrypto-2.0.1.tar.gz
Patch0:		%{name}-x86_64-buildfix.patch
BuildRequires:	python >= 2.2
BuildRequires:	python-devel >= 2.2
BuildRequires:	gmp-devel >= 4.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot-%(%{__id_u} -n)
Requires:	python-abi = %(%{__python} -c "import sys ; print sys.version[:3]")

%description
Python-crypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, IDEA, RSA, ElGamal,
etc.).


%prep
%setup -n pycrypto-%{version} -q
%ifarch x86_64
%patch0 -b .patch0
%endif


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find -name "*.py"|xargs %{__perl} -pi -e "s:/usr/local/bin/python:%{__python}:"


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README TODO ACKS ChangeLog LICENSE Doc
%{python_sitearch}/Crypto/*.py
%{python_sitearch}/Crypto/*.pyc
%ghost %{python_sitearch}/Crypto/*.pyo
%{python_sitearch}/Crypto/Cipher/*.so
%{python_sitearch}/Crypto/Cipher/*.py
%{python_sitearch}/Crypto/Cipher/*.pyc
%ghost %{python_sitearch}/Crypto/Cipher/*.pyo
%{python_sitearch}/Crypto/Hash/*.so
%{python_sitearch}/Crypto/Hash/*.py
%{python_sitearch}/Crypto/Hash/*.pyc
%ghost %{python_sitearch}/Crypto/Hash/*.pyo
%{python_sitearch}/Crypto/Protocol/*.py
%{python_sitearch}/Crypto/Protocol/*.pyc
%ghost %{python_sitearch}/Crypto/Protocol/*.pyo
%{python_sitearch}/Crypto/PublicKey/*.so
%{python_sitearch}/Crypto/PublicKey/*.py
%{python_sitearch}/Crypto/PublicKey/*.pyc
%ghost %{python_sitearch}/Crypto/PublicKey/*.pyo
%{python_sitearch}/Crypto/Util/*.py
%{python_sitearch}/Crypto/Util/*.pyc
%ghost %{python_sitearch}/Crypto/Util/*.pyo
%dir %{python_sitearch}/Crypto
%dir %{python_sitearch}/Crypto/Cipher/
%dir %{python_sitearch}/Crypto/Hash/
%dir %{python_sitearch}/Crypto/Protocol/
%dir %{python_sitearch}/Crypto/PublicKey/
%dir %{python_sitearch}/Crypto/Util/


%changelog
* Mon Feb 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info>
- Rebuild for Fedora Extras 5

* Wed Aug 17 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0.1-1
- Update to 2.0.1
- Use Dist
- Drop python-crypto-64bit-unclean.patch, similar patch was applied 
  upstream

* Thu May 05 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-4
- add python-crypto-64bit-unclean.patch (#156173)

* Mon Mar 21 2005 Seth Vidal <skvidal at phy.duke.edu> - 0:2.0-3
- iterate release for build on python 2.4 based systems

* Sat Dec 18 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-2
- Fix build on x86_64: use python_sitearch for files and patch source
  to find gmp

* Thu Aug 26 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-0.fdr.1
- Update to 2.00

* Fri Aug 13 2004 Ville Skytta <ville.skytta at iki.fi> - 0:1.9-0.fdr.6.a6
- Don't use get_python_version(), it's available in Python >= 2.3 only.

* Thu Aug 12 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.5.a6
- Own dir python_sitearch/Crypto/

* Wed Aug 11 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.4.a6
- Match python spec template more

* Sat Jul 17 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.3.a6
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

