#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import urllib
import webbrowser
import platform
from urllib.request import urlretrieve


class Util:
    @staticmethod
    def popen(cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        return out

    @staticmethod
    def check_input_yes(input_str):
        answer = input(input_str) or 'y'
        if answer == 'y':
            return True

        return False


class CondaPT:
    def __init__(self):
        self.currentdir = os.path.dirname(__file__)
        print('currentdir:', self.currentdir)

        self.conda_settings = '''channels:
  - defaults
show_channel_urls: true
channel_alias: https://mirrors.tuna.tsinghua.edu.cn/anaconda
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud'''

        self.pip_settings = '''[global]
index-url=https://mirrors.aliyun.com/pypi/simple
[install]
trusted-host=mirrors.aliyun.com'''

        self.pip_settings_tuna = '''[global]
index-url=https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host=pypi.tuna.tsinghua.edu.cn'''

        self.silent_mode = True
        self.conda_packages = ['tensorboard',
                               'ipython',
                               'matplotlib',
                               'pandas',
                               'jupyter notebook'
                               ]
        self.pip_packages = ['opencv-python']
        self.python_ver = '3.8'
        self.pt_env = f'pytorch{self.python_ver}'
        self.tf_env = f'tensorflow{self.python_ver}'
        self.pathenv = None

    def conda_install(self, env, *packages):
        if env != '':
            env = f'-n {env} '
        conda_install = f'conda install {env}'
        if self.silent_mode:
            conda_install = f'conda install -y {env}'

        conda_install = conda_install + ' '.join(packages)
        print(conda_install)
        os.system(conda_install)

    def pip_install(self, *packages):
        pip_install = 'pip install '

        pip_install = pip_install + ' '.join(packages)
        print(pip_install)
        os.system(pip_install)

    def setup_conda(self):
        condarc = os.path.join(os.path.expanduser('~'), r'.condarc')
        if os.path.exists(condarc):
            with open(condarc, 'r') as f:
                content = f.read()
                if self.conda_settings in content:
                    return

        print('\nSetup conda mirror\n')
        with open(condarc, 'w') as f:
            f.write(self.conda_settings)
        os.system('conda config --set remote_max_retries 10')
        os.system('conda config --set remote_read_timeout_secs 300')
        # enable yes to all in current env
        # os.system('conda config --env --set always_yes true')
        # disable it in current env
        # os.system('conda config --env --remove always_yes')
        os.system('conda config --show')

        os.system('conda clean -i ')
        os.system('conda update -n base -c defaults conda -y')
        if platform.system() == "Darwin":
            dirname = os.path.dirname(sys.executable)
            if not os.path.exists(os.path.join(dirname, '../lib/libffi.6.dylib')):
                command = 'ln -s %s %s' % (os.path.join(dirname, '../lib/libffi.7.dylib'),
                                           os.path.join(dirname, '../lib/libffi.6.dylib'))
                os.system(command)

    def setup_pip(self):
        pippathname = 'pip'
        pipconfname = 'pip.ini'
        if not platform.system() == "Windows":
            pippathname = '.pip'
            pipconfname = 'pip.conf'

        pipconfpath = os.path.join(os.path.expanduser('~'), pippathname)
        if not os.path.exists(pipconfpath):
            os.mkdir(pipconfpath)

        pipconf = os.path.join(pipconfpath, pipconfname)
        if os.path.exists(pipconf):
            with open(pipconf, 'r') as f:
                content = f.read()
                if self.pip_settings in content:
                    return

        print('\nSetup pip mirror\n')
        with open(pipconf, 'w') as f:
            f.write(self.pip_settings)

        self.conda_install('', 'pip')
        os.system('pip config list')

    def setup_cuda(self):
        if not Util.check_input_yes('Setup cuda?([y]/n):'):
            return

        # os.system('nvidia-smi')
        # cuda = Util.check_input_yes('Is cuda available?(y/n):')
        # geforce_url = 'http://cn.download.nvidia.com/GFE/GFEClient/3.20.3.63/GeForce_Experience_v3.20.3.63.exe'
        # print('Downloading GeForce Experience')
        # urlretrieve(geforce_url, "GeForce_Experience_v3.20.3.63.exe")
        # os.system("GeForce_Experience_v3.20.3.63.exe")
        # https://developer.nvidia.com/cuda-downloads
        print('Download driver and install')
        webbrowser.open("https://www.geforce.cn/drivers")

        if Util.check_input_yes('Driver has been installed?([y]/n):'):
            pass

    def install_conda_packages(self, env, packages=[]):
        conda_packages = self.conda_packages + packages
        print('\nInstall conda packages', conda_packages, '\n')
        self.conda_install(env, *conda_packages)

    def install_pip_packages(self, packages=[]):
        pip_packages = self.pip_packages + packages
        print('\nInstall pip packages', pip_packages, '\n')
        self.pip_install(*pip_packages)

    def update_env_path(self, env):
        dirname = os.path.dirname(sys.executable)
        envpath = os.path.join(dirname, f'envs/{env}')
        if platform.system() != "Windows":
            envpath = os.path.join(dirname, f'../envs/{env}')
            python = os.path.join(envpath, 'bin/python')
            pathlist = [
                os.path.join(envpath, 'bin'),
            ]
        else:
            pathlist = [
                envpath,
                os.path.join(envpath, 'Library/mingw-w64/bin'),
                os.path.join(envpath, 'Library/usr/bin'),
                os.path.join(envpath, 'Library/bin'),
                os.path.join(envpath, 'Scripts'),
                os.path.join(envpath, 'bin'),
            ]

        if self.pathenv:
            os.environ["PATH"] = os.environ["PATH"].replace(self.pathenv, '')
            # print(os.environ["PATH"])

        self.pathenv = os.pathsep.join(pathlist) + os.pathsep
        os.environ["PATH"] = self.pathenv + os.environ["PATH"]
        # print(os.environ["PATH"])

    def create_env(self, env, python_ver):
        # command = 'conda create -n %s python=3.7 -y' % env
        env = input(f'Enter env name (default is {env}):') or env
        python_ver = input(f'Enter python version (default is {python_ver}):') or python_ver
        # conda remove -n name --all
        command = f'conda create -n {env} python={python_ver}'
        if platform.system() != "Windows":
            command += ' && eval "$(conda shell.bash hook)"'
        command += f' && conda activate {env}'
        command += ' && conda env list'
        os.system(command)
        self.update_env_path(env)

    def install_pytorch(self):
        if not Util.check_input_yes('Install pytorch?([y]/n):'):
            return

        print('\nInstalling pytorch.\n')
        env = self.pt_env
        self.create_env(env, self.python_ver)
        conda = True
        if conda:
            # www.pytorch.org
            # conda install -n pytorch
            if platform.system() == "Darwin":
                self.conda_install(env, 'pytorch torchvision -c pytorch')
            else:
                if Util.check_input_yes('Install cuda version?([y]/n):'):
                    self.conda_install(env, 'pytorch torchvision cudatoolkit=10.2 -c pytorch')
                else:
                    self.conda_install(env, 'pytorch torchvision cpuonly -c pytorch')
        else:
            if platform.system() == "Darwin":
                self.pip_install('torch torchvision')
            else:
                if Util.check_input_yes('Install cuda version?([y]/n):'):
                    self.pip_install(env,
                                     'torch===1.5.0 torchvision===0.6.0 -f https://download.pytorch.org/whl/torch_stable.html')
                else:
                    self.pip_install(env,
                                     'torch==1.5.0+cpu torchvision==0.6.0+cpu -f https://download.pytorch.org/whl/torch_stable.html')
        self.install_conda_packages(env)
        self.install_pip_packages(['visdom'])
        print('\nInstall pytorch done.')

    def install_tensorflow(self):
        if not Util.check_input_yes('Install tensorflow?([y]/n):'):
            return

        print('\nInstalling tensorflow.\n')
        env = self.tf_env
        self.create_env(env, self.python_ver)
        conda = True
        if conda:
            if platform.system() == "Darwin":
                self.conda_install(env, 'tensorflow')
            else:
                if Util.check_input_yes('Install gpu?([y]/n):'):
                    self.conda_install(env, 'tensorflow-gpu')
                else:
                    self.conda_install(env, 'tensorflow')
        else:
            if platform.system() == "Darwin":
                self.pip_install(env, 'tensorflow')
            else:
                if Util.check_input_yes('Install gpu?([y]/n):'):
                    self.pip_install('tensorflow-gpu')
                else:
                    self.pip_install('tensorflow')
        self.install_conda_packages(env)
        self.install_pip_packages()
        print('\nInstall tensorflow done.')

    def install_pycharm(self):
        if not Util.check_input_yes('Install pycharm?([y]/n):'):
            return

        print('\nInstall pycharm.\n')
        url = "https://www.jetbrains.com/pycharm/download/"
        webbrowser.open(url)

    def check_env(self, env, check_code):
        print()
        print('-' * 60, end='\n\n')
        print(f'check {env} env\n')
        with open('check.py', 'w') as f:
            f.write(check_code)

        dirname = os.path.dirname(sys.executable)
        envpath = os.path.join(dirname, f'envs/{env}')
        python = os.path.join(envpath, 'python')
        self.update_env_path(env)
        os.system(f'{python} check.py')
        print()
        print('-' * 60, end='\n\n')
        os.remove('check.py')

    def check_pt(self):
        check_code = '''import torch
print('torch.__version__', torch.__version__)
print('torch.cuda.is_available()', torch.cuda.is_available())'''
        self.check_env(self.pt_env, check_code)

    def check_tf(self):
        check_code = '''import tensorflow as tf
print('tf.__version__', tf.__version__)
print()
print('tf.test.is_gpu_available()', tf.test.is_gpu_available())
print()
print("tf.config.list_physical_devices('GPU')", tf.config.list_physical_devices('GPU'))'''
        self.check_env(self.tf_env, check_code)

    def setup_jupyter(self):
        jupyter_conf = os.path.join(os.path.expanduser('~'), '.jupyter/jupyter_notebook_config.py')
        if not os.path.exists(jupyter_conf):
            os.system('jupyter notebook --generate-config')

    def run(self):
        self.setup_conda()
        self.setup_pip()
        self.setup_cuda()
        self.install_pytorch()
        self.check_pt()
        self.install_tensorflow()
        self.check_tf()
        self.install_pycharm()
        # self.setup_jupyter()


def main():
    condaPT = CondaPT()
    condaPT.run()
    pass


if __name__ == "__main__":
    main()
