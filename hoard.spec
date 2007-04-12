%define name hoard
%define version 3.5.1
%define underversion %(version=%version;echo ${version//./_})
%define nodotsversion %(version=%version;echo ${version//./})

%define libname %mklibname %name

Name:		%name
Version:	3.6
Release:	%mkrel 1
Group:		System/Libraries
License:	GPL
URL:		http://www.hoard.org/
Source:		http://www.cs.umass.edu/%7Eemery/hoard/hoard-%{version}/%{name}-%{nodotsversion}.tar.gz
Summary:	A fast, scalable, and memory-efficient memory allocator
BuildRoot:	%{_tmppath}/%{name}-root

%description
The Hoard memory allocator is a fast, scalable, and memory-efficient memory
allocator. It runs on a variety of platforms, including Linux, Solaris, and
Windows. Hoard is a drop-in replacement for malloc() that can  dramatically
improve application performance, especially for multithreaded programs running
on multiprocessors. No change to your source is necessary. Just link it in or
set just one environment variable, e.g.:

LD_PRELOAD="%{_libdir}/libhoard.so:%{_libdir}/libdl.so"

This package mostly contains the documentation

%package -n %libname
Group:		System/Libraries
License:	GPL
Summary:	A fast, scalable, and memory-efficient memory allocator

%description -n %libname
The Hoard memory allocator is a fast, scalable, and memory-efficient memory
allocator. It runs on a variety of platforms, including Linux, Solaris, and
Windows. Hoard is a drop-in replacement for malloc() that can  dramatically
improve application performance, especially for multithreaded programs running
on multiprocessors. No change to your source is necessary. Just link it in or
set just one environment variable, e.g.:

LD_PRELOAD="%{_libdir}/libhoard.so:%{_libdir}/libdl.so"



%prep
%setup -q -n hoard-%{nodotsversion}
cp -pf src/Makefile{,.orig}
perl -pi -e 's/-O/-fPIC -O/g;s/-static//g;s/-pipe//g' src/Makefile
# on non-i586 we assume that the default arch is sufficient
%ifnarch i586
perl -pi -e 's/-march=pentiumpro //g;s/ -malign-double//g' src/Makefile
%endif

%build
pushd src
make generic-gcc

%clean
rm -Rf %{buildroot}

%install
rm -Rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}
install src/libhoard.so %{buildroot}/%{_libdir}

%files
%defattr(0644,root,root,755)
%doc doc NEWS README THANKS

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libhoard.so


