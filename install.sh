#!/bin/bash

OS="`uname`"
case $OS in
  Linux*)     OS='Linux';;
  FreeBSD*)   OS='FreeBSD';;
  WindowsNT*) OS='Windows';;
  Darwin*)    OS='MacOSX';;
  CYGWIN*)    OS='Cygwin';;
  MINGW*)     OS='MinGw';;
  SunOS*)     OS='Solaris';;
  AIX*)       OS='AIX';;
  *)          OS='UNKNOWN';;
esac

if [ $OS = 'Linux' ]; then
  echo Linux
elif [ $OS = "MacOSX" ]; then
  echo MacOSX
fi

miniconda=Miniconda3-latest-$OS-x86_64.sh
anaconda=Anaconda3-2020.02-$OS-x86_64.sh
miniconda_mirror=https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/$miniconda
anaconda_mirror=https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/$anaconda
conda=$miniconda
conda_mirror=$miniconda_mirror
conda_type=1
selected_conda=0
install_dir=~/miniconda3

function select_conda() {
  if [ ${selected_conda}x = "0"x ]; then
    read -p "Select conda miniconda([1]), anaconda(2):" conda_type
    conda_type=${conda_type:-1}
    selected_conda=1
    case $conda_type in
      1) ;;
      2)
        conda=$anaconda
        conda_mirror=$anaconda_mirror
        install_dir=~/anaconda3
        ;;
      *)
        echo "enter 1 or 2, please."
        exit
        ;;
    esac
  fi
}

function download_conda() {
  read -p "Download conda?([y]/n):" input
  input=${input:-y}
  case $input in
    [yY]*)
      select_conda
      if [ ${conda_type}x = "1"x ]; then
          echo "Download miniconda"
      elif [ ${conda_type}x = "2"x ]; then
          echo "Download anaconda"
      fi
      curl -O $conda_mirror
      ;;
    [nN]*)
      ;;
    *)
      echo "enter y or n, please."
      exit
      ;;
  esac
}

function install_conda() {
  read -p "Install conda?([y]/n):" input
  input=${input:-y}
  case $input in
    [yY]*)
      select_conda
      if [ ${conda_type}x = "1"x ]; then
        echo "Install miniconda"
      elif [ ${conda_type}x = "2"x ]; then
        echo "Install anaconda"
      fi
      chmod +x ./$conda
      ./$conda -u fork
      ;;
    [nN]*)
      ;;
    *) ;;
  esac
}

function install_env() {
  select_conda
  default_install_dir=$install_dir
  read -p "Input conda install dir (Default dir is $default_install_dir):" install_dir
  install_dir=${install_dir:-$default_install_dir}
  source $install_dir/bin/activate
  $install_dir/bin/python ./install.py
}

function main() {
  download_conda
  install_conda
  install_env
}

main