#
# Conditional build:
%bcond_with	perl	# Perl module (needs update: uses C++11, while main libs need C++17 now)

Summary:	A purely functional package manager
Summary(pl.UTF-8):	Czysto funkcyjny zarządca pakietów
Name:		nix
Version:	2.3.4
Release:	0.1
License:	LGPL v2.1+
Group:		Applications/System
Source0:	https://nixos.org/releases/nix/%{name}-%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	0d8486cb6622bb53116200d3a3d378ca
Patch0:		%{name}-sh.patch
Patch1:		%{name}-paths.patch
URL:		https://nixos.org/nix/
# aws-sdk-cpp/aws-cpp-sdk-s3 (aws/s3/S3Client.h)
BuildRequires:	boost-devel >= 1.66
BuildRequires:	bzip2-devel
%{?with_perl:BuildRequires:	curl}
BuildRequires:	curl-devel
BuildRequires:	editline-devel >= 1.15.2
BuildRequires:	gc-devel
BuildRequires:	libbrotli-devel
BuildRequires:	libseccomp-devel
BuildRequires:	libsodium-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	openssl-devel
BuildRequires:	sqlite3-devel >= 3.6.19
%if %{with perl}
BuildRequires:	perl-DBI
BuildRequires:	perl-DBD-SQLite
BuildRequires:	perl-base >= 1:5.8.0
%endif
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	nix-emacs-mode
Provides:	/var/nix/manifests
Provides:	/var/nix/profiles
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		nixdir		/var/lib/nix

%description
Nix is a purely functional package manager. It allows multiple
versions of a package to be installed side-by-side, ensures that
dependency specifications are complete, supports atomic upgrades and
rollbacks, allows non-root users to install software, and has many
other features.

%description -l pl.UTF-8
Nix jest czysto funkcyjnym zarządcą pakietów. Pozwala na jednoczesną
instalację różnych wersji pakietu, zapewnia kompletność specyfikacji
zależności, umożliwia niepodzielną aktualizację systemu i wycofanie do
poprzedniej wersji, pozwala na instalację oprogramowania przez
użytkowników. Posiada też wiele innych funkcji.

%package libs
Summary:	Nix libraries
Summary(pl.UTF-8):	Biblioteki Niksa
Group:		Libraries

%description libs
Nix libraries.

%description libs -l pl.UTF-8
Biblioteki Niksa.

%package devel
Summary:	Header files for Nix
Summary(pl.UTF-8):	Pliki nagłówkowe Niksa
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gc-devel
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for Nix.

%description devel -l pl.UTF-8
Pliki nagłówkowe Niksa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%configure \
	--localstatedir=%{nixdir}/var \
	--with-store-dir=%{nixdir}/store

%{__make} \
	V=1

%if %{with perl}
ln -sf nix src/nix/nix-instantiate
topdir=$(pwd)
cd perl
%configure \
	NIX_CFLAGS="-I$topdir/src/libstore -I$topdir/src/libutil" \
	NIX_LIBS="-L$topdir/src/libstore -lnixstore" \
	NIX_INSTANTIATE_PROGRAM="$topdir/src/nix/nix-instantiate"

%{__make} \
	V=1
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with perl}
%{__make} -C perl install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

install -d $RPM_BUILD_ROOT%{nixdir}/{store,var/nix/{gcroots,profiles}/per-user}

# dead upstart stuff
%{__rm} -r $RPM_BUILD_ROOT/etc/init
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/manual

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md doc/manual/{manual.html,figures,images}
%attr(755,root,root) %{_bindir}/nix*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/build-remote
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/corepkgs
%{_datadir}/%{name}/sandbox
%{systemdunitdir}/nix-daemon.service
%{systemdunitdir}/nix-daemon.socket
/etc/profile.d/nix.sh
/etc/profile.d/nix-daemon.sh
%dir %{nixdir}
%attr(1775,root,root) %dir %{nixdir}/store
%dir %{nixdir}/var
%dir %{nixdir}/var/nix
%dir %{nixdir}/var/nix/gcroots
%dir %{nixdir}/var/nix/gcroots/per-user
%dir %{nixdir}/var/nix/profiles
%dir %{nixdir}/var/nix/profiles/per-user
%{_mandir}/man1/nix-*.1*
%{_mandir}/man5/nix.conf.5*
%{_mandir}/man8/nix-daemon.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnixexpr.so
%attr(755,root,root) %{_libdir}/libnixmain.so
%attr(755,root,root) %{_libdir}/libnixstore.so
%attr(755,root,root) %{_libdir}/libnixutil.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/nix
%{_pkgconfigdir}/nix-expr.pc
%{_pkgconfigdir}/nix-main.pc
%{_pkgconfigdir}/nix-store.pc
