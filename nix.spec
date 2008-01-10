Summary:	A purely functional package manager
Summary(pl):	Czysto funkcyjny zarządca pakietów
Name:		nix
Version:	0.11
Release:	0.2
License:	GPL v2.1
Group:		Applications/System
Source0:	http://nix.cs.uu.nl/dist/%{name}/%{name}-%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	890c25ac0005ff466683869efc288b67
URL:		http://nix.cs.uu.nl/
BuildRequires:	bzip2-devel
BuildRequires:	db-devel
BuildRequires:	openssl-devel
Provides:	/var/nix/manifests
Provides:	/var/nix/profiles
Requires:	curl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

## %define         filterout_ld    -Wl,--as-needed

%description
Nix is a purely functional package manager. It allows multiple
versions of a package to be installed side-by-side, ensures that
dependency specifications are complete, supports atomic upgrades and
rollbacks, allows non-root users to install software, and has many
other features.

%description -l pl
Nix jest czysto funkcyjnym zarządcą pakietów.  Pozwala na jednoczesną
instalację różnych wersji pakietu, zapewnia kompletność specyfikacji
zależności, umożliwia niepodzielną aktualizację systemu i wycofanie do
poprzedniej wersji, pozwala na instalację oprogramowania przez
użytkowników.  Posiada też wiele innych funkcji.

%package devel
Summary:	Header files for nix
Summary(pl.UTF-8):	Pliki nagłówkowe nixa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for nix

%description devel -l pl.UTF-8
Pliki nagłówkowe nixa


%package emacs-mode
Summary:	Emacs mode for nix expressions
Summary(pl.UTF-8):	Tryb Emacsa dla wyrażeń nix
Group:		Development/Libraries
Requires:	emacs

%description emacs-mode
Emacs mode for nix expressions

%description emacs-mode -l pl.UTF-8
Tryb Emacsa dla wyrażeń nix


%prep
%setup -q

%build

%configure \
    --with-bzip2=/usr \
    --with-bdb=/usr \
    --with-store-dir=/%{name}/store
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{name}/store
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/
mv $RPM_BUILD_ROOT/%{_localstatedir}/%{name}/* $RPM_BUILD_ROOT/%{name}/
rmdir $RPM_BUILD_ROOT/%{_localstatedir}/%{name}
ln -s /%{name} $RPM_BUILD_ROOT/%{_localstatedir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS doc/manual/manual.html doc/manual/figures doc/manual/images
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/corepkgs
%dir %{_datadir}/%{name}/corepkgs/*
%attr(755,root,root) %{_datadir}/%{name}/corepkgs/*/*.pl
%attr(755,root,root) %{_datadir}/%{name}/corepkgs/*/*.sh
%{_datadir}/%{name}/corepkgs/*/*.nix
%{_datadir}/%{name}/log2html
%{_datadir}/%{name}/manual
%attr(755,root,root) %{_libdir}/bsdiff
%attr(755,root,root) %{_libdir}/bspatch
%attr(755,root,root) %{_libdir}/nix-setuid-helper
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.pl
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%{_libdir}/%{name}/*.pm
%{_localstatedir}/log/%{name}
%{_localstatedir}/%{name}/
%{_mandir}/man*/*
/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/nix.conf
%{_sysconfdir}/%{name}/nix.conf.example
%attr(755,root,root) %{_sysconfdir}/profile.d/nix.sh

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}/*.la

%files emacs-mode
%{_datadir}/emacs/site-lisp/*.el