#
# Conditional build:
%bcond_with	perl	# Perl module (needs update: uses C++11, while main libs need C++17 now)

Summary:	A purely functional package manager
Summary(pl.UTF-8):	Czysto funkcyjny zarządca pakietów
Name:		nix
Version:	2.14.1
Release:	0.1
License:	LGPL v2.1+
Group:		Applications/System
#Source0Download: https://github.com/NixOS/nix/tags
Source0:	https://github.com/NixOS/nix/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a132c8cf9a246c6ceecb8625163beff0
Patch0:		%{name}-sh.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-ldflags.patch
Patch3:		%{name}-link.patch
Patch4:		%{name}-fix_nix_DIR_in_doc_local_mk.patch
URL:		https://nixos.org/nix/
BuildRequires:	autoconf >= 2.50
BuildRequires:	autoconf-archive
BuildRequires:	automake
# TODO: aws-sdk-cpp/aws-cpp-sdk-s3 (aws/s3/S3Client.h)
BuildRequires:	bison
BuildRequires:	boost-devel >= 1.66
BuildRequires:	bzip2-devel
%{?with_perl:BuildRequires:	curl}
BuildRequires:	curl-devel
BuildRequires:	editline-devel >= 1.15.2
BuildRequires:	flex
BuildRequires:	gc-devel
BuildRequires:	graphviz
BuildRequires:	gtest-devel
BuildRequires:	jq
BuildRequires:	libarchive-devel >= 3.1.2
BuildRequires:	libbrotli-devel
BuildRequires:	libseccomp-devel
BuildRequires:	libsodium-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	lowdown-devel >= 0.9.0
BuildRequires:	lsof
BuildRequires:	mdbook
BuildRequires:	mdbook-linkcheck
BuildRequires:	nlohmann-json-devel >= 3.10.5-3
BuildRequires:	openssl-devel
# with gtest support
BuildRequires:	rapidcheck-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.720
%if %{with perl}
BuildRequires:	perl-DBI
BuildRequires:	perl-DBD-SQLite
BuildRequires:	perl-base >= 1:5.8.0
%endif
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	sqlite3-devel >= 3.6.19
BuildRequires:	xz-devel
Requires:	%{name}-libs = %{version}-%{release}
Provides:	/var/nix/manifests
Provides:	/var/nix/profiles
Obsoletes:	nix-emacs-mode < 2.3
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

%package -n bash-completion-nix
Summary:	Bash completion for nix commands
Summary(pl.UTF-8):	Dopełnianie parametrów w bashu dla poleceń nix
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-nix
Bash completion for nix commands.

%description -n bash-completion-nix -l pl.UTF-8
Dopełnianie parametrów w bashu dla poleceń nix.

%package -n fish-completion-nix
Summary:	Fish completion for nix commands
Summary(pl.UTF-8):	Dopełnianie parametrów w fishu dla poleceń nix
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-nix
Fish completion for nix commands.

%description -n fish-completion-nix -l pl.UTF-8
Dopełnianie parametrów w fishu dla poleceń nix.

%package -n zsh-completion-nix
Summary:	Zsh completion for nix commands
Summary(pl.UTF-8):	Dopełnianie parametrów w zsh dla poleceń nix
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-nix
Zsh completion for nix commands.

%description -n zsh-completion-nix -l pl.UTF-8
Dopełnianie parametrów w zsh dla poleceń nix.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%configure \
	--localstatedir=%{nixdir}/var \
	--with-store-dir=%{nixdir}/store

# avoid BOOST_LDFLAGS=-L%{_libdir} which causes to link with system nix libraries instead of built ones
%{__make} \
	BOOST_LDFLAGS="" \
	GLOBAL_CXXFLAGS="%{rpmcxxflags} -Wall -include config.h -std=c++17 -I src -fPIC" \
	GLOBAL_LDFLAGS="%{rpmldflags}" \
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
	BOOST_LDFLAGS="" \
	DESTDIR=$RPM_BUILD_ROOT \
	V=1

%if %{with perl}
%{__make} -C perl install \
	DESTDIR=$RPM_BUILD_ROOT \
	V=1
%endif

install -d $RPM_BUILD_ROOT%{nixdir}/{store,var/nix/{gcroots,profiles}/per-user}

%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/nix3-manpages
# dead upstart stuff
%{__rm} -r $RPM_BUILD_ROOT/etc/init

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/nix*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/build-remote
%{systemdunitdir}/nix-daemon.service
%{systemdunitdir}/nix-daemon.socket
%{systemdtmpfilesdir}/nix-daemon.conf
/etc/profile.d/nix.fish
/etc/profile.d/nix.sh
/etc/profile.d/nix-daemon.fish
/etc/profile.d/nix-daemon.sh
%dir %{nixdir}
%attr(1775,root,root) %dir %{nixdir}/store
%dir %{nixdir}/var
%dir %{nixdir}/var/nix
%dir %{nixdir}/var/nix/gcroots
%dir %{nixdir}/var/nix/gcroots/per-user
%dir %{nixdir}/var/nix/profiles
%dir %{nixdir}/var/nix/profiles/per-user
%{_mandir}/man1/nix.1*
%{_mandir}/man1/nix-*.1*
%{_mandir}/man1/nix3-*.1*
%{_mandir}/man5/nix.conf.5*
%{_mandir}/man8/nix-daemon.8*
%dir %{_docdir}/nix
%{_docdir}/nix/manual

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnixcmd.so
%attr(755,root,root) %{_libdir}/libnixexpr.so
%attr(755,root,root) %{_libdir}/libnixfetchers.so
%attr(755,root,root) %{_libdir}/libnixmain.so
%attr(755,root,root) %{_libdir}/libnixstore.so
%attr(755,root,root) %{_libdir}/libnixutil.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/nix
%{_pkgconfigdir}/nix-cmd.pc
%{_pkgconfigdir}/nix-expr.pc
%{_pkgconfigdir}/nix-main.pc
%{_pkgconfigdir}/nix-store.pc

%files -n bash-completion-nix
%defattr(644,root,root,755)
%{bash_compdir}/nix

%files -n fish-completion-nix
%defattr(644,root,root,755)
%{fish_compdir}/nix.fish

%files -n zsh-completion-nix
%defattr(644,root,root,755)
%{zsh_compdir}/_nix
%{zsh_compdir}/run-help-nix
