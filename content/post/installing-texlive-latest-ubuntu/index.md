---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Installing Texlive Latest Version (Texlive-2021) on Ubuntu-20.04/18.04"
subtitle: ""
summary: ""
authors: ["Md Fahim Sikder"]
tags: ["Texlive", "Ubuntu", "Latex", "Installation", "Latest", "Texlive-2021"]
categories: ["Tutorial", "Blog Post"]
date: 2021-10-01T10:29:54+02:00
lastmod: 2021-10-01T10:29:54+02:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: "Image Source: google"
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

Hello there! In this tutorial, we will learn how to install the latest version of texlive in the ubuntu system! Generally, Ubuntu 20.04 / 18.04 only install Texlive-version-2019 from the local repository! But the Texlive current version is 2021! So, a lot happened in these updates. So, we need to install the 2021 version from the source! But before we do that, we have to uninstall any existing Texlive installation.

### Uninstalling existing Texlive

Use the following command from the terminal to remove the existing installation of Texlive [3].

```console
$ sudo apt-get purge texlive*

$ sudo rm -rf /usr/local/texlive/*

$ rm -rf ~/.texlive*

$ sudo rm -rf /usr/local/share/texmf

$ sudo rm -rf /var/lib/texmf

$ sudo rm -rf /etc/texmf

$ sudo apt-get remove tex-common --purge

$ rm -rf ~/.texlive
```
These commands should remove delete any existing texlive installation.

### Installing Texlive-2021 

Now it's time for install the Texlive latest version! But first, we have to install some dependency [2]! 

```console
$ sudo apt install wget perl-tk
```

We need to get the official installer for Texlive. We can do that by using the following commands:

```console
$ wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
$ tar -xzf install-tl-unx.tar.gz
$ cd install-tl-****
```

Here, **** means the version of the installer! Replace the **** according to your downloaded filename. After changing the directory to the downloaded folder, run the installer by using:

```console
$ sudo ./install-tl
```

Installation of the latest version of the texlive should start. After the installation, we need to add the installation path with variables to the `.bashrc` file.

```console
$ sudo vim ~/.bashrc
```

Add the following variables to the file:

```console
export PATH=/usr/local/texlive/2021/bin/x86_64-linux${PATH:+:${PATH}}
export INFOPATH=/usr/local/texlive/2021/texmf-dist/doc/info${INFOPATH:+:${INFOPATH}}
export MANPATH=/usr/local/texlive/2021/texmf-dist/doc/man${MANPATH:+:${MANPATH}}
```

After this, texlive should be installed in the system. We can check it by typing `which tex` in the terminal. It should return the path where texlive is installed! Now we have to make sure that Ubuntu thinks we have installed texlive. We can do that by installing the `equivs` package!

```console
$ sudo apt install equivs --no-install-recommends freeglut3
$ wget -O debian-equivs-2021-ex.txt https://www.tug.org/texlive/files/debian-equivs-2021-ex.txt
```

We are using the `debian-equivs-2021-ex.txt` file to build a `.deb` file to install the necessary packages. To build the file and install it follow this:

```console
$ equivs-build debian-equivs-2021-ex.txt
$ sudo dpkg -i texlive-local_2021.99999999-1_all.deb
$ sudo apt install -f
```

After this, Texlive should be working just fine in Ubuntu! 

Enjoy!

### Common Issues in Installation

#### Installing Packages Using Texlive Manager (tlmgr)

If we need to install / update packages in our texlive installations, we can use the `Texlive manager (tlmgr)`. We can open the `tlmgr` by typing the following in the terminal:

```console
$ sudo tlmgr --gui
```
But sometimes, it can give the error, such as: `tlmgr: command not found`. If this happens, do the following to open the texlive manager [2]:

```console
$ sudo env PATH="$PATH" tlmgr --gui
```
Now, it should work!

### Reference

1. [Texlive Official Guide 2021](https://www.tug.org/texlive/doc/texlive-en/texlive-en.pdf)
2. [Post about installing Texlive: Answer Section](https://tex.stackexchange.com/questions/1092/how-to-install-vanilla-texlive-on-debian-or-ubuntu)
3. [Post about removing Texlive: Answer Section](https://tex.stackexchange.com/questions/95483/how-to-remove-everything-related-to-tex-live-for-fresh-install-on-ubuntu)