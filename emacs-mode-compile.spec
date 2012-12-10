%define rname mode-compile
%define name emacs-%{rname}
%define version 2.27
%define release %mkrel 14

%define flavor emacs

Summary: Smart command for compiling files according to major-mode
Name: %{name}
Version: %{version}
Release: %{release}
# From the XEmacs source
Source0: %{rname}.el.bz2
Source1: %{name}-autostart.el
License: GPL
Group: Editors
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildRequires: %{flavor}-bin
BuildRequires: perl
BuildArch: noarch

%description
Provide `mode-compile' function as a replacement for the use of
 `compile' command which is very dumb for creating it's compilation
 command (use "make -k" by default).  `mode-compile' is a layer
 above `compile'; Its purpose is mainly to build a smart
 compile-command for `compile' to execute it. This compile-command
 is built according to number of parameters:
  - the major-mode.
  - presence or not of a makefile in current directory.
  - the buffer-file-name and extension.
  - what is in the current buffer (`main' function,"#!/path/shell", ...).
  - and more ...
Most of these parameters are higly customizable through Emacs
Lisp variables (to be set in your .emacs or through Customization
menu).  Running mode-compile after an universal-argument (C-u)
allows remote compilations, user is prompted for a host name to
run the compilation command on.  Another function provided is
`mode-compile-kill' which terminate a running compilation session
launched by `mode-compile'.

%prep
%setup -T -c %{name}-%{version}
bzcat %{SOURCE0} > %{rname}.el

%build
for i in %{flavor};do
$i -batch -q -no-site-file -f batch-byte-compile %{rname}.el 
mv %{rname}.elc $i-%{rname}.elc
done

#Maybe need adjust
perl -n -e 'last if /^\(/;last if /^;;; Code/; print' < %{SOURCE0} > DOCUMENTATION

%install
rm -rf $RPM_BUILD_ROOT

for i in %{flavor};do
install -D -m644 $i-%{rname}.elc %{buildroot}%{_datadir}/${i}/site-lisp/$i-%{rname}.elc
[[ $i = emacs ]] && install -D -m644 %{rname}.el %{buildroot}%{_datadir}/emacs/site-lisp/%{rname}.el
done

install -d %buildroot%{_sysconfdir}/emacs/site-start.d
cat << EOF > %buildroot%{_sysconfdir}/emacs/site-start.d/%{name}.el
%{expand:%(%__cat %{SOURCE1})}
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc DOCUMENTATION
%config(noreplace) /etc/emacs/site-start.d/%{name}.el
%{_datadir}/*/site-lisp/*el*


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 2.27-14mdv2011.0
+ Revision: 618051
- the mass rebuild of 2010.0 packages

* Thu Sep 03 2009 Thierry Vignaud <tv@mandriva.org> 2.27-13mdv2010.0
+ Revision: 428568
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 2.27-12mdv2009.0
+ Revision: 244767
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 2.27-10mdv2008.1
+ Revision: 124575
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot
- bump release
- use %%mkrel
- Import emacs-mode-compile



* Fri Apr 29 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.27-8mdk
- rebuild for new emacs

* Thu Jul 22 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.27-7mdk
- rebuild

* Thu Jun 26 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.27-6mdk
- fix description

* Tue Jan 21 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.27-5mdk
- rebuild for latest emacs

* Fri Jan 17 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.27-4mdk
- rebuild

* Fri Jun 21 2002 Götz Waschk <waschk@linux-mandrake.com> 2.27-3mdk
- fix spelling in description
- buildrequires emacs-bin

* Thu Jun 20 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.27-2mdk 
- fix %%prep, %%install
- Buildarch noarch
- bzip %%{SOURCE0}

* Tue May 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.27-1mdk
- First version.

# end of file
