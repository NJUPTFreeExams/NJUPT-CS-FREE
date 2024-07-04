# 说明及一些参考资料

该目录下是此课程四次实验的相关资料。

- 第一次实验：datalab
- 第二次实验：bomblab
- 第三次实验：attacklab
- 第四次实验：linklab

## 实验环境

本课程的四次实验基本都会在学校提供的服务器上完成，要求各位使用 [SSH](https://en.wikipedia.org/wiki/Secure_Shell) 连接到服务器。前期准备可能需要各位安装一个 ubuntu 虚拟机并学习一些基本的 Linux 终端命令。在此简单地为各位提供一些资料：

### 安装虚拟机（或者不安装）

按照老师的要求，你首先需要安装一个虚拟机软件，如 VMWare，然后再在其中安装一个 Ubuntu。但是，如果你有一台 Mac 或者本身正在使用一台预装了 Linux 的机器，那你实际上可以直接跳过这一步，直接使用系统的终端，使用自带的 ssh 连接服务器即可。

如果你使用 Windows 系统，那你也可以通过安装 [git](https://git-scm.com/) 来获得一个 git-bash 并在其中直接使用 ssh 连接服务器。

如果你在使用 Windows 系统，并且非要安装一个虚拟机，那我建议你安装 WSL2，而非按照老师的要求安装一个完整的带图形界面的 Ubuntu 虚拟机。可以参考*[如何使用 WSL 在 Windows 上安装 Linux | Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/wsl/install)*。

如果你就是要安装 VMWare 然后安装 Ubuntu，请关注 _[博通直接放大招：VMware Workstation Pro 和 Fusion Pro 对个人完全免费](https://www.landiannews.com/archives/103898.html)_ 这样一条新闻。建议直接到官方途径下载该虚拟机软件，不要去找什么破解版资源了。

## 连接到服务器

你可以使用多种方式连接到服务器，下面介绍三种常用的：在终端中连接、在 VS Code 中连接、使用第三方软件连接。

### 终端连接

打开你的终端，使用以下命令来连接到服务器：

```bash
ssh username@hostname
```

在此我们约定：`username` 在这几次实验中指的都是你的学号，`hostname` 指的都是学校的服务器地址。举例而言，如果你的学号是 `B22040000`，服务器地址是 `10.160.106.190`，那么你的连接命令就应该是 `ssh B22040000@10.160.106.190`。

### 使用 VS Code 连接

使用 VS Code 连接的好处在于，即使你不会使用终端文本编辑器（如 Vim）或十六进制编辑器（如 hexedit），你也可以直接使用 VS Code 及其 [Hex Editor](https://marketplace.visualstudio.com/items?itemName=ms-vscode.hexeditor) 扩展来方便地进行纯文本和十六进制编辑。

具体的方法请参考 _[Developing on Remote Machines using SSH and Visual Studio Code](https://code.visualstudio.com/docs/remote/ssh)_。

### 使用第三方软件连接

使用第三方软件的主要目的在于图形化地管理你服务器上的文件，毕竟输入 `scp` 来上传实验报告还是挺麻烦的。下面是两个可用的第三方软件：

- [WinSCP](https://winscp.net/eng/download.php)
- [FileZilla](https://filezilla-project.org/)

### 配置使用密钥登录服务器

使用 ssh 登录服务器时，会要求你输入你的密码。实验手册还会要求你使用 `passwd` 命令来修改你自己的密码。每次登录都需要输入密码还挺麻烦的，所以，你可以使用以下命令序列配置一个本地密钥验证，这样就不用每次都输入密码了。

```bash
ssh-keygen -t ed25519 # 生成一个 ssh 密钥对（如果你还没有的话），生成过程中一直按回车就可以了。
ssh-copy-id username@hostname # 将生成的公钥复制到服务器上去。还记得 username 和 hostname 的约定吗？别忘了替换成你自己的。这里会要求你输入一次你的密码。
ssh username@hostname # 现在再登录服务器就不需要你输入密码了，自动采用本地密钥验证了。
```

## 终端基本知识及一些常用的终端命令

连接上服务器，你应该位于 `/home/username/` 这样一个目录下（记得我们的约定，记得替换）。这是你的家目录，在命令提示符中（prompt）中，显示为一个 `~`。

使用下面的命令来看看你是不是在这个位置：

```bash
pwd # print working directory 打印工作目录，即打印你现在所在的那层目录的完整路径
```

在类 Unix 操作系统中，所有路径的根都是 `/`，以 `/` 开头的路径因此是一个完整的路径，称为绝对路径。但很多时候，我们使用的是基于当前工作目录的相对路径。例如，如果我现在位于 `/home/username/`，那么这个目录下的文件 `hello.txt` 的绝对路径是 `/home/username/hello.txt`，相对路径就是 `hello.txt`。有两个特殊的符号用于表示当前目录和上一层目录，分别是 `.` 和 `..`。在实验中，你可能需要执行一个你编译产生的文件（如 `linkbomb`），你会使用 `./linkbomb` 来执行它，在这里 `.` 表示当前路径，而 `./linkbomb` 就表示当前路径下的文件 `linkbomb`。

使用 `cd`（change directory）来切换你所在的目录：

```bash
cd lab1 # 进入当前目录下的 lab1 子目录（如果有的话）
cd .. # 返回上层目录
cd # 返回家目录
```

创建和删除目录：

```bash
mkdir lab1 # make directory 在当前目录下创建一个 lab1 目录
rmdir lab1 # remove directory 删除当前目录下的 lab1 目录，lab1 必须是空的
rm -r lab1 # 如果 lab1 非空，可以使用 rm（remove）命令的递归（recursively）删除来完整删除这个目录
```

复制、移动和重命名：

```bash
cp hello.txt world.txt # copy 复制 hello.txt，副本名称为 world.txt
scp hello.txt username@hostname:/home/username # 类似的，scp 也只是一种复制工具，该命令将 hello.txt 复制到 hostname 服务器的 username 用户的家目录下
mv hello.txt lab1/ # move 移动当前目录下的 hello.txt 到子目录 lab1 之中
mv hello.txt world.txt # 你可以直接使用 mv 来重命名 hello.txt 为 world.txt
```

## 更多资源

- _[计算机教育中缺失的一课 The Missing Semester of Your CS Education 中文版](https://missing-semester-cn.github.io/)_：教会你使用很多计算机学科的常用工具及基本知识
- _[CSAPP 官方实验介绍](http://csapp.cs.cmu.edu/3e/labs.html)_：官方的实验介绍站。你可以在这儿找到有关每个实验的更多的资料，非常建议你读一读每个实验的 writeup 之后再开始做那些实验。注意，不包括 linklab，因为那不是官方实验。
