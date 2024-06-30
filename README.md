# DashTrack

## Installation (&#x26a0;&#xfe0f; WIP)

In its current iteration, this method will not work. We are still in the process of setting up a reliable distribution target.

```
brew tap KartavyaSharma/DashTrack-Homebrew
brew install dashtrack
```

## Installation (for developers)

```
git clone https://github.com/KartavyaSharma/DashTrack.git
cd DashTrack
```

Then, run the following commands to get access to the DEV home directory variable.

```
export DT_HOME=$(pwd)
```

Run the following commands to install the nessasary brew packages.

```
brew install bash coreutils gum docker gawk unzip gnu-tar bat wget rm-improved colima openssl@1.1 python-setuptools
```
