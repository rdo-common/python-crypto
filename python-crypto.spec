%global pythonver %(%{__python} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}

Summary:	Cryptography library for Python
Name:		python-crypto
Version:	2.3
Release:	5%{?dist}
# Mostly Public Domain apart from parts of HMAC.py and setup.py, which are Python
License:	Public Domain and Python
Group:		Development/Libraries
URL:		http://www.pycrypto.org/
Source0:	http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-%{version}.tar.gz
Patch0:		python-crypto-2.2-optflags.patch
Patch1:		pycrypto-2.3-lib64.patch
Provides:	pycrypto = %{version}-%{release}
BuildRequires:	python2-devel >= 2.2, gmp-devel >= 4.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot-%(id -nu)

# Don't want provides for python shared objects
%{?filter_provides_in: %filter_provides_in %{python_sitearch}/Crypto/.*\.so}
%{?filter_setup}

%description
Python-crypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

%prep
%setup -n pycrypto-%{version} -q

# Use distribution compiler flags rather than upstream's
%patch0 -p1

# Look in the right place for libgmp
%if "%{_lib}" == "lib64"
%patch1 -p1
%endif

# Remove spurious shellbangs
sed -i -e '\|^#!/usr/local/bin/python| d' lib/Crypto/Util/RFC1751.py

# Fix permissions for debuginfo
chmod -c -x src/_fastmath.c

%build
CFLAGS="%{optflags} -fno-strict-aliasing" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove group write permissions on shared objects
find %{buildroot}%{python_sitearch} -name '*.so' -exec chmod -c g-w {} \;

# See if there's any egg-info
if [ -f %{buildroot}%{python_sitearch}/pycrypto-%{version}-py%{pythonver}.egg-info ]; then
	echo %{python_sitearch}/pycrypto-%{version}-py%{pythonver}.egg-info
fi > egg-info

%check
%{__python} setup.py test

# Benchmark uses os.urandom(), which is available from python 2.4
%if %(%{__python} -c "import sys; print sys.hexversion >= 0x02040000 and 1 or 0" 2>/dev/null || echo 0)
PYTHONPATH=%{buildroot}%{python_sitearch} %{__python} pct-speedtest.py
%endif

%clean
rm -rf %{buildroot}

%files -f egg-info
%defattr(-,root,root,-)
%doc README TODO ACKS ChangeLog LEGAL/ COPYRIGHT Doc/
%{python_sitearch}/Crypto/

%changelog
* Wed May 11 2011 Paul Howarth <paul@city-fan.org> - 2.3-5
- Upstream rolled new tarball with top-level directory restored
- Nobody else likes macros for commands

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 2.3-3
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 David Malcolm <dmalcolm@redhat.com> - 2.3-2
- add "-fno-strict-aliasing" to compilation flags

* Fri Aug 27 2010 Paul Howarth <paul@city-fan.org> - 2.3-1
- Update to 2.3
  - Fix NameError when attempting to use deprecated getRandomNumber() function
  - _slowmath: Compute RSA u parameter when it's not given to RSA.construct;
    this makes _slowmath behave the same as _fastmath in this regard
  - Make RSA.generate raise a more user-friendly exception message when the
    user tries to generate a bogus-length key
- Add -c option to %%setup because upstream tarball has dropped the top-level
  directory
- Run benchmark as part of %%check if we have python 2.4 or later
- BR: python2-devel rather than just python-devel
- Add patch to make sure we can find libgmp in 64-bit multilib environments

* Tue Aug  3 2010 Paul Howarth <paul@city-fan.org> - 2.2-1
- Update to 2.2
  - Deprecated Crypto.Util.number.getRandomNumber()
  - It's been replaced by getRandomNBitInteger and getRandomInteger
  - Better isPrime() and getPrime() implementations
  - getStrongPrime() implementation for generating RSA primes
  - Support for importing and exporting RSA keys in DER and PEM format
  - Fix PyCrypto when floor division (python -Qnew) is enabled
  - When building using gcc, use -std=c99 for compilation
- Update optflags patch

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Feb 16 2010 Paul Howarth <paul@city-fan.org> - 2.1.0-1
- Update to 2.1.0 (see ChangeLog for details)
- Remove patches (no longer needed)
- Use new upstream URLs
- Upstream has replaced LICENSE with LEGAL/ and COPYRIGHT
- Clarify that license is mostly Public Domain, partly Python
- Add %%check section and run the test suite in it
- Remove upstream's fiddling with compiler optimization flags so we get
  usable debuginfo
- Filter out unwanted provides for python shared objects
- Tidy up egg-info handling
- Simplify %%files list
- Pacify rpmlint as much as is reasonable
- Add dist tag

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-17
- Use patches in upstream git to fix #484473

* Fri Feb 13 2009 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-16.1
- add patch to fix #485298 / CVE-2009-0544

* Sat Feb 7 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-15.1
- Oops, actually apply the patch
- Modify patch so modules remain compatible with PEP 247

* Sat Feb 7 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-15
- Add patch to hashlib instead of deprecated md5 and sha modules (#484473)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.1-14.1
- Rebuild for Python 2.6

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-13
- provide pycrypto

* Sat Feb 09 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-12
- rebuilt

* Fri Jan 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-11
- egg-info file in python_sitearch and not in python_sitelib

* Fri Jan 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-10
- ship egg-file

* Tue Aug 21 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-9
- Remove the old and outdated python-abi hack

* Fri Aug 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- Update License field due to the "Licensing guidelines changes"

* Mon Jun 04 2007 David Woodhouse <dwmw2@infradead.org> - 2.0.1-8
- Fix libdir handling so it works on more arches than x86_64

* Wed Apr 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-7
- Fix typo

* Wed Apr 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-6
- Remove dist
- rebuild, because the older version was much bigger, as it was build when
  distutils was doing static links of libpython

* Sat Dec 09 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-5
- Rebuild for python 2.5

* Thu Sep 07 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-4
- Don't ghost pyo files (#205408)

* Tue Aug 29 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-3
- Rebuild for Fedora Extras 6

* Mon Feb 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-2
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

