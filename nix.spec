# TODO: json-schema-checks under tests bcond? (BR: jv from jsonschema)
#
# Conditional build:
%bcond_with	s3	# S3 AWS auth support

Summary:	A purely functional package manager
Summary(pl.UTF-8):	Czysto funkcyjny zarządca pakietów
Name:		nix
Version:	2.35.2
Release:	0.1
License:	LGPL v2.1+
Group:		Applications/System
#Source0Download: https://github.com/NixOS/nix/tags
Source0:	https://github.com/NixOS/nix/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0a03af3b164ead26aeff9cd431de6a8f
Patch1:		%{name}-paths.patch
URL:		https://nixos.org/nix/
%{?with_s3:BuildRequires:	aws-c-auth-devel}
%{?with_s3:BuildRequires:	aws-c-common-devel}
%{?with_s3:BuildRequires:	aws-crt-cpp-devel}
BuildRequires:	bison
BuildRequires:	blake3-devel >= 1.8.2
BuildRequires:	boost-devel >= 1.66
BuildRequires:	bzip2-devel
%{?with_perl:BuildRequires:	curl}
BuildRequires:	curl-devel >= 8.17.0
BuildRequires:	doxygen
# or readline with -Dlibcmd:readline-flavor=readline
BuildRequires:	editline-devel >= 1.15.2
BuildRequires:	flex
BuildRequires:	gc-devel
BuildRequires:	gmock-devel
BuildRequires:	graphviz
BuildRequires:	gtest-devel
BuildRequires:	jq
BuildRequires:	libarchive-devel >= 3.1.2
%ifarch %{arm} ppc
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libbrotli-devel
%ifarch %{x8664} x32
BuildRequires:	libcpuid-devel >= 0.7.0
%endif
BuildRequires:	libgit2-devel >= 1.9
BuildRequires:	libseccomp-devel >= 2.5.5
BuildRequires:	libsodium-devel
BuildRequires:	libstdc++-devel >= 6:11
BuildRequires:	llvm-devel >= 16
BuildRequires:	lowdown-devel >= 0.9.0
BuildRequires:	lsof
BuildRequires:	mdbook
BuildRequires:	mdbook-linkcheck
BuildRequires:	meson >= 1.8
BuildRequires:	ninja >= 1.5
BuildRequires:	nlohmann-json-devel >= 3.12
BuildRequires:	openssl-devel >= 1.1.1
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-json-schema-for-humans
# with gtest support and .pc files
BuildRequires:	rapidcheck-devel >= 0-0.20231204
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.720
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	sqlite3-devel >= 3.6.19
BuildRequires:	toml11 >= 3.7.0
BuildRequires:	zstd-devel >= 1.4.0
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Provides:	/var/nix/manifests
Provides:	/var/nix/profiles
Obsoletes:	nix-emacs-mode < 2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		nixdir		/var/lib/nix

# uses `assert(false)` under default switch conditions
%define		filterout_cpp	-DNDEBUG

# non-function _ZN3nix4unix14interruptCheckE symbol in libnixutil
%define		skip_post_check_so	libnixcmd.so.* libnixexpr.so.* libnixfetchers.so.* libnixmain.so.* libnixstore.so.* 

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
Requires:	blake3%{?_isa} >= 1.8.2
Requires:	curl-libs%{?_isa} >= 8.17.0
Requires:	editline%{?_isa} >= 1.15.2
Requires:	libarchive%{?_isa} >= 3.1.2
%ifarch %{x8664} x32
Requires:	libcpuid%{?_isa} >= 0.7.0
%endif
Requires:	libgit2%{?_isa} >= 1.9
Requires:	libseccomp%{?_isa} >= 2.5.5
Requires:	lowdown%{?_isa} >= 0.9.0
Requires:	openssl%{?_isa} >= 1.1.1
Requires:	sqlite3-libs%{?_isa} >= 3.6.19
Requires:	zstd%{?_isa} >= 1.4.0

%description libs
Nix libraries.

%description libs -l pl.UTF-8
Biblioteki Niksa.

%package devel
Summary:	Header files for Nix
Summary(pl.UTF-8):	Pliki nagłówkowe Niksa
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
%if %{with s3}
Requires:	aws-crt-cpp-devel%{?_isa}
%endif
Requires:	blake3-devel%{?_isa} >= 1.8.2
Requires:	boost-devel%{?_isa} >= 1.66
Requires:	curl-devel%{?_isa} >= 8.17.0
Requires:	editline-devel%{?_isa} >= 1.15.2
Requires:	gc-devel%{?_isa}
Requires:	libarchive-devel%{?_isa} >= 3.1.2
Requires:	libbrotli-devel%{?_isa}
%ifarch %{x8664} x32
Requires:	libcpuid-devel%{?_isa} >= 0.7.0
%endif
Requires:	libgit2-devel%{?_isa} >= 1.9
Requires:	libseccomp-devel%{?_isa} >= 2.5.5
Requires:	libsodium-devel%{?_isa}
Requires:	libstdc++-devel%{?_isa} >= 6:11
Requires:	lowdown-devel%{?_isa} >= 0.9.0
Requires:	nlohmann-json-devel%{?_isa} >= 3.12
Requires:	openssl-devel%{?_isa} >= 1.1.1
Requires:	sqlite3-devel%{?_isa} >= 3.6.19
Requires:	zstd-devel%{?_isa} >= 1.4.0

%description devel
Header files for Nix.

%description devel -l pl.UTF-8
Pliki nagłówkowe Niksa.

%package static
Summary:	Static Nix libraries
Summary(pl.UTF-8):	Statyczne biblioteki Niksa
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static Nix libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Niksa.

%package test-libs
Summary:	Nix test libraries
Summary(pl.UTF-8):	Biblioteki testowe Niksa
Group:		Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description test-libs
Nix test libraries.

%description test-libs -l pl.UTF-8
Biblioteki testowe Niksa.

%package test-devel
Summary:	Development files for Nix test libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek testowych Niksa
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-test-libs%{?_isa} = %{version}-%{release}
# libLLVM for nix-clang-tidy plugin
Requires:	llvm-devel%{?_isa} >= 16
Requires:	rapidcheck-devel%{?_isa} >= 0-0.20231204
Requires:	gtest-devel%{?_isa}

%description test-devel
Development files for Nix test libraries.

%description test-devel -l pl.UTF-8
Pliki programistyczne bibliotek testowych Niksa.

%package test-static
Summary:	Static Nix test libraries
Summary(pl.UTF-8):	Statyczne biblioteki testowe Niksa
Group:		Development/Libraries
Requires:	%{name}-test-devel%{?_isa} = %{version}-%{release}

%description test-static
Static Nix test libraries.

%description test-static -l pl.UTF-8
Statyczne biblioteki testowe Niksa.

%package apidocs
Summary:	API documentation for Nix
Summary(pl.UTF-8):	Dokumentacja API Niksa
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Nix.

%description apidocs -l pl.UTF-8
Dokumentacja API Niksa.

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
%patch -P1 -p1

%build
%meson \
	--localstatedir=%{nixdir}/var \
	-Ddoc-gen=true \
	-Djson-schema-checks=false \
	-Dlibcmd:markdown=enabled \
	-Dlibexpr:gc=enabled \
	-Dlibstore:log-dir=%{nixdir}/var/log/nix \
	-Dlibstore:s3-aws-auth=%{__enabled_disabled s3} \
	-Dlibstore:seccomp-sandboxing=enabled \
	-Dlibstore:store-dir=%{nixdir}/store \
%ifarch %{x8664}
	-Dlibutil:cpuid=enabled \
%endif
	-Dnix:mimalloc=disabled \
	-Dnix:profile-dir=/etc/profile.d

# -Dplugin-c-api=true ?

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

install -d $RPM_BUILD_ROOT%{nixdir}/{store,var/nix/{gcroots,profiles}/per-user}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	test-libs -p /sbin/ldconfig
%postun	test-libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/nix*
%attr(755,root,root) %{_libexecdir}/nix-nswrapper
%dir %{_libexecdir}/nix
%attr(755,root,root) %{_libexecdir}/nix/build-remote
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
%{_mandir}/man5/nix-profiles.5*
%{_mandir}/man8/nix-daemon.8*
%dir %{_docdir}/nix
%{_docdir}/nix/manual

%files libs
%defattr(644,root,root,755)
%{_libdir}/libnixcmd.so.*.*.*
%{_libdir}/libnixexpr.so.*.*.*
%{_libdir}/libnixexprc.so.*.*.*
%{_libdir}/libnixfetchers.so.*.*.*
%{_libdir}/libnixfetchersc.so.*.*.*
%{_libdir}/libnixflake.so.*.*.*
%{_libdir}/libnixflakec.so.*.*.*
%{_libdir}/libnixmain.so.*.*.*
%{_libdir}/libnixmainc.so.*.*.*
%{_libdir}/libnixstore.so.*.*.*
%{_libdir}/libnixstorec.so.*.*.*
%{_libdir}/libnixutil.so.*.*.*
%{_libdir}/libnixutilc.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libnixcmd.so
%{_libdir}/libnixexpr.so
%{_libdir}/libnixexprc.so
%{_libdir}/libnixfetchers.so
%{_libdir}/libnixfetchersc.so
%{_libdir}/libnixflake.so
%{_libdir}/libnixflakec.so
%{_libdir}/libnixmain.so
%{_libdir}/libnixmainc.so
%{_libdir}/libnixstore.so
%{_libdir}/libnixstorec.so
%{_libdir}/libnixutil.so
%{_libdir}/libnixutilc.so
%{_includedir}/nix
%exclude %{_includedir}/nix/expr/tests
%exclude %{_includedir}/nix/store/tests
%exclude %{_includedir}/nix/util/tests
%{_includedir}/nix_api_store
%{_includedir}/nix_api_*.h
%{_includedir}/nix_api_*.hh
%{_pkgconfigdir}/nix-cmd.pc
%{_pkgconfigdir}/nix-expr.pc
%{_pkgconfigdir}/nix-expr-c.pc
%{_pkgconfigdir}/nix-fetchers.pc
%{_pkgconfigdir}/nix-fetchers-c.pc
%{_pkgconfigdir}/nix-flake.pc
%{_pkgconfigdir}/nix-flake-c.pc
%{_pkgconfigdir}/nix-main.pc
%{_pkgconfigdir}/nix-main-c.pc
%{_pkgconfigdir}/nix-store.pc
%{_pkgconfigdir}/nix-store-c.pc
%{_pkgconfigdir}/nix-util.pc
%{_pkgconfigdir}/nix-util-c.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnixcmd.a
%{_libdir}/libnixexpr.a
%{_libdir}/libnixexprc.a
%{_libdir}/libnixfetchers.a
%{_libdir}/libnixfetchersc.a
%{_libdir}/libnixflake.a
%{_libdir}/libnixflakec.a
%{_libdir}/libnixmain.a
%{_libdir}/libnixmainc.a
%{_libdir}/libnixstore.a
%{_libdir}/libnixstorec.a
%{_libdir}/libnixutil.a
%{_libdir}/libnixutilc.a

%files test-libs
%defattr(644,root,root,755)
%{_libdir}/libnix-clang-tidy.so
%{_libdir}/libnix-expr-test-support.so.*.*.*
%{_libdir}/libnix-store-test-support.so.*.*.*
%{_libdir}/libnix-util-test-support.so.*.*.*

%files test-devel
%defattr(644,root,root,755)
%{_libdir}/libnix-expr-test-support.so
%{_libdir}/libnix-store-test-support.so
%{_libdir}/libnix-util-test-support.so
%{_includedir}/nix/expr/tests
%{_includedir}/nix/store/tests
%{_includedir}/nix/util/tests
%{_pkgconfigdir}/nix-clang-tidy.pc
%{_pkgconfigdir}/nix-expr-test-support.pc
%{_pkgconfigdir}/nix-store-test-support.pc
%{_pkgconfigdir}/nix-util-test-support.pc

%files test-static
%defattr(644,root,root,755)
%{_libdir}/libnix-expr-test-support.a
%{_libdir}/libnix-store-test-support.a
%{_libdir}/libnix-util-test-support.a

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/nix/external-api
%{_docdir}/nix/internal-api

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
